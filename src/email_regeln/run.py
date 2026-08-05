"""Verschiebt Mails aus der INBOX in die passenden filter-andwendungen-Ordner."""

from __future__ import annotations

import time

from email_regeln.imap_connection import connect, create_email_folder_in_filter_anwendungen

from email_regeln.move_to_delete import own_address, run, validate_absender

"""
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
"""

def move_emails(dry_run: bool, folder: str = "INBOX"):
    mode = "DRY RUN" if dry_run else "LIVE"
    print(f"=== {mode} === Quelle: {folder}\n")

    # Alle Zuordnungen vorab pruefen, damit ein fehlerhafter Suchbegriff den Lauf
    # nicht erst zur Haelfte abbricht.
    for ordner, absender in ZUORDNUNGEN.items():
        validate_absender(absender, target_folder=ordner)

    if folder == "All Mail":
        print(
            "Hinweis: 'All Mail' enthaelt auch Sent, Drafts, Archive und Trash.\n"
            f"Mails mit '{own_address()}' im From-Header werden deshalb "
            "grundsaetzlich uebersprungen.\n"
        )

    print("Verbinde mit Protonmail Bridge …")
    mail = connect()

    try:
        grand_total = 0
        for ordner, absender in ZUORDNUNGEN.items():
            count = run(absender, target_folder=ordner, folder=folder, dry_run=dry_run, mail=mail)
            if count:
                label = "gefunden" if dry_run else "verschoben"
                print(f"  → {ordner}: {count} Mail(s) {label}")
            else:
                print(f"  → {ordner}: –")
            print("\n")
            grand_total += count

        print(f"\nGesamt: {grand_total} Mail(s)")
        if dry_run:
            print("Dry-Run abgeschlossen. Mit dry_run=False ausfuehren zum Verschieben.")
        else:
            print("Fertig.")
    finally:
        mail.logout()

from email_regeln.bereits_ausgefuerht_und_spaeter_als_regel_hinterlegen import ZUORDNUNGEN13 as ZUORDNUNGEN

if __name__ == "__main__":
    # create_dirs()

    move_emails(dry_run=True, folder="All Mail")
