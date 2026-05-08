"""Verschiebt Mails aus der INBOX in die passenden filter-andwendungen-Ordner."""

from __future__ import annotations

import time

from email_regeln.imap_connection import create_email_folder_in_filter_anwendungen
from email_regeln.move_to_delete import run

ZUORDNUNGEN: dict[str, list[str]] = {
    # --- Bestehende Ordner ---
    "Folders/filter-andwendungen/deltakonnect": [
        "dennis.hamann@deltakonnect.de",
    ],
    "Folders/filter-andwendungen/ramona-mertens": [
        "info@ramona-mertens.com",
    ],
    "Folders/filter-andwendungen/booking.com": [
        "noreply-iam@booking.com",
        "noreply-payments@booking.com",
        "customer.service@booking.com",
        "noreply.taxi@booking.com",
    ],
    "Folders/filter-andwendungen/chessly": [
        "alert@chess.com",
        "account@chess.com",
        "hello@chess.com",
        "receipt@chess.com",
    ],
    "Folders/filter-andwendungen/antrophic": [
        "team@email.anthropic.com",
        "notice@email.anthropic.com",
        "team@email2.anthropic.com",
    ],
    "Folders/filter-andwendungen/google": [
        "noreply@google.com",
        "meetings-noreply@google.com",
        "cloudplatform-noreply@google.com",
        "workspace-noreply@google.com",
        "googledevelopers-noreply@google.com",
        "drive-shares-dm-noreply@google.com",
        "forwarding-noreply@google.com",
        "sanjaalcu@google.com",
    ],
    "Folders/filter-andwendungen/debeka": [
        "sabine.goertz@debeka.de",
        "felix.wagner@debeka.de",
        "mitgliederinformation@info.debeka.de",
        "newsletter@info.debeka.de",
        "noreply-debeka-gesundheit@info.debeka.de",
        "noreply-gesundheitsapp@info.debeka.de",
        "no-reply-debeka-gesundheit@app.debeka.de",
    ],
    "Folders/filter-andwendungen/airbnb": [
        "discover@airbnb.com",
        "noreply@airbnb.com",
        "reply@email-support.airbnb.com",
    ],
    "Folders/filter-andwendungen/boom-festival": [
        "noreply@boomfestival.org",
        "info@boomfestival.org",
    ],
    "Folders/filter-andwendungen/eventim": [
        "news@service.eventim.de",
        "kundenservice@service.eventim.de",
        "info@service.eventim.de",
        "ticketnews@service.eventim.de",
        "bestellstatus@eventim.de",
        "registrierung@eventim.de",
        "kundenservice-hamburgopenatp500@eventim.de",
    ],
    "Folders/filter-andwendungen/etke-host": [
        "scheduler@etke.host",
        "support@etke.host",
        "goodbye@etke.host",
    ],
    "Folders/filter-andwendungen/freelancer-agenturen/soorce": [
        "felix.martin@soorce.de",
        "ayseguel.pinarbas@soorce.de",
        "andre.schreiner@soorce.de",
        "lisa-marie.blumenschein@soorce.de",
        "damjar.namin@soorce.de",
    ],
    "Folders/filter-andwendungen/coinbase": [
        "info@mail.coinbase.com",
        "no-reply@info.coinbase.com",
    ],
    "Folders/filter-andwendungen/alibaba": [
        "feedback@service.alibaba.com",
        "discover@service.alibaba.com",
        "marketing@service.alibaba.com",
        "buyer@service.alibaba.com",
        "globalsupplier@service.alibaba.com",
        "vip@service.alibaba.com",
        "alisourcepro@service.alibaba.com",
        "alibaba@email.alibaba.com",
        "buyer_01@email.alibaba.com",
        "promotion@email.alibaba.com",
        "promotion@member.alibaba.com",
        "promotion_01@member.alibaba.com",
        "member@notice.alibaba.com",
        "service@notice.alibaba.com",
        "promotion@buynotice.alibaba.com",
    ],
    "Folders/filter-andwendungen/jameda": [
        "noreply@jameda.de",
    ],
    "Folders/filter-andwendungen/vattenfall": [
        "ihre-meinung@vattenfall.de",
        "noreply-sales@vattenfall.de",
    ],
    "Folders/filter-andwendungen/flatex": [
        "noreply@eventmail.flatex.de",
        "news@reply.flatex.de",
        "mailing@rply.flatex.de",
    ],
    "Folders/filter-andwendungen/orgainic": [
        "support@orgainic.com",
    ],
    "Folders/filter-andwendungen/soundcloud": [
        "alerts@notifications.soundcloud.com",
        "no-reply@login.soundcloud.com",
        "support@support.soundcloud.com",
    ],
    "Folders/filter-andwendungen/agoda": [
        "no-reply@agoda.com",
    ],
    "Folders/filter-andwendungen/nymtech": [
        "comms@nymtech.net",
        "jessica@nymtech.net",
    ],
    "Folders/filter-andwendungen/miles-and-more": [
        "newsletter@mailing.milesandmore.com",
        "travel.id@information.milesandmore.com",
    ],
    "Folders/filter-andwendungen/ikea": [
        "do-not-reply@ikea.com",
        "no.reply@ikea.com",
        "information@info.email.ikea.com",
        "information@cm.order.email.ikea.com",
    ],
    # --- Neue Ordner ---
    "Folders/filter-andwendungen/gintech": [
        "marcel.v@gintech.io",
    ],
    "Folders/filter-andwendungen/shbb-steuerberater": [
        "info@gluecksburg.shbb.de",
        "jkortum@gluecksburg.shbb.de",
    ],
    "Folders/filter-andwendungen/builder-io": [
        "hello@builder.io",
        "customers@builder.io",
        "help@builder.io",
        "product@builder.io",
        "info@builder.io",
    ],
    "Folders/filter-andwendungen/xceed": [
        "clara@xceed.me",
        "tickets@xceed.me",
        "info@xceed.me",
        "info@news.xceed.me",
    ],
    "Folders/filter-andwendungen/gesundheit": [
        "info@neurologie-neuer-wall.de",
    ],

    "Folders/filter-andwendungen/cubicl": [
        "christian.blank@lemonade-research.de",
    ],

    "Folders/filter-andwendungen/freelancer-agenturen/hays": [
        "gdpr@email.hays.com",
        "tribeworks@email.hays.com",
        "hays-customer-voice@email.hays.com",
        "noreply-hays-team@email.hays.com",
        "community@email.hays.com",
        "ekaterina.boese@hays.de",
        "melanie.eisen@hays.de",
        "cigdem.koese@hays.de",
        "lucas.galbierz@hays.de",
        "tobias.pollmeier@hays.de",
        "service@hays.de",
    ],
    "Folders/filter-andwendungen/supabase": [
        "ant.wilson@supabase.com",
        "welcome@supabase.com",
        "noreply@supabase.com",
        "ant@supabase.com",
    ],
    "Folders/filter-andwendungen/smartflow-consulting": [
        "leonard.zimmermann@smartflow-consulting.com",
        "marina.krause@smartflow-consulting.com",
    ],

    "Folders/filter-andwendungen/fem-ai": [
        "alexandra.wudel@fem-ai.com",
        "ali.guelerman@fem-ai.com",
    ],


    "Folders/filter-andwendungen/opodo": [
        "de@e.opodo.com",
    ],

    "Folders/filter-andwendungen/selber-lagern": [
        "info@selber-lagern.de",
    ],
    "Folders/filter-andwendungen/figma": [
        "support@figma.com",
        "announcements@figma.com",
    ],
    "Folders/filter-andwendungen/mediamarkt": [
        "onlineshop@mediamarkt.de",
        "info@mail.my.mediamarkt.de",
        "noreply@mediamarkt.de",
    ],
    # --- to-be-deleted ---
    "Folders/to-be-deleted": [
        "chelsea.c@ifttt.com",
        "chelsea@ifttt.com",
        "support@pinecone.io",
        "info@pinecone.io",
        "alerts@pinecone.io",
        "contact@hungry4.io",
        "info@crissbellini.com",

        "news@mail.yfood.eu",
        "info@mail.yfood.eu",
        "no-reply@yfood.eu",
        "info@yfood.eu",
        "dave@urvin.finance",
    ],
}


FOLDERS_TO_BE_CREATED: list[str] = [
    "gintech",
    # "urvin-finance",
    "shbb-steuerberater",
    "builder-io",
    "xceed",
    # "pinecone",
    "lemonade-research",
    # "ifttt",
    # "hays",
    "supabase",
    "smartflow-consulting",
    # "hungry4",
    "fem-ai",
    # "crissbellini",
    "opodo",
    # "yfood",
    "selber-lagern",
    "figma",
    "mediamarkt",
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
