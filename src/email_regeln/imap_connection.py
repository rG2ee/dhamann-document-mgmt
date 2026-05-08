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


def print_folder_tree(mail: imaplib.IMAP4 | None = None) -> None:
    """Gibt die Ordnerstruktur als Baum auf stdout aus."""
    folders = list_folders(mail)

    for folder in folders:
        depth = folder.count("/")
        name = folder.rsplit("/", 1)[-1]
        print(f"{'  ' * depth}{name}")



if __name__ == '__main__':
    print_folder_tree()