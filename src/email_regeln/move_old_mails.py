"""Verschiebt alle Mails von 2022 und aelter aus der INBOX in einen Archiv-Ordner."""

from __future__ import annotations

from email_regeln.imap_connection import connect
from email_regeln.move_to_delete import (
    PROTECTED_SOURCE_FOLDERS,
    _move_messages,
    own_addresses,
)

DIR_NAME = "Folders/filter-andwendungen/2022_and_older"


def move_old_mails_to_archive(
    dry_run: bool = True,
    *,
    folder: str = "INBOX",
    target: str = DIR_NAME,
    protect_own: bool = True,
) -> None:
    """Verschiebt alle Mails von 2022 und aelter aus *folder* nach *target*.

    Mit protect_own bleiben eigene Mails (gesendete, Entwuerfe, Notizen an sich
    selbst) unangetastet.
    """
    if folder in PROTECTED_SOURCE_FOLDERS:
        raise ValueError(f"{folder} ist als Quellordner gesperrt.")

    mail = connect()
    try:
        quoted = f'"{folder}"' if " " in folder else folder
        mail.select(quoted, readonly=dry_run)

        criteria = ["BEFORE", "1-Jan-2023"]
        if protect_own:
            for own in own_addresses():
                criteria += ["NOT", "FROM", f'"{own}"']

        _status, data = mail.uid("SEARCH", None, *criteria)
        uids = data[0].split() if data and data[0] else []

        if not uids:
            print("Keine Mails von 2022 oder aelter gefunden.")
            return

        print(f"{len(uids)} Mail(s) von 2022 oder aelter gefunden.")

        if dry_run:
            print("Dry-Run – keine Mails verschoben.")
            return

        moved = _move_messages(mail, uids, target)
        print(f"{moved} Mail(s) nach {target} verschoben.")
    finally:
        mail.logout()


if __name__ == "__main__":
    move_old_mails_to_archive(dry_run=True)
