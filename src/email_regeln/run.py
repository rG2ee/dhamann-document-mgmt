"""Verschiebt Mails aus der INBOX in die passenden filter-andwendungen-Ordner."""

from __future__ import annotations

import time

from email_regeln.imap_connection import create_email_folder_in_filter_anwendungen
from email_regeln.move_to_delete import run

ZUORDNUNGEN: dict[str, list[str]] = {
    # =====================================================================
    # BESTEHENDE ORDNER (bereits in filter-andwendungen vorhanden)
    # =====================================================================
    "Folders/filter-andwendungen/persoenliche-kontakte": [ # ok
        # gmail.com
        "winniehamann@gmail.com",
        "gerrit.hendricks@gmail.com",
        "davinablank.ba@gmail.com",
        "runge.ph@gmail.com",
        "cblank.de@gmail.com",
        "jana.fischer1999@gmail.com",
        "saigonrooftopshostel@gmail.com",
        "nicokriebel95@gmail.com",
        "jannik.siems@gmail.com",
        "vikram01.jha@gmail.com",
        "ramonanieswandt@gmail.com",
        "kelseyj.harrison0@gmail.com",
        "ksmkhan7@gmail.com",
        "aleksandarfaraj@gmail.com",
        "sarahflensburg95@gmail.com",
        "dennis.hamann.dev@gmail.com",
        # protonmail.com
        "dennis.hamann@protonmail.com",
        "lars.globisch@protonmail.com",
        "danja.kluever@protonmail.com",
        # t-online.de
        "heinerhamann@t-online.de",
        # gmx.de
        "pascal.greder@gmx.de",
        "andreas.verweyen@gmx.de",
        "violeneaouinti@gmx.de",
        "va-katja.bardon@proton.me",
    ],


    "Folders/filter-andwendungen/gesundheit": [
        "naturheilpraxis-saschahoff@gmx.de",
        "villaamroseneck@gmx.de",
    ],
    "Folders/filter-andwendungen/antrophic": [
        "invoice+statements@mail.anthropic.com",
        "support+news@mail.anthropic.com",
        "support+terms@mail.anthropic.com",
        "failed-payments@mail.anthropic.com",
        "no-reply-r6ovhw3pmj5djxflrbplja@mail.anthropic.com",
        "no-reply-8nemz8hb78szuefe48mqbq@mail.anthropic.com",
        "no-reply-vw_ru07h3ag4ozbpvv2yqg@mail.anthropic.com",
        "no-reply-eko8lgacqstmrok69o1t7a@mail.anthropic.com",
        "no-reply-rrrsfdsdfq-xuwr40u2q2w@mail.anthropic.com",
        "no-reply-ylzg4voiswtrflljkmkndg@mail.anthropic.com",
        "no-reply-lgo-obp-mww5oiujy6yaoq@mail.anthropic.com",
        "no-reply-isb8faghetf7jsl7kyzhjg@mail.anthropic.com",
        "no-reply-a23yj2zy0zrmky7z3bxycq@mail.anthropic.com",
        "no-reply-bj9h9ucnmam1afmrkwqetg@mail.anthropic.com",
        "no-reply-lqwz_lkxu59191n6ixauww@mail.anthropic.com",
        "no-reply-8g8uvqvcbfn0xiqta-h6tg@mail.anthropic.com",
        "no-reply-bi4ial7u5y3vumnycg-lxw@mail.anthropic.com",
        "no-reply-jyathaulnztpg6i1llidjq@mail.anthropic.com",
        "no-reply-qgxytpxqxz_vfxufgpof0q@mail.anthropic.com",
    ],
    "Folders/filter-andwendungen/computershare": [
        "computershare online services",
    ],
    "Folders/filter-andwendungen/vorwerk": [
        "contact.de@mkt.vorwerk.com",
        "neolane.de@mkt.vorwerk.com",
        "cookidoo@mkt.vorwerk.com",
        "zufriedenheitsumfrage-thermomix@mkt.vorwerk.com",
    ],
    "Folders/filter-andwendungen/fiverr": [
        "info@research.fiverr.com",
    ],
    "Folders/filter-andwendungen/nespresso": [
        "nespresso-no-reply@versand-status.de",
    ],
    "Folders/filter-andwendungen/emmy": [
        "isa@info.emmy-sharing.de",
        "lilo@info.emmy-sharing.de",
        "emmy@info.emmy-sharing.de",
    ],
    "Folders/filter-andwendungen/tuhh": [
        "dennis.hamann@tuhh.de",
        "servicedesk@tuhh.de",
        "otrs@tuhh.de",
    ],
    "Folders/filter-andwendungen/amorelie": [
        "produktempfehlung@mailing.amorelie.de",
        "newsletter@mailing.amorelie.de",
    ],
    "Folders/filter-andwendungen/american-express": [
        "erechnung@welcome.americanexpress.com",
        "onlineservices@welcome.americanexpress.com",
    ],
    "Folders/filter-andwendungen/uber": [
        "admin@uber.com",
    ],
    "Folders/filter-andwendungen/proton": [
        "mailer-daemon@proton.me",
    ],
    "Folders/filter-andwendungen/mietverein-hamburg": [
        "infomail@news.mieterverein-hamburg.de",
        "mieterjournal@news.mieterverein-hamburg.de",
        "noreply@news.mieterverein-hamburg.de",
        "newsletter@news.mieterverein-hamburg.de",
    ],
    "Folders/filter-andwendungen/hostelworld": [
        "bookings@hostelworld.com",
        "noreply@hostelworld.com",
    ],
    "Folders/filter-andwendungen/trip.com": [
        "de_noreply@trip.com",
        "de_flight@trip.com",
    ],
    "Folders/filter-andwendungen/wise": [
        "noreply@info.wise.com",
    ],
    "Folders/filter-andwendungen/patreon": [
        "no-reply@patreon.com",
    ],
    "Folders/filter-andwendungen/hauer-naturprodukte": [
        "g.feldhusen-schwarz@hauer-naturprodukte.com",
    ],
    "Folders/filter-andwendungen/discord": [
        "notifications@discord.com",
    ],
    "Folders/filter-andwendungen/wasabi": [
        "support@wasabi.com",
    ],
    "Folders/filter-andwendungen/ikea": [
        "no.reply@order.email.ikea.com",
    ],
    "Folders/filter-andwendungen/stadt-hamburg": [
        "noreply@termine.hamburg.de",
        "erichsen@hamburg.de",
    ],
    "Folders/filter-andwendungen/ebay": [
        "ebay@ebay.com",
    ],
    "Folders/filter-andwendungen/klarna": [
        "noreply-de@klarna.de",
    ],
    "Folders/filter-andwendungen/builder-io": [
        "support@builderio.zendesk.com",
    ],
    "Folders/filter-andwendungen/moia": [
        "noreply@welcome.moia-mail.io",
    ],
    "Folders/filter-andwendungen/galaxus": [
        "noreply@notifications.galaxus.de",
    ],
    "Folders/filter-andwendungen/freelancer-agenturen/gulp": [
        "willkommen@reply.gulp.de",
        "verfuegbarkeit@reply.gulp.de",
    ],

    # =====================================================================
    # NEUE ORDNER (müssen noch angelegt werden)
    # =====================================================================
    "Folders/filter-andwendungen/stripe": [
        "support@stripe.com",
        "invoice+statements+acct_1dyefsangonnitrp@stripe.com",
        "invoice+statements+acct_1c0kgpbolzqytay9@stripe.com",
        "upcoming-invoice+acct_1ivkoplx4fybotqj@stripe.com",
        "invoice+statements+acct_1reyrsbnuncszfs9@stripe.com",
        "failed-payments+acct_1ivkoplx4fybotqj@stripe.com",
        "trial-ending+acct_1ivkoplx4fybotqj@stripe.com",
    ],
    "Folders/filter-andwendungen/ups": [
        "pkginfo@ups.com",
        "mcinfo@ups.com",
        "emailinfo@ups.com",
    ],
    "Folders/filter-andwendungen/freelancer-agenturen/nemensis": [
        "rene.schwinning@nemensis.de",
    ],
    "Folders/filter-andwendungen/freelancer-agenturen/solcom": [
        "projektpartner@solcom.de",
        "projekte@solcom.de",
        "bewerbung@solcom.de",
    ],
    "Folders/filter-andwendungen/freelancer-agenturen/redglobal": [
        "info@redglobal.com",
        "nhnguyen@redglobal.com",
        "bgerhard@redglobal.com",
        "smegrelishvili@redglobal.com",
        "dataofficer@redglobal.com",
        "zrasch@redglobal.com",
        "jdabaas@redglobal.com",
    ],
    "Folders/filter-andwendungen/12go-asia": [
        "28351394@b.12go.asia",
        "27855159@b.12go.asia",
        "11067549@b.12go.asia",
        "27855160@b.12go.asia",
        "11067550@b.12go.asia",
    ],
    "Folders/filter-andwendungen/pal-tv": [
        "info@pal-tv.de",
        "andre.stubbs@pal-tv.de",
    ],
    "Folders/filter-andwendungen/dampfdorado": [
        "bestellungen@dampfdorado.de",
    ],
    "Folders/filter-andwendungen/wolt": [
        "info@wolt.com",
    ],
    "Folders/filter-andwendungen/home24": [
        "do-not-reply@reply.em.home24.de",
        "noreply@reply.em.home24.de",
    ],
    "Folders/filter-andwendungen/bassliner": [
        "buero@bassliner.org",
        "bookings@bassliner.org",
        "buchungen@bassliner.org",
    ],
    "Folders/filter-andwendungen/skatbank": [
        "info@skatbank.de",
    ],
    "Folders/filter-andwendungen/blizzard": [
        "noreply@e.battle.net",
    ],
    "Folders/filter-andwendungen/finanzguru": [
        "dein@finanzguru.de",
    ],
    "Folders/filter-andwendungen/tivoli": [
        "info@mailing.tivoli.de",
    ],
    "Folders/filter-andwendungen/meetup": [
        "info@meetup.com",
    ],
    "Folders/filter-andwendungen/motelamiio": [
        "news@motelamiio.com",
        "hello@motelamiio.com",
    ],
    "Folders/filter-andwendungen/shippypro": [
        "no-reply@shippypro.com",
    ],
    "Folders/filter-andwendungen/mindfactory": [
        "info@mindfactory.de",
    ],
    "Folders/filter-andwendungen/swiss": [
        "flight.service@information.swiss.com",
        "travel.id@information.swiss.com",
        "booking@information.swiss.com",
    ],
    "Folders/filter-andwendungen/zara": [
        "noreply@zara.com",
    ],
    "Folders/filter-andwendungen/reddit": [
        "noreply@redditmail.com",
    ],
    "Folders/filter-andwendungen/deutsche-bahn": [
        "noreply@deutschebahn.com",
    ],
    "Folders/filter-andwendungen/thomann": [
        "kundenservice@thomann.de",
        "buchhaltung@thomann.de",
    ],
    "Folders/filter-andwendungen/etke-host": [
        "ko-fi@ko-fi.com",
    ],
    "Folders/filter-andwendungen/warburg": [
        "nicholas.ziegert@ownly.de",
    ],

    # =====================================================================
    # TO-BE-DELETED
    # =====================================================================
    "Folders/to-be-deleted": [
        "team@m.ngrok.com",
        "mailings@newsletter.zattoo.com",
        "noreply@dfinity.org",
        "comms@dfinity.org",
        "hello@duolingo.com",
        "pageupdates@facebookmail.com",
        "notification@facebookmail.com",
        "groupupdates@facebookmail.com",
        "no-reply@mail.instagram.com",
        "mail@updates.fresha.com",
    ],
}


FOLDERS_TO_BE_CREATED: list[str] = [
    "stripe",
    "ups",
    "freelancer-agenturen/nemensis",
    "freelancer-agenturen/solcom",
    "freelancer-agenturen/redglobal",
    "12go-asia",
    "pal-tv",
    "dampfdorado",
    "wolt",
    "home24",
    "bassliner",
    "skatbank",
    "blizzard",
    "finanzguru",
    "tivoli",
    "meetup",
    "motelamiio",
    "shippypro",
    "mindfactory",
    "swiss",
    "zara",
    "reddit",
    "deutsche-bahn",
    "thomann",
    # "ko-fi",
    #"ownly",
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
