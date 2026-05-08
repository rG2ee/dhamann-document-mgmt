"""Verschiebt alle Mails bestimmter Absender aus der INBOX nach Folders/to-be-deleted."""

from __future__ import annotations

import imaplib

from email_regeln.imap_connection import connect

TARGET_FOLDER = "Folders/to-be-deleted"


def _search_by_sender(mail: imaplib.IMAP4, sender: str) -> list[bytes]:
    """Sucht in der aktuell selektierten Mailbox nach Mails eines Absenders."""
    _status, data = mail.search(None, "FROM", f'"{sender}"')
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


def run(absender: list[str], *, dry_run: bool = True) -> None:
    """Verschiebt alle Mails der gegebenen Absender aus INBOX nach to-be-deleted."""
    if dry_run:
        print("=== DRY RUN – es werden keine Mails verschoben ===\n")

    print("Verbinde mit Protonmail Bridge …")
    mail = connect()

    try:
        mail.select("INBOX", readonly=dry_run)
        total = 0

        for sender in absender:
            msg_ids = _search_by_sender(mail, sender)
            count = len(msg_ids)

            if count == 0:
                print(f"  {sender}: keine Mails gefunden")
                continue

            if dry_run:
                print(f"  {sender}: {count} Mail(s) wuerden verschoben")
            else:
                moved = _move_messages(mail, msg_ids, TARGET_FOLDER)
                total += moved
                print(f"  {sender}: {moved} Mail(s) verschoben")

        print()
        if dry_run:
            print("Dry-Run abgeschlossen. Mit dry_run=False ausfuehren zum Verschieben.")
        else:
            print(f"Fertig. {total} Mail(s) insgesamt verschoben.")
    finally:
        mail.logout()


if __name__ == '__main__':

    run(["communications@iohk.io",
         "info@dfinity.org"], dry_run=False)