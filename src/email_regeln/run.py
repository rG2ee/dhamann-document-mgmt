"""Verschiebt Mails aus der INBOX in die passenden filter-andwendungen-Ordner."""

from __future__ import annotations

import time

from email_regeln.imap_connection import create_email_folder_in_filter_anwendungen
from email_regeln.move_to_delete import run

ZUORDNUNGEN: dict[str, list[str]] = {
    # --- Bestehende Ordner, neue Adressen ---
    "Folders/filter-andwendungen/openai": [
        "noreply@email.openai.com",
    ],
    "Folders/filter-andwendungen/trade-republic": [
        "service-de@traderepublic.com",
    ],
    "Folders/filter-andwendungen/remarkable": [
        "newsletters@email.remarkable.com",
    ],
    "Folders/filter-andwendungen/bitwarden": [
        "productupdates@bitwarden.com",
    ],
    "Folders/filter-andwendungen/airbnb": [
        "no-reply@supportmessaging.airbnb.com",
    ],
    "Folders/filter-andwendungen/audible": [
        "noreply@audible.de",
    ],
    "Folders/filter-andwendungen/trip.com": [
        "de_flt_noreply@trip.com",
    ],
    "Folders/filter-andwendungen/freelancer-agenturen/soorce": [
        "daniel.frech@soorce.de",
    ],
    "Folders/filter-andwendungen/gorillas": [
        "news@newsletter.gorillasapp.com",
    ],
    "Folders/filter-andwendungen/antrophic": [
        "support@mail.anthropic.com",
    ],
    # --- Neue Ordner (siehe FOLDERS_TO_BE_CREATED) ---
    "Folders/to-be-deleted": [
        "noreply@booking-time.com",
        "support@mathpix.com",
        "admin@gearinstock.com",
        "noreply@myfritz.net",
        "noreply@hiveos.farm",
        "info@balloonapp.de",
        "info@solver.com",
        "catalyst@iohk.io",
        "info@easymeal.de",
        "reminders@facebookmail.com",
        "security@mail.instagram.com",
        "no-reply@storj.io",
        "chef@cuisine.rudirocks.com",
        "newsletter@aktuelles.eat-the-world.com",

        "info@reply.pixum.com",
        "service-de@reply.pixum.com",
        "reminders@facebookmail.com",

        "donotreply@testflow.eu",

        "info@einfach-zypern.com",
        "noreply@newsletter.austrian.com",

        "info@theaos.de",
        "mail@ifttt.com",
        "noreply@tomorrowland.com",
        "info@fitmart.de",
        "news@whitebit.com",
        "community@pinecone.io",
        "newsletter@pizzamax.de",
        "noreply@clickandboat.com",
        "noreply@pizzeria.de",
    ],
    "Folders/filter-andwendungen/google": [
        "no-reply@accounts.google.com",
        "googledev-noreply@google.com",
    ],
    "Folders/filter-andwendungen/stadt-hamburg": [
        "noreply_serviceportal-hamburg@dataport.de",
        "meinserviceportal@dataport.de",
    ],
    "Folders/filter-andwendungen/hauer-naturprodukte": [
        "shop@hauer-naturprodukte.com",
    ],
    "Folders/filter-andwendungen/orgainic": [
        "info@orgainic.com",
    ],
    "Folders/filter-andwendungen/webo-hosting": [
        "support@webo.hosting",
    ],
    "Folders/filter-andwendungen/vorwerk": [
        "kontakt@mkt.de.vorwerk.com",
    ],
    "Folders/filter-andwendungen/treatwell": [
        "noreply@treatwell.de",
    ],
    "Folders/filter-andwendungen/weird-events": [
        "tickets@weird-events.com",
    ],
    "Folders/filter-andwendungen/nymtech": [
        "contact@nymtech.net",
    ],
    "Folders/filter-andwendungen/etke-host": [
        "monitoring@etke.host",
    ],
    "Folders/filter-andwendungen/ttv-dance": [
        "admin@ttv.dance",
    ],




    "Folders/filter-andwendungen/ramona-mertens": [
        "noreply@lemniscus.de",
        "info@tisso.de",
        "info@nl.biogena.com",
    ],

    "Folders/filter-andwendungen/stakingrewards": [
        "stakingrewards@substack.com",
        "newsletter@stakingrewards.com",
    ],


    "Folders/filter-andwendungen/proton": [
        "no-reply@news.proton.me",
    ],
    "Folders/filter-andwendungen/kickstarter": [
        "no-reply@kickstarter.com",
    ],

    "Folders/filter-andwendungen/ubiquiti": [
        "account-noreply@ui.com",
    ],


    "Folders/filter-andwendungen/letsencrypt": [
        "expiry@letsencrypt.org",
    ],

    "Folders/filter-andwendungen/notion": [
        "notify@mail.notion.so",
    ],
    "Folders/filter-andwendungen/shein": [
        "noreply@sheinnotice.com",
    ],
    "Folders/filter-andwendungen/lazada": [
        "noreply@support.lazada.co.th",
    ],
    "Folders/filter-andwendungen/amd": [
        "memberservices@amd-member.com",
    ],
    "Folders/filter-andwendungen/ebay": [
        "ebay@reply.ebay.de",
    ],






    "Folders/filter-andwendungen/boom-festival": [
        "info@community.boomfestival.org",
    ],
    "Folders/filter-andwendungen/doppelgaenger": [
        "pip@mail.doppelgaenger.io",
    ],
    "Folders/filter-andwendungen/hostelworld": [
        "noreply@email.hostelworld.com",
        "no.reply@m.email.hostelworld.com",
    ],
    "Folders/filter-andwendungen/grab": [
        "no-reply@grab.com",
    ],

    "Folders/filter-andwendungen/free-now": [
        "no-reply@my.free-now.com",
    ],
    "Folders/filter-andwendungen/rewe": [
        "reweshop@mailing.rewe.de",
    ],
    "Folders/filter-andwendungen/alternate": [
        "info@alternate.de",
    ],
    "Folders/filter-andwendungen/samedi": [
        "no-reply@mail.samedi.de",
    ],
    "Folders/filter-andwendungen/miles-and-more": [
        "mail@mailing.milesandmore.com",
    ],
    "Folders/filter-andwendungen/psy-spirits": [
        "info@psy-spirits.de",
    ],
    "Folders/filter-andwendungen/newsletter": [
        "newsletter@mkt.flytap.com",
    ],


    "Folders/filter-andwendungen/vattenfall": [
        "onlineservice@vattenfall.de",
    ],


    "Folders/filter-andwendungen/doodle": [
        "mailer@doodle.com",
    ],
    "Folders/filter-andwendungen/chessly": [
        "team@chessly.com",
    ],
    "Folders/filter-andwendungen/discord": [
        "noreply@discord.com",
    ],
    "Folders/filter-andwendungen/refurbed": [
        "peter@m.refurbed.com",
    ],
    "Folders/filter-andwendungen/buymeacoffee": [
        "hello@buymeacoffee.com",
    ],


    "Folders/filter-andwendungen/hamburg-open-atp": [
        "ticketing@hamburgopenatp500.com",
    ],
    "Folders/filter-andwendungen/debeka": [
        "noreply-newsletter@info.debeka.de",
    ],
    "Folders/filter-andwendungen/emirates": [
        "do-not-reply@emirates.email",
    ],
    "Folders/filter-andwendungen/alibaba": [
        "alibaba@service.alibaba.com",
    ],
    "Folders/filter-andwendungen/medium": [
        "noreply@medium.com",
    ],
    "Folders/filter-andwendungen/nespresso": [
        "identification@nespresso.com",
    ],
}

FOLDERS_TO_BE_CREATED: list[str] = [
    #"booking-time",
    "google",
    "stadt-hamburg",
    #"mathpix",
    "hauer-naturprodukte",
    #"gearinstock",
    "orgainic",
    "webo-hosting",
    "vorwerk",
    "treatwell",
    "weird-events",
    "nymtech",
    #"myfritz",
    "etke-host",
    "ttv-dance",
    #"hiveos",
    #"balloonapp",
    # "solver",
    "ramona-mertens",
    #"iohk",
    #"easymeal",
    #"facebook",
    "stakingrewards",
   # "instagram",
  #  "storj",
    "proton",
    "kickstarter",
   # "rudirocks",
   # "eat-the-world",
    "ubiquiti",
   # "pixum",



   # "testflow",
   # "austrian-airlines",
   # "einfach-zypern",
   # "tisso",
   # "theaos",
   # "ifttt",
    #"biogena",
    #"letsencrypt",
    #"tomorrowland",
    "notion",
    "shein",
    "lazada",
    "amd",
    "ebay",
    #"fitmart",

    "boom-festival",
    "doppelgaenger",
    "hostelworld",
    "grab",
    # "whitebit",
    "free-now",
    "rewe",
    "alternate",
    "samedi",
    "miles-and-more",
    "psy-spirits",


    #"flytap",
    "vattenfall",
    #"pinecone",
    #"pizzamax",


    "doodle",
    "chessly",
    "discord",
    "refurbed",
    "buymeacoffee",
    # "pizzeria-de",
    # "clickandboat",
    "hamburg-open-atp",
    "debeka",
    "emirates",
    "alibaba",
    "medium",
    "nespresso",
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

