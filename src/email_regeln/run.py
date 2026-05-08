"""Verschiebt Mails aus der INBOX in die passenden filter-andwendungen-Ordner."""

from __future__ import annotations

import time

from email_regeln.imap_connection import create_email_folder_in_filter_anwendungen
from email_regeln.move_to_delete import run

ZUORDNUNGEN: dict[str, list[str]] = {
    # --- Bestehende Ordner in filter-andwendungen ---

    "Folders/filter-andwendungen/etke-host": [
        "aine@etke.cc", # ok
        "billing@b.etesync.com",  # ok
        "support-mailer@b.etesync.com",  # ok
        "failed-payments+acct_1apfzwjetinljgaa@stripe.com",  # ok
    ],
    "Folders/filter-andwendungen/amd": [
        "amdcommunity.mailer@amd.com", # ok
        "noreply@shop.amd.com", # ok
        "orderconfirmation@digitalriver.com",  # ok
    ],
    "Folders/filter-andwendungen/vattenfall": [
        "angebot@vattenfall.de", # ok
    ],
    "Folders/filter-andwendungen/proton": [  # ok
        "contact@protonmail.com",
        "usersfeedback@protonmail.com",
        "no-reply@app.protonmail.com",
        "no-reply@app.protonvpn.com",
        "no-reply@news.protonmail.com",
        "no-reply@notify.protonmail.com",
        "no-reply@notify.protonvpn.com",
        "mailer-daemon@protonmail.com",
    ],
    "Folders/filter-andwendungen/remarkable": [  # ok
        "team@mail.remarkable.com",
        "team@remarkable.com",
        "donotreply@remarkable.com",
    ],
    "Folders/filter-andwendungen/qubes-os": [ # ok
        "team@research.qubes-os.org",
        "no-reply@qubes-os.opencollective.com",
    ],
    "Folders/filter-andwendungen/doodle": [ # ok
        "time@doodle.com",
    ],
    "Folders/filter-andwendungen/miles-car-sharing": [  # ok
        "sophia@news.miles-mobility.com",
    ],
    "Folders/filter-andwendungen/barclays": [ # ok
        "service@email.barclaycard.de",
        "info@rueckzahlung.barclays.de",
    ],
    "Folders/filter-andwendungen/dhl-post": [  # ok
        "paket@dhl.de",
        "noreply@dhl.com",
        "noreply.kundenkonto@dhl.de",
    ],
    "Folders/filter-andwendungen/ionos": [ # ok
        "noreply@ionos.com",
    ],
    "Folders/filter-andwendungen/stakingrewards": [ # ok
        "noreply@stakingrewards.com",
    ],
    "Folders/filter-andwendungen/interactive-brokers": [ # ok
        "interactive brokers client services",
    ],
    "Folders/filter-andwendungen/dpd": [ # ok
        "empfangen@dpd.de",
        "info@paket.dpd.de",
    ],
    "Folders/filter-andwendungen/gorillas": [ # ok
        "feedback@gorillasapp.com",
        "feedback@mail.gorillasapp.es",
    ],
    "Folders/filter-andwendungen/flink": [ # ok
        "funda.zurnaci@flink-44a615fa4e6a.intercom-mail.com",
        "hello@goflink.com",
        "jonah@flink-44a615fa4e6a.intercom-mail.com",
        "operator@flink-44a615fa4e6a.intercom-mail.com",
    ],
    "Folders/filter-andwendungen/samedi": [  # ok
        "info@mail.samedi.de",
    ],
    "Folders/filter-andwendungen/webo-hosting": [ # ok
        "info@webo.hosting",
    ],
    "Folders/filter-andwendungen/debeka": [ # ok
        "kundenservice@debeka.de",
        "noreply-newsletter@debeka.de",
    ],
    "Folders/filter-andwendungen/medium": [ # ok
        "members@medium.com",
    ],
    "Folders/filter-andwendungen/vodafone": [ # ok
        "nicht.antworten@kundenservice.vodafone.com",
    ],
    "Folders/filter-andwendungen/fiverr": [ # ok
        "no-reply@fiverr.com",
    ],
    "Folders/filter-andwendungen/eversports": [ # ok
        "no-reply@priority-send.eversports.com",
    ],
    "Folders/filter-andwendungen/github": [ # ok
        "noreply@github.com",
    ],
    "Folders/filter-andwendungen/discord": [ # ok
        "noreply@discordapp.com",
    ],
    "Folders/filter-andwendungen/buymeacoffee": [ # ok
        "notifications@buymeacoffee.com",
    ],
    "Folders/filter-andwendungen/google": [  # ok
        "no-reply@youtube.com",
        "noreply-utos@google.com",
    ],
    "Folders/filter-andwendungen/stadt-hamburg": [  # ok
        "info@stadtradhamburg.de",
    ],
    "Folders/filter-andwendungen/alternate": [ # ok
        "studio@djmerlin.com",
        "kundenservice@spb-garant.de",
    ],
    "Folders/filter-andwendungen/freelancer-agenturen": [
    ],
    "Folders/filter-andwendungen/ramona-mertens": [ # ok
        "uwe@harste.org",
    ],

    # --- Neue Ordner in filter-andwendungen ---

    "Folders/filter-andwendungen/computershare": [ # ok
        "computershare.npcegbcecmgekcdecd@cpucommunications.com",
        "computershare.npcegbjemjgecdjejd@cpucommunications.com",
        "computershare.npcegdgemcjecdlebl@cpucommunications.com",
        "computershare.npcegdmeblcebhfemg@cpucommunications.com",
        "computershare.npceggkejdbedfgedf@cpucommunications.com",
        "message.npcefmledbcedhmecg@cpucommunications.com",
        "message.npcegbbemhfegllejg@cpucommunications.com",
        "message.npcegbbemhfehbdedd@cpucommunications.com",
        "message.npcegbbemhgecfbekl@cpucommunications.com",
        "message.npcegdmefddedfkejh@cpucommunications.com",
    ],
    "Folders/filter-andwendungen/onvista": [ # ok
        "service@onvista-bank.de",
    ],
    "Folders/filter-andwendungen/warburg": [ # ok
        "sburgsdorff@mmwarburg.com",
        "rbudinsky@mmwarburg.com",
        "thomas.weinmann@astorius.net",
        "dennis.hamann@ownly.de",
        "jan.steinke@ownly.de",
        "noreply@astorius.net",
    ],
    "Folders/filter-andwendungen/flatex": [ # ok
        "info@flatex.de",
        "vbs22@bafin.de",
    ],
    "Folders/filter-andwendungen/hanseatic-physio": [ # ok
        "dkluge@hanseatic-physio.de",
    ],
    "Folders/filter-andwendungen/finanzamt-hamburg": [ # ok
        "automatischeantwort@finanzamt.hamburg.de",
    ],
    "Folders/filter-andwendungen/gesundheit": [ # ok
        "do-not-reply@mgs-eportal.de",
        "bremer-rheumatologie@hamburg.de",
        "info@hnoamrothenbaum.de",
        "mail@argon-orthopaedie.de",
    ],
    "Folders/filter-andwendungen/galaxus": [ # ok
        "coupons@galaxus.de",
        "galaxus@galaxus.de",
        "galaxus@security.galaxus.de",
    ],
    "Folders/filter-andwendungen/notebooksbilliger": [ # ok
        "team@notebooksbilliger.de",
        "service@notebooksbilliger.de",
    ],
    "Folders/filter-andwendungen/pricezilla": [ # ok
        "pricezilla@versand-status.de",
    ],
    "Folders/filter-andwendungen/roborock": [ # ok
        "noreply@notice-eu.roborock.com",
    ],
    "Folders/filter-andwendungen/ikea": [ # ok
        "do.not.reply@ikea.com",
        "noreply@ikea.com",
    ],
    "Folders/filter-andwendungen/etsy": [ # ok
        "emails@mail.etsy.com",
        "noreply@etsy.com",
        "noreply@mail.etsy.com",
    ],
    "Folders/filter-andwendungen/physiosupplies": [ # ok
        "info@physiosupplies.de",
    ],
    "Folders/filter-andwendungen/amorelie": [ # ok
        "kundenservice@amorelie.de",
    ],
    "Folders/filter-andwendungen/allianz": [ # ok
        "sepa-awpde@allianz.com",
        "service-reise@allianz.com",
    ],
    "Folders/filter-andwendungen/1password": [ # ok
        "hello@1password.com",
    ],
    "Folders/filter-andwendungen/coinbase": [ # ok
        "no-reply@coinbase.com",
        "info@cb.mail.coinbase.com",
    ],
    "Folders/filter-andwendungen/transparenzregister": [ # ok
        "no-reply@transparenzregister.de",
    ],
    "Folders/filter-andwendungen/schufa": [ # ok
        "meineschufa@schufa.de",
        "no-reply-pk@schufa.de",
    ],
    "Folders/filter-andwendungen/persoenliche-kontakte": [ # ok
        "andrearuff@gmx.de",
        "danja.kluever@gruene-hu.de",
        "ulf.kluever@gruene-hu.de",
        "ulf.kluever@gruene-se-kv.de",
        "ulf.kluever@protonmail.com",
        "safli@web.de",
        "pascal_dominik.greder@smail.th-koeln.de",
        "miguelchapero@icloud.com",
        "msb@atelier-bachert.de",
        "neugebauer_katharina@ymail.com",
    ],
    "Folders/filter-andwendungen/mietverein-hamburg": [  # ok
        "beratung@mieterverein-hamburg.de",
        "noreply_mia@mieterverein-hamburg.de",
    ],
    "Folders/filter-andwendungen/1a-visum": [ # ok
        "eta@1avisum.de",
        "info@1avisum.de",
        "immigrationofficegovernmentcomplexchaengwattanard@imm1division.onmicrosoft.com",
    ],
    "Folders/filter-andwendungen/deltakonnect": [ # ok
        "info@deltakonnect.de",
    ],
    "Folders/filter-andwendungen/dkb": [ # ok
        "info@dkb.de",
    ],
    "Folders/filter-andwendungen/tuhh": [ # ok
        "empfang@trude-hh.de",
    ],
    "Folders/filter-andwendungen/activatio": [ # ok
        "nm@activatio.de",
    ],
    "Folders/filter-andwendungen/agoda": [ # ok
        "no-reply@agoda-email.com",
        "no-reply@security.agoda.com",
        "no-reply@sg.sgt.agoda-email.com",
    ],
    "Folders/filter-andwendungen/soundcloud": [ # ok
        "no-reply@announcements.soundcloud.com",
    ],
    "Folders/filter-andwendungen/jameda": [ # ok
        "no-reply@jameda.de",
    ],
    "Folders/filter-andwendungen/cubicl": [ # ok
        "dennis@cubicl.de",
        "pia-info@pleugerindustries.com",
        "inez@cubicl.de",
    ],
    "Folders/filter-andwendungen/steuer": [ # ok
        "svencarstens@carstens-stb.de",
    ],

    # --- Sonstige bestehende Ordner ---

    "Folders/computer": [
    ],

    # --- to-be-deleted ---

    "Folders/to-be-deleted": [
        "help@paddle.com",
        "hoheluft@pokehamburg.de",
        "huami@email.huami.com",
        "mifit-feedback-auto@email.huami.com",
        "official@amazfit.com",
        "noreply@buhl.de",
    ],
}


FOLDERS_TO_BE_CREATED: list[str] = [
    "1a-visum",
    "1password",
    "activatio",
    "agoda",
    "allianz",
    "amorelie",
    "coinbase",
    "computershare",
    "cubicl",
    "deltakonnect",
    "dkb",
    "etsy",
    "finanzamt-hamburg",
    "flatex",
    "galaxus",
    "gesundheit",
    "hanseatic-physio",
    "ikea",
    "jameda",
    "mietverein-hamburg",
    "notebooksbilliger",
    "onvista",
    "persoenliche-kontakte",
    "physiosupplies",
    "pricezilla",
    "roborock",
    "schufa",
    "soundcloud",
    "steuer",
    "transparenzregister",
    "tuhh",
    "warburg",
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
    #move_emails(dry_run=False)
