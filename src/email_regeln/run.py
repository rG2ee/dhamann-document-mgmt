"""Verschiebt Mails aus der INBOX in die passenden filter-andwendungen-Ordner."""

from __future__ import annotations

import time

from email_regeln.imap_connection import create_email_folder_in_filter_anwendungen
from email_regeln.move_to_delete import run

ZUORDNUNGEN: dict[str, list[str]] = {
    # =====================================================================
    # BESTEHENDE ORDNER (bereits in filter-andwendungen vorhanden)
    # =====================================================================

    # =====================================================================
    # NEUE ORDNER
    # =====================================================================

    # =====================================================================
    # TO-BE-DELETED
    # =====================================================================
    "Folders/to-be-deleted": [
    ],
}


FOLDERS_TO_BE_CREATED: list[str] = [
]


def create_dirs():
    for folder in FOLDERS_TO_BE_CREATED:
        create_email_folder_in_filter_anwendungen(folder)
        time.sleep(1)


def move_emails(dry_run: bool):
    for ordner, absender in ZUORDNUNGEN.items():
        print(f"\n--- Verschiebe nach: {ordner} ---")
        run(absender, target_folder=ordner, dry_run=dry_run)


if __name__ == "__main__":
    create_dirs()
    move_emails(dry_run=False)
