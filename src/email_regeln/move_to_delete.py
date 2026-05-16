"""Verschiebt alle Mails bestimmter Absender aus der INBOX in einen konfigurierbaren Zielordner."""

from __future__ import annotations

import imaplib

from email_regeln.imap_connection import connect

TARGET_FOLDER = "Folders/to-be-deleted"


def _search_by_sender(mail: imaplib.IMAP4, sender: str) -> list[bytes]:
    """Sucht in der aktuell selektierten Mailbox nach Mails eines Absenders."""
    quoted = f'"{sender}"'
    if sender.isascii():
        _status, data = mail.search(None, "FROM", quoted)
    else:
        prev_encoding = mail._encoding
        mail._encoding = "utf-8"
        try:
            _status, data = mail.search("UTF-8", "FROM", quoted)
        finally:
            mail._encoding = prev_encoding
    return data[0].split()


def _move_messages(
    mail: imaplib.IMAP4, msg_ids: list[bytes], target_folder: str
) -> int:
    """Verschiebt Nachrichten per COPY + STORE \\Deleted + EXPUNGE. Gibt Anzahl zurueck."""
    id_set = b",".join(msg_ids)
    mail.copy(id_set, target_folder)
    mail.store(id_set, "+FLAGS", "\\Deleted")
    mail.expunge()
    return len(msg_ids)


def run(
    absender: list[str],
    *,
    target_folder: str = TARGET_FOLDER,
    folder: str = "INBOX",
    dry_run: bool = True,
    mail: imaplib.IMAP4 | None = None,
) -> int:
    """Verschiebt alle Mails der gegebenen Absender aus *folder* in den Zielordner.

    Gibt die Gesamtanzahl (gefunden bzw. verschoben) zurueck.
    Wird *mail* uebergeben, wird die Verbindung NICHT geschlossen (Caller verwaltet sie).
    """
    own_connection = mail is None
    if own_connection:
        if dry_run:
            print("=== DRY RUN – es werden keine Mails verschoben ===\n")
        print(f"Verbinde mit Protonmail Bridge … Quelle: {folder}, Ziel: {target_folder}")
        mail = connect()

    try:
        quoted = f'"{folder}"' if " " in folder else folder
        mail.select(quoted, readonly=dry_run)
        total = 0

        for sender in absender:
            msg_ids = _search_by_sender(mail, sender)
            count = len(msg_ids)

            if count == 0:
                continue

            if dry_run:
                print(f"  {sender}: {count} Mail(s) wuerden verschoben")
                total += count
            else:
                moved = _move_messages(mail, msg_ids, target_folder)
                total += moved
                print(f"  {sender}: {moved} Mail(s) verschoben")

        if own_connection:
            print()
            if dry_run:
                print("Dry-Run abgeschlossen. Mit dry_run=False ausfuehren zum Verschieben.")
            else:
                print(f"Fertig. {total} Mail(s) insgesamt verschoben.")

        return total
    finally:
        if own_connection:
            mail.logout()


def undo(*, dry_run: bool = True) -> None:
    """Verschiebt alle Mails aus Folders/to-be-deleted zurueck in die INBOX."""
    if dry_run:
        print("=== DRY RUN – es werden keine Mails verschoben ===\n")

    print("Verbinde mit Protonmail Bridge …")
    mail = connect()

    try:
        mail.select(TARGET_FOLDER, readonly=dry_run)
        _status, data = mail.search(None, "ALL")
        msg_ids = data[0].split()

        if not msg_ids:
            print("Keine Mails in Folders/to-be-deleted gefunden.")
            return

        if dry_run:
            print(f"{len(msg_ids)} Mail(s) wuerden zurueck in INBOX verschoben.")
        else:
            moved = _move_messages(mail, msg_ids, "INBOX")
            print(f"{moved} Mail(s) zurueck in INBOX verschoben.")
    finally:
        mail.logout()


if __name__ == '__main__':
    undo(dry_run=False)