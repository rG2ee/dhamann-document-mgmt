"""Read-only Diagnose: findet, wohin Mails aus Sent verschoben wurden.

Hintergrund: Laeuft run.py mit folder="All Mail", werden auch gesendete Mails
erfasst. Da Protonmail-Ordner exklusiv sind, nimmt ein COPY in einen Zielordner
die Nachricht aus Sent heraus.

Dieses Skript veraendert keine Mails: alle SELECTs laufen mit readonly=True.
"""

from __future__ import annotations

import email
import imaplib
import json
import os
import shutil
from datetime import datetime
from email.header import decode_header, make_header
from pathlib import Path

from dotenv import load_dotenv

from email_regeln.imap_connection import (
    _folder_message_count,
    connect,
    list_folders,
)

_STATE_DIR = Path(__file__).resolve().parents[2] / "email-state"
_TREE_FILE = _STATE_DIR / "folder_tree.json"

# Virtuelle bzw. Sammel-Ordner, die als Fundort nichts aussagen.
_SKIP_FOLDERS = {"All Mail", "Drafts", "Sent", "Folders", "Labels", "Starred"}

_SAMPLE_COUNT = 5


def _backup_tree() -> dict[str, int | None]:
    """Sichert den alten Folder-Tree und gibt ihn zurueck (leer, wenn keiner existiert)."""
    if not _TREE_FILE.exists():
        print(f"Kein alter Folder-Tree in {_TREE_FILE} – Vorher-Vergleich nicht moeglich.\n")
        return {}

    stamp = datetime.fromtimestamp(_TREE_FILE.stat().st_mtime).strftime("%Y%m%d-%H%M%S")
    backup = _TREE_FILE.with_name(f"folder_tree.{stamp}.backup.json")
    if not backup.exists():
        shutil.copy2(_TREE_FILE, backup)
        print(f"Backup des alten Folder-Trees: {backup.name}")
    print(f"Stand des alten Snapshots: {stamp}\n")
    return json.loads(_TREE_FILE.read_text())


def _quote(folder: str) -> str:
    return f'"{folder}"'


def _search_from(mail: imaplib.IMAP4, folder: str, needle: str) -> list[bytes] | None:
    """Sucht Mails in *folder*, deren From-Header *needle* enthaelt. Rein lesend.

    Gibt None zurueck, wenn der Ordner nicht selektiert werden kann.
    """
    status, _ = mail.select(_quote(folder), readonly=True)
    if status != "OK":
        return None

    if needle.isascii():
        status, data = mail.search(None, "FROM", f'"{needle}"')
    else:
        prev = mail._encoding
        mail._encoding = "utf-8"
        try:
            status, data = mail.search("UTF-8", "FROM", f'"{needle}"')
        finally:
            mail._encoding = prev

    if status != "OK" or not data or not data[0]:
        return []
    return data[0].split()


def _decode(raw: str | None) -> str:
    if not raw:
        return ""
    try:
        return str(make_header(decode_header(raw)))
    except Exception:
        return raw


def _print_samples(mail: imaplib.IMAP4, folder: str, msg_ids: list[bytes]) -> None:
    """Gibt Kopfdaten einiger Nachrichten aus, damit der Fund verifizierbar ist."""
    mail.select(_quote(folder), readonly=True)
    for msg_id in msg_ids[-_SAMPLE_COUNT:]:
        status, data = mail.fetch(msg_id, "(BODY.PEEK[HEADER.FIELDS (DATE FROM TO SUBJECT)])")
        if status != "OK" or not data or not isinstance(data[0], tuple):
            continue
        msg = email.message_from_bytes(data[0][1])
        print(f"      {_decode(msg.get('Date'))}")
        print(f"        von     : {_decode(msg.get('From'))}")
        print(f"        an      : {_decode(msg.get('To'))}")
        print(f"        Betreff : {_decode(msg.get('Subject'))}")


def _step_1_diff(mail: imaplib.IMAP4, folders: list[str], old_tree: dict[str, int | None]) -> None:
    print("=== Schritt 1: Veraenderung der Nachrichtenanzahl je Ordner ===\n")
    if not old_tree:
        print("  (uebersprungen – kein Vorher-Snapshot)\n")
        return

    deltas: list[tuple[int, str, int, int]] = []
    for folder in folders:
        new = _folder_message_count(mail, folder)
        old = old_tree.get(folder)
        if new is None or old is None or new == old:
            continue
        deltas.append((new - old, folder, old, new))

    if not deltas:
        print("  Keine Unterschiede – der Snapshot entstand wohl nach dem Lauf.\n")
        return

    for delta, folder, old, new in sorted(deltas, key=lambda t: -abs(t[0])):
        print(f"  {delta:+8d}  {folder}  ({old} → {new})")

    neu_dazu = [d for d in deltas if d[0] > 0]
    if neu_dazu:
        groesster = max(neu_dazu, key=lambda t: t[0])
        print(f"\n  Groesster Zuwachs: {groesster[1]} ({groesster[0]:+d})")
    print()


def _step_2_own_mails(
    mail: imaplib.IMAP4, folders: list[str], own_address: str
) -> list[tuple[int, str, list[bytes]]]:
    print(f"=== Schritt 2: Mails mit '{own_address}' im From-Header je Ordner ===\n")
    hits: list[tuple[int, str, list[bytes]]] = []

    for folder in folders:
        if folder in _SKIP_FOLDERS:
            continue
        msg_ids = _search_from(mail, folder, own_address)
        if msg_ids is None:
            print(f"  {'n/a':>8}  {folder}  (nicht selektierbar)")
            continue
        if msg_ids:
            hits.append((len(msg_ids), folder, msg_ids))

    if not hits:
        print("  Keine eigenen Mails ausserhalb von Sent gefunden.\n")
        return hits

    for count, folder, _ in sorted(hits, key=lambda t: -t[0]):
        print(f"  {count:8d}  {folder}")
    print(f"\n  Summe: {sum(c for c, _, _ in hits)} Mail(s)\n")
    return hits


def _step_3_samples(mail: imaplib.IMAP4, hits: list[tuple[int, str, list[bytes]]]) -> None:
    if not hits:
        return
    print("=== Schritt 3: Stichproben aus den auffaelligsten Ordnern ===\n")
    for count, folder, msg_ids in sorted(hits, key=lambda t: -t[0])[:3]:
        print(f"  {folder} ({count} Mail(s)):")
        _print_samples(mail, folder, msg_ids)
        print()


def main() -> None:
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    own_address = os.environ["IMAP_Username"]

    old_tree = _backup_tree()

    print("Verbinde mit Protonmail Bridge …\n")
    mail = connect()
    try:
        folders = list_folders(mail)
        print(f"{len(folders)} Ordner gefunden.\n")

        _step_1_diff(mail, folders, old_tree)
        hits = _step_2_own_mails(mail, folders, own_address)
        _step_3_samples(mail, hits)
    finally:
        mail.logout()


if __name__ == "__main__":
    main()
