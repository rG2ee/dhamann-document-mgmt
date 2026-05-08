"""Verschiebt alle Mails von 2022 und aelter aus INBOX in einen Archiv-Ordner."""

from __future__ import annotations

from email_regeln.imap_connection import connect

DIR_NAME = "Folders/filter-andwendungen/2022_and_older"


def move_old_mails_to_archive(dry_run: bool = True) -> None:
    """Verschiebt alle Mails von 2022 und aelter aus INBOX nach DIR_NAME."""
    mail = connect()
    try:
        mail.select("INBOX", readonly=dry_run)
        _status, data = mail.search(None, "BEFORE", "1-Jan-2023")
        msg_ids = data[0].split()

        if not msg_ids:
            print("Keine Mails von 2022 oder aelter gefunden.")
            return

        print(f"{len(msg_ids)} Mail(s) von 2022 oder aelter gefunden.")

        if dry_run:
            print("Dry-Run – keine Mails verschoben.")
            return

        id_set = b",".join(msg_ids)
        mail.copy(id_set, DIR_NAME)
        mail.store(id_set, "+FLAGS", "\\Deleted")
        mail.expunge()
        print(f"{len(msg_ids)} Mail(s) nach {DIR_NAME} verschoben.")
    finally:
        mail.logout()


if __name__ == "__main__":
    move_old_mails_to_archive(dry_run=True)