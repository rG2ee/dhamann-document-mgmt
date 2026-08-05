"""Holt faelschlich verschobene Sent-Mails aus einem Zielordner zurueck.

Vorgeschichte: Ein Lauf von run.py mit folder="All Mail" hat den Suchbegriff
"dennis.hamann@protonmail.com" (eigene Adresse, eingetragen unter
Folders/filter-andwendungen/persoenliche-kontakte) auf ALLE Mails angewendet.
Da jede gesendete Mail die eigene Adresse im From-Header traegt und
Protonmail-Ordner exklusiv sind, wurde damit der komplette Sent-Ordner
nach persoenliche-kontakte verschoben.

Dieses Skript verschiebt Mails mit der eigenen Adresse im From-Header aus dem
Quellordner zurueck nach "Sent". Standard ist ein Dry-Run.

Die Bridge akzeptiert COPY nach "Sent" und sortiert dabei selbst nach Charakter
der Nachricht: Entwuerfe landen in "Drafts", Mails an die eigene Adresse
zusaetzlich in der INBOX.
"""

from __future__ import annotations

import email
import imaplib
import os
import re
from collections import Counter
from email.header import decode_header, make_header
from pathlib import Path

from dotenv import load_dotenv

from email_regeln.imap_connection import connect
from email_regeln.move_to_delete import own_addresses

SOURCE_FOLDER = "Folders/filter-andwendungen/persoenliche-kontakte"
RESTORE_FOLDER = "Sent"

_BATCH_SIZE = 200
_UID_RE = re.compile(rb"UID (\d+)")


def _own_address() -> str:
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    return os.environ["IMAP_Username"]


def _search_own(mail: imaplib.IMAP4, adressen: list[str]) -> list[bytes]:
    """Sucht Mails, deren From-Header eine der eigenen Adressen enthaelt."""
    gefunden: list[bytes] = []
    gesehen: set[bytes] = set()
    for adresse in adressen:
        status, data = mail.uid("SEARCH", None, "FROM", f'"{adresse}"')
        if status != "OK" or not data or not data[0]:
            continue
        for uid in data[0].split():
            if uid not in gesehen:
                gesehen.add(uid)
                gefunden.append(uid)
    return gefunden


def _decode(raw: str | None) -> str:
    if not raw:
        return ""
    try:
        return str(make_header(decode_header(raw)))
    except Exception:
        return raw


def _fetch_headers(mail: imaplib.IMAP4, uids: list[bytes]) -> dict[bytes, email.message.Message]:
    """Holt die Kopfzeilen der Nachrichten. Nutzt BODY.PEEK, setzt also kein \\Seen."""
    headers: dict[bytes, email.message.Message] = {}
    for start in range(0, len(uids), _BATCH_SIZE):
        batch = ",".join(uid.decode() for uid in uids[start : start + _BATCH_SIZE])
        status, data = mail.uid(
            "FETCH",
            batch,
            "(BODY.PEEK[HEADER.FIELDS (DATE FROM TO CC SUBJECT)])",
        )
        if status != "OK":
            continue

        # Die Bridge liefert je Nachricht ein Tupel (Prefix, Rohdaten) und danach
        # ein Byte-Fragment mit der UID, z.B. b' UID 260)'.
        pending: email.message.Message | None = None
        for item in data:
            if isinstance(item, tuple):
                prefix, raw = item
                pending = email.message_from_bytes(raw)
                match = _UID_RE.search(prefix)
                if match:
                    headers[match.group(1)] = pending
                    pending = None
            elif isinstance(item, bytes) and pending is not None:
                match = _UID_RE.search(item)
                if match:
                    headers[match.group(1)] = pending
                    pending = None
    return headers


def _classify(msg: email.message.Message, own_address: str) -> str:
    """Unterscheidet Notizen an sich selbst von echten Mails an andere."""
    recipients = f"{msg.get('To', '')} {msg.get('Cc', '')}".lower()
    return "an mich selbst" if own_address.lower() in recipients else "an andere"


def _ensure_folder(mail: imaplib.IMAP4, folder: str) -> None:
    status, _ = mail.create(folder)
    if status == "OK":
        print(f"Ordner erstellt: {folder}")
    else:
        print(f"Ordner existiert bereits: {folder}")
    mail.subscribe(folder)


def _move(mail: imaplib.IMAP4, uids: list[bytes], target: str) -> int:
    """Verschiebt per UID COPY + STORE \\Deleted + EXPUNGE, batchweise.

    Bricht ab, wenn ein COPY fehlschlaegt, damit nie geloescht wird, was nicht
    vorher erfolgreich kopiert wurde.
    """
    moved = 0
    for start in range(0, len(uids), _BATCH_SIZE):
        chunk = uids[start : start + _BATCH_SIZE]
        batch = ",".join(uid.decode() for uid in chunk)

        status, response = mail.uid("COPY", batch, f'"{target}"')
        if status != "OK":
            raise RuntimeError(f"COPY nach {target} fehlgeschlagen: {status} {response!r}")

        status, response = mail.uid("STORE", batch, "+FLAGS", "\\Deleted")
        if status != "OK":
            raise RuntimeError(f"STORE \\Deleted fehlgeschlagen: {status} {response!r}")

        mail.expunge()
        moved += len(chunk)
        print(f"  {moved}/{len(uids)} verschoben …")
    return moved


def restore(
    *,
    dry_run: bool = True,
    source: str = SOURCE_FOLDER,
    target: str = RESTORE_FOLDER,
    only_to_others: bool = False,
) -> int:
    """Verschiebt eigene Mails aus *source* nach *target*.

    only_to_others=True beschraenkt auf Mails an fremde Empfaenger, laesst also
    die Notizen an sich selbst im Quellordner liegen.
    """
    own_address = _own_address()
    adressen = own_addresses()
    mode = "DRY RUN" if dry_run else "LIVE"
    print(f"=== {mode} ===")
    print(f"Quelle : {source}")
    print(f"Ziel   : {target}")
    print(f"Filter : From enthaelt eine von {', '.join(adressen)}")
    if only_to_others:
        print("         nur Mails an fremde Empfaenger")
    print()

    print("Verbinde mit Protonmail Bridge …")
    mail = connect()
    try:
        status, _ = mail.select(f'"{source}"', readonly=True)
        if status != "OK":
            raise RuntimeError(f"Quellordner nicht selektierbar: {source}")

        uids = _search_own(mail, adressen)
        if not uids:
            print("Keine passenden Mails gefunden.")
            return 0

        print(f"{len(uids)} Mail(s) mit eigener Absenderadresse gefunden.\n")

        headers = _fetch_headers(mail, uids)
        kinds = Counter(_classify(msg, own_address) for msg in headers.values())
        for kind, count in kinds.most_common():
            print(f"  {count:6d}  {kind}")

        jahre = Counter()
        for msg in headers.values():
            datum = _decode(msg.get("Date"))
            jahr = next((t for t in datum.split() if t.isdigit() and len(t) == 4), "unbekannt")
            jahre[jahr] += 1
        print("\n  Verteilung nach Jahr:")
        for jahr, count in sorted(jahre.items()):
            print(f"    {jahr}: {count}")

        if only_to_others:
            uids = [u for u in uids if _classify(headers[u], own_address) == "an andere"]
            print(f"\nNach Filter verbleiben {len(uids)} Mail(s).")

        print("\n  Beispiele:")
        for uid in uids[:3] + uids[-3:]:
            msg = headers.get(uid)
            if msg is None:
                continue
            print(f"    {_decode(msg.get('Date'))} → {_decode(msg.get('To'))}")
            print(f"      {_decode(msg.get('Subject'))}")

        if dry_run:
            print(f"\nDry-Run: {len(uids)} Mail(s) wuerden nach {target} verschoben.")
            print("Mit dry_run=False ausfuehren zum Verschieben.")
            return len(uids)

        print()
        _ensure_folder(mail, target)

        # Fuer den Schreibvorgang neu selektieren, diesmal nicht readonly.
        status, _ = mail.select(f'"{source}"', readonly=False)
        if status != "OK":
            raise RuntimeError(f"Quellordner nicht beschreibbar: {source}")

        moved = _move(mail, uids, target)
        print(f"\nFertig. {moved} Mail(s) nach {target} verschoben.")
        return moved
    finally:
        mail.logout()


if __name__ == "__main__":
    restore(dry_run=True)
