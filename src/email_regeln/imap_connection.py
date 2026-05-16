"""Gemeinsame IMAP-Verbindung zur Protonmail Bridge."""

from __future__ import annotations

import imaplib
import os
import re
import ssl
from pathlib import Path

from dotenv import load_dotenv


def connect() -> imaplib.IMAP4:
    """Stellt eine IMAP-Verbindung zur lokalen Protonmail Bridge her."""
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(env_path)

    host = os.environ["IMAP_Address"]
    port = int(os.environ["IMAP_port"])
    username = os.environ["IMAP_Username"]
    password = os.environ["IMAP_Password"]

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    mail = imaplib.IMAP4(host, port)
    mail.starttls(ssl_context=ctx)
    mail.login(username, password)
    return mail


_LIST_RE = re.compile(rb'\((?P<flags>[^)]*)\)\s+"(?P<sep>[^"]+)"\s+"?(?P<name>[^"]*)"?')


def list_folders(mail: imaplib.IMAP4 | None = None) -> list[str]:
    """Gibt alle IMAP-Ordner als sortierte Liste zurueck.

    Kann mit einer bestehenden Verbindung aufgerufen werden,
    oder stellt selbst eine her (und schliesst sie danach).
    """
    own_connection = mail is None
    if own_connection:
        mail = connect()

    try:
        _status, data = mail.list()
        folders: list[str] = []
        for entry in data:
            if not isinstance(entry, bytes):
                continue
            m = _LIST_RE.match(entry)
            if m:
                folders.append(m.group("name").decode("utf-7").replace("&", "+").rstrip())
        return sorted(folders)
    finally:
        if own_connection:
            mail.logout()


def _folder_message_count(mail: imaplib.IMAP4, folder: str) -> int | None:
    """Gibt die Anzahl der Nachrichten in *folder* zurueck (None bei Fehler)."""
    try:
        status, data = mail.status(f'"{folder}"', "(MESSAGES)")
        if status == "OK" and data and data[0]:
            m = re.search(rb"MESSAGES\s+(\d+)", data[0])
            if m:
                return int(m.group(1))
    except imaplib.IMAP4.error:
        pass
    return None


def create_email_folder_in_filter_anwendungen(
    folder_name: str, *, mail: imaplib.IMAP4 | None = None
) -> str:
    """Erstellt einen Ordner unter Folders/filter-andwendungen/.

    Gibt den vollen Pfad des erstellten Ordners zurueck.
    Existiert der Ordner bereits, wird nichts geaendert.
    """
    full_path = f"Folders/filter-andwendungen/{folder_name}"

    own_connection = mail is None
    if own_connection:
        mail = connect()

    try:
        status, _ = mail.create(full_path)
        if status == "OK":
            print(f"Ordner erstellt: {full_path}")
        else:
            print(f"Ordner existiert bereits oder Fehler: {full_path}")
        mail.subscribe(full_path)
        print(f"Ordner abonniert (subscribe): {full_path}")
    finally:
        if own_connection:
            mail.logout()

    return full_path


if __name__ == '__main__':
    from email_regeln.folder_tree import main as folder_tree_main

    folder_tree_main(refresh=True)
