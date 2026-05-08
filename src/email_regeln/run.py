"""Verschiebt Mails aus der INBOX in die passenden filter-andwendungen-Ordner."""

from __future__ import annotations

import time

from email_regeln.imap_connection import create_email_folder_in_filter_anwendungen
from email_regeln.move_to_delete import run

ZUORDNUNGEN: dict[str, list[str]] = {
}

FOLDERS_TO_BE_CREATED: list[str] = [

]


if __name__ == "__main__":
    """
    for folder in FOLDERS_TO_BE_CREATED:
        create_email_folder_in_filter_anwendungen(folder)
        time.sleep(1)
    """


    for ordner, absender in ZUORDNUNGEN.items():
        print(f"\n--- Verschiebe nach: {ordner} ---")
        run(absender, target_folder=ordner, dry_run=False)
