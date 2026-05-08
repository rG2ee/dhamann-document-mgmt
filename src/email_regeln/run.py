"""Verschiebt Mails aus der INBOX in die passenden filter-andwendungen-Ordner."""

from __future__ import annotations

import time

from email_regeln.imap_connection import create_email_folder_in_filter_anwendungen
from email_regeln.move_to_delete import run

ZUORDNUNGEN: dict[str, list[str]] = {
    # --- Bestehende Ordner ---
    # Folders/filter-andwendungen/...
    "Folders/filter-andwendungen/gmail.com": [
        "winniehamann@gmail.com", # -> persoenliche-kontakte
        "gerrit.hendricks@gmail.com", # -> persoenliche-kontakte
        "davinablank.ba@gmail.com", # -> persoenliche-kontakte
        "runge.ph@gmail.com", # -> persoenliche-kontakte
        "cblank.de@gmail.com", # -> persoenliche-kontakte
        "jana.fischer1999@gmail.com", # -persoenliche-kontakte
        "saigonrooftopshostel@gmail.com", # -> persoenliche-kontakte
        "nicokriebel95@gmail.com", # -> persoenliche-kontakte
        "jannik.siems@gmail.com",  # -> persoenliche-kontakte
        "vikram01.jha@gmail.com",  # -> persoenliche-kontakte
        "ramonanieswandt@gmail.com",  # -> persoenliche-kontakte
        "kelseyj.harrison0@gmail.com",  # -> persoenliche-kontakte
        "ksmkhan7@gmail.com",  # -> persoenliche-kontakte
        "aleksandarfaraj@gmail.com",  # -> persoenliche-kontakte
        "sarahflensburg95@gmail.com",  # -> persoenliche-kontakte
        "dennis.hamann.dev@gmail.com",  # -> persoenliche-kontakte
    ],
    "Folders/filter-andwendungen/protonmail.com": [
        "dennis.hamann@protonmail.com",  # -> persoenliche-kontakte
        "lars.globisch@protonmail.com",  # -> persoenliche-kontakte
        "danja.kluever@protonmail.com",  # -> persoenliche-kontakte
    ],
    "Folders/filter-andwendungen/t-online.de": [
        "heinerhamann@t-online.de",  # -> persoenliche-kontakte


        "singintapas@t-online.de",
        "vanessamaurer84549@t-online.de",
        "geier.rheindiebach@t-online.de",
        "a.gaertner@t-online.de",
        "heinz.stickel@t-online.de",
        "b.r.waldvogel@t-online.de",
        "sad4gr@t-online.de",
        "haas-r@t-online.de",
        "giese.b@t-online.de",
        "asd3gssad3gg@t-online.de",
        "heizpi@t-online.de",
        "gsd32fdfdsf@t-online.de",
        "schwarz-detlef@t-online.de",
        "r.heravi@t-online.de",
        "rreiss@t-online.de",
        "eichin.laempe@t-online.de",
        "abaz.imeri@t-online.de",
        "andreasstiedl@t-online.de",
        "uwe.hafer@t-online.de",
        "axel.darup@t-online.de",
        "6193922396763833211@t-online.de",
        "windmuehle1@t-online.de",
        "brit_martin@t-online.de",
        "khummel@t-online.de",
        "metawi@t-online.de",
        "ticket-36999470@t-online.de",
        "paket-12115927@t-online.de",
        "ing-kunde.89421176@t-online.de",
        "charlotte.michael@t-online.de",
        "ansgarfoerster@t-online.de",
        "hldoths@t-online.de",
        "fritsch.t@t-online.de",
        "wahner.oberbuchen@t-online.de",
        "armin.jacob@t-online.de",
        "infotele9281291@t-online.de",
        "a.kostyra@t-online.de",
        "nicolarieger@t-online.de",
        "famstopp@t-online.de",
        "lang-alfons@t-online.de",
        "robert.polifka@t-online.de",
        "info-tele-094274@t-online.de",
        "info-tele-5744572@t-online.de",
        "info-tele-6536367@t-online.de",
        "info-tele-39922@t-online.de",
        "stiebel.ulrich@t-online.de",
        "georg.wissmeier@t-online.de",
    ],
    "Folders/filter-andwendungen/stripe.com": [
        "support@stripe.com",
        "invoice+statements+acct_1dyefsangonnitrp@stripe.com",
        "invoice+statements+acct_1c0kgpbolzqytay9@stripe.com",
        "upcoming-invoice+acct_1ivkoplx4fybotqj@stripe.com",
        "invoice+statements+acct_1reyrsbnuncszfs9@stripe.com",
        "failed-payments+acct_1ivkoplx4fybotqj@stripe.com",
        "trial-ending+acct_1ivkoplx4fybotqj@stripe.com",
    ],
    "Folders/filter-andwendungen/mail.anthropic.com": [
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
    "Folders/filter-andwendungen/gmx.de": [
        "naturheilpraxis-saschahoff@gmx.de",  # -> gesundheit
        "pascal.greder@gmx.de",  # -> persoenliche-kontakte
        "andreas.verweyen@gmx.de", # -> persoenliche-kontakte
        "violeneaouinti@gmx.de", # -> persoenliche-kontakte
        "villaamroseneck@gmx.de",  # -> gesundheit
    ],
    "Folders/filter-andwendungen/computershare-online-services": [
        "computershare online services", # -> computershare
    ],
    "Folders/filter-andwendungen/ups.com": [
        "pkginfo@ups.com",
        "mcinfo@ups.com",
        "emailinfo@ups.com",
    ],

    "Folders/filter-andwendungen/mkt.vorwerk.com": [ # -> vorwerk
        "contact.de@mkt.vorwerk.com",
        "neolane.de@mkt.vorwerk.com",
        "cookidoo@mkt.vorwerk.com",
        "zufriedenheitsumfrage-thermomix@mkt.vorwerk.com",
    ],
    "Folders/filter-andwendungen/freelancer-agenturen/nemensis": [
        "rene.schwinning@nemensis.de",
    ],


    "Folders/filter-andwendungen/b.12go.asia": [
        "28351394@b.12go.asia",
        "27855159@b.12go.asia",
        "11067549@b.12go.asia",
        "27855160@b.12go.asia",
        "11067550@b.12go.asia",
    ],
    "Folders/filter-andwendungen/pal-tv.de": [
        "info@pal-tv.de",
        "andre.stubbs@pal-tv.de",
    ],
    "Folders/filter-andwendungen/dampfdorado.de": [
        "bestellungen@dampfdorado.de",
    ],
    "Folders/filter-andwendungen/research.fiverr.com": [  # -> fiverr
        "info@research.fiverr.com",
    ],
    "Folders/filter-andwendungen/versand-status.de": [ # -> nespresso
        "nespresso-no-reply@versand-status.de",
    ],

    "Folders/filter-andwendungen/wolt": [
        "info@wolt.com",
    ],
    "Folders/filter-andwendungen/home24": [
        "do-not-reply@reply.em.home24.de",
        "noreply@reply.em.home24.de",
    ],
    "Folders/filter-andwendungen/info.emmy-sharing.de": [ # -> emmy
        "isa@info.emmy-sharing.de",
        "lilo@info.emmy-sharing.de",
        "emmy@info.emmy-sharing.de",
    ],

    "Folders/filter-andwendungen/bassliner": [
        "buero@bassliner.org",
        "bookings@bassliner.org",
        "buchungen@bassliner.org",
    ],
    "Folders/filter-andwendungen/freelancer-agenturen/solcom": [
        "projektpartner@solcom.de",
        "projekte@solcom.de",
        "bewerbung@solcom.de",
    ],
    "Folders/filter-andwendungen/skatbank": [
        "info@skatbank.de",
    ],
    "Folders/filter-andwendungen/tuhh.de": [
        "dennis.hamann@tuhh.de",
        "servicedesk@tuhh.de",
        "otrs@tuhh.de",
    ],
    "Folders/filter-andwendungen/mailing.amorelie.de": [
        "produktempfehlung@mailing.amorelie.de",
        "newsletter@mailing.amorelie.de",
    ],
    "Folders/filter-andwendungen/welcome.americanexpress.com": [
        "erechnung@welcome.americanexpress.com",
        "onlineservices@welcome.americanexpress.com",
    ],
    "Folders/filter-andwendungen/e.battle.net": [
        "noreply@e.battle.net",
    ],
    "Folders/filter-andwendungen/uber.com": [
        "admin@uber.com",
    ],
    "Folders/filter-andwendungen/proton.me": [
        "va-katja.bardon@proton.me",
        "mailer-daemon@proton.me",
    ],
    "Folders/filter-andwendungen/news.mieterverein-hamburg.de": [
        "infomail@news.mieterverein-hamburg.de",
        "mieterjournal@news.mieterverein-hamburg.de",
        "noreply@news.mieterverein-hamburg.de",
        "newsletter@news.mieterverein-hamburg.de",
    ],
    "Folders/filter-andwendungen/hostelworld.com": [
        "bookings@hostelworld.com",
        "noreply@hostelworld.com",
    ],
    "Folders/filter-andwendungen/trip.com": [
        "de_noreply@trip.com",
        "de_flight@trip.com",
    ],
    "Folders/filter-andwendungen/finanzguru.de": [
        "dein@finanzguru.de",
    ],
    "Folders/filter-andwendungen/info.wise.com": [
        "noreply@info.wise.com",
    ],
    "Folders/filter-andwendungen/patreon.com": [
        "no-reply@patreon.com",
    ],
    "Folders/filter-andwendungen/mailing.tivoli.de": [
        "info@mailing.tivoli.de",
    ],
    "Folders/filter-andwendungen/hauer-naturprodukte.com": [
        "g.feldhusen-schwarz@hauer-naturprodukte.com",
    ],
    "Folders/filter-andwendungen/redglobal.com": [
        "info@redglobal.com",
        "nhnguyen@redglobal.com",
        "bgerhard@redglobal.com",
        "smegrelishvili@redglobal.com",
        "dataofficer@redglobal.com",
        "zrasch@redglobal.com",
        "jdabaas@redglobal.com",
    ],
    "Folders/filter-andwendungen/discord.com": [
        "notifications@discord.com",
    ],
    "Folders/filter-andwendungen/meetup.com": [
        "info@meetup.com",
    ],
    "Folders/filter-andwendungen/wasabi.com": [
        "support@wasabi.com",
    ],
    "Folders/filter-andwendungen/order.email.ikea.com": [
        "no.reply@order.email.ikea.com",
    ],
    "Folders/filter-andwendungen/motelamiio.com": [
        "news@motelamiio.com",
        "hello@motelamiio.com",
    ],
    "Folders/filter-andwendungen/termine.hamburg.de": [
        "noreply@termine.hamburg.de",
    ],
    "Folders/filter-andwendungen/ebay.com": [
        "ebay@ebay.com",
    ],
    "Folders/filter-andwendungen/klarna.de": [
        "noreply-de@klarna.de",
    ],
    "Folders/filter-andwendungen/shippypro.com": [
        "no-reply@shippypro.com",
    ],
    "Folders/filter-andwendungen/mindfactory.de": [
        "info@mindfactory.de",
    ],
    "Folders/filter-andwendungen/hamburg.de": [
        "erichsen@hamburg.de",
    ],
    "Folders/filter-andwendungen/information.swiss.com": [
        "flight.service@information.swiss.com",
        "travel.id@information.swiss.com",
        "booking@information.swiss.com",
    ],
    "Folders/filter-andwendungen/zara.com": [
        "noreply@zara.com",
    ],
    "Folders/filter-andwendungen/redditmail.com": [
        "noreply@redditmail.com",
    ],
    "Folders/filter-andwendungen/builderio.zendesk.com": [
        "support@builderio.zendesk.com",
    ],
    "Folders/filter-andwendungen/welcome.moia-mail.io": [
        "noreply@welcome.moia-mail.io",
    ],
    "Folders/filter-andwendungen/deutschebahn.com": [
        "noreply@deutschebahn.com",
    ],
    "Folders/filter-andwendungen/notifications.galaxus.de": [
        "noreply@notifications.galaxus.de",
    ],
    "Folders/filter-andwendungen/thomann.de": [
        "kundenservice@thomann.de",
        "buchhaltung@thomann.de",
    ],
    "Folders/filter-andwendungen/ko-fi.com": [
        "ko-fi@ko-fi.com",
    ],
    "Folders/filter-andwendungen/ownly.de": [
        "nicholas.ziegert@ownly.de",
    ],
    "Folders/filter-andwendungen/reply.gulp.de": [
        "willkommen@reply.gulp.de",
        "verfuegbarkeit@reply.gulp.de",
    ],

    # --- to-be-deleted ---
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
    "gmail.com",
    "protonmail.com",
    "t-online.de",
    "stripe.com",
    "mail.anthropic.com",
    "gmx.de",
    "computershare-online-services",
    "ups.com",
    # "m.ngrok.com",
    "mkt.vorwerk.com",
    "freelancer-agenturen/nemensis",


    # "newsletter.zattoo.com",
    # "dfinity.org",
    #"duolingo.com",
    #"facebookmail.com",
    "b.12go.asia",
    "pal-tv.de",
    "dampfdorado.de",
    "research.fiverr.com",
    "versand-status.de",
    # "mail.instagram.com",
    #"wolt.com",
    "home24",
    #"info.emmy-sharing.de",
    # "updates.fresha.com",
    "bassliner",
    "freelancer-agenturen/solcom",
    "skatbank",


    "tuhh.de",
    "mailing.amorelie.de",
    "welcome.americanexpress.com",
    "e.battle.net",
    "uber.com",
    "proton.me",
    "news.mieterverein-hamburg.de",
    "hostelworld.com",
    "trip.com",
    "finanzguru.de",
    "info.wise.com",
    "patreon.com",
    "mailing.tivoli.de",
    "hauer-naturprodukte.com",
    "redglobal.com",
    "discord.com",
    "meetup.com",
    "wasabi.com",
    "order.email.ikea.com",
    "motelamiio.com",
    "termine.hamburg.de",
    "ebay.com",
    "klarna.de",
    "shippypro.com",
    "mindfactory.de",
    "hamburg.de",
    "information.swiss.com",
    "zara.com",
    "redditmail.com",
    "builderio.zendesk.com",
    "welcome.moia-mail.io",
    "deutschebahn.com",
    "notifications.galaxus.de",
    "thomann.de",
    "ko-fi.com",
    "ownly.de",
    "reply.gulp.de",
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
    move_emails(dry_run=True)
