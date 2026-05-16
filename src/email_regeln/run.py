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
    # TO-BE-DELETED
    # =====================================================================




    "Folders/to-be-deleted": [

    # spam:
        "6193922396763833211@t-online.de",
        "a.gaertner@t-online.de",

        "a.kostyra@t-online.de",
        "abaz.imeri@t-online.de",
        "andreasstiedl@t-online.de",

        "ansgarfoerster@t-online.de",


        "armin.jacob@t-online.de",
        "asd3gssad3gg@t-online.de",
        "axel.darup@t-online.de",
        "b.r.waldvogel@t-online.de",
        "brit_martin@t-online.de",
        "charlotte.michael@t-online.de",
        "eichin.laempe@t-online.de",
        "famstopp@t-online.de",
        "fritsch.t@t-online.de",
        "geier.rheindiebach@t-online.de",
        "georg.wissmeier@t-online.de",
        "giese.b@t-online.de",
        "gsd32fdfdsf@t-online.de",
        "haas-r@t-online.de",
        "heinz.stickel@t-online.de",
        "heizpi@t-online.de",
        "hldoths@t-online.de",
        "info-tele-094274@t-online.de",
        "info-tele-39922@t-online.de",
        "info-tele-5744572@t-online.de",
        "info-tele-6536367@t-online.de",
        "infotele9281291@t-online.de",
        "ing-kunde.89421176@t-online.de",
        "khummel@t-online.de",
        "lang-alfons@t-online.de",
        "metawi@t-online.de",
        "nicolarieger@t-online.de",
        "paket-12115927@t-online.de",
        "r.heravi@t-online.de",
        "robert.polifka@t-online.de",
        "rreiss@t-online.de",
        "sad4gr@t-online.de",
        "schwarz-detlef@t-online.de",
        "singintapas@t-online.de",
        "stiebel.ulrich@t-online.de",
        "ticket-36999470@t-online.de",
        "uwe.hafer@t-online.de",
        "vanessamaurer84549@t-online.de",
        "wahner.oberbuchen@t-online.de",
        "windmuehle1@t-online.de",
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
    #create_dirs()
    move_emails(dry_run=False)
