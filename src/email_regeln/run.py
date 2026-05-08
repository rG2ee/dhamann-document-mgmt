"""Verschiebt Mails aus der INBOX in die passenden filter-andwendungen-Ordner."""

from __future__ import annotations

import time

from email_regeln.imap_connection import create_email_folder_in_filter_anwendungen
from email_regeln.move_to_delete import run

ZUORDNUNGEN: dict[str, list[str]] = {
    # --- Bestehende Ordner in filter-andwendungen ---

    "Folders/filter-andwendungen/etke-host": [
        "aine@etke.cc", # ok

    ],
    "Folders/filter-andwendungen/amd": [
        "amdcommunity.mailer@amd.com", # ok
        "noreply@shop.amd.com", # ok
    ],
    "Folders/filter-andwendungen/vattenfall": [
        "angebot@vattenfall.de",  # ok
    ],
    "Folders/filter-andwendungen/proton": [
        "contact@protonmail.com",  # ok
        "usersfeedback@protonmail.com",  # ok
        "no-reply@app.protonmail.com", # ok
        "no-reply@app.protonvpn.com", # ok
        "no-reply@news.protonmail.com", # ok
        "no-reply@notify.protonmail.com", # ok
        "no-reply@notify.protonvpn.com", # ok
        "mailer-daemon@protonmail.com", # ok
    ],
    "Folders/filter-andwendungen/remarkable": [
        "team@mail.remarkable.com", # ok
        "team@remarkable.com", # ok
        "donotreply@remarkable.com",  # ok
    ],
    "Folders/filter-andwendungen/qubes-os": [
        "team@research.qubes-os.org",  # ok
        "no-reply@qubes-os.opencollective.com",  # ok
    ],
    "Folders/filter-andwendungen/doodle": [
        "time@doodle.com",  # ok
    ],
    "Folders/filter-andwendungen/miles-car-sharing": [
        "sophia@news.miles-mobility.com",  # ok
    ],
    "Folders/filter-andwendungen/barclays": [
        "service@email.barclaycard.de",  # ok
        "info@rueckzahlung.barclays.de",  # ok
    ],
    "Folders/filter-andwendungen/dhl-post": [
        "paket@dhl.de", # ok
        "noreply@dhl.com", # ok
        "noreply.kundenkonto@dhl.de", # ok
    ],
    "Folders/filter-andwendungen/ionos": [
        "noreply@ionos.com", # ok
    ],
    "Folders/filter-andwendungen/stakingrewards": [
        "noreply@stakingrewards.com",  # ok
    ],
    "Folders/filter-andwendungen/interactive-brokers": [
        "computershare.npcegbcecmgekcdecd@cpucommunications.com", # not ok, -> computershare
        "computershare.npcegbjemjgecdjejd@cpucommunications.com", # not ok, -> computershare
        "computershare.npcegdgemcjecdlebl@cpucommunications.com", # not ok, -> computershare
        "computershare.npcegdmeblcebhfemg@cpucommunications.com", # not ok, -> computershare
        "computershare.npceggkejdbedfgedf@cpucommunications.com", # not ok, -> computershare

        "service@onvista-bank.de", # not ok -> onvista
        "sburgsdorff@mmwarburg.com", # not ok -> warburg
        "rbudinsky@mmwarburg.com", # not ok -> warburg
        "thomas.weinmann@astorius.net", # not ok -> warburg
        "interactive brokers client services",
        "info@flatex.de", # not ok -> flatex
    ],
    "Folders/filter-andwendungen/dpd": [
        "empfangen@dpd.de", # ok
        "info@paket.dpd.de", # ok
    ],
    "Folders/filter-andwendungen/gorillas": [
        "feedback@gorillasapp.com", # ok
        "feedback@mail.gorillasapp.es", # ok
    ],
    "Folders/filter-andwendungen/flink": [
        "funda.zurnaci@flink-44a615fa4e6a.intercom-mail.com", # ok
        "hello@goflink.com", # ok
        "jonah@flink-44a615fa4e6a.intercom-mail.com", #ok
        "operator@flink-44a615fa4e6a.intercom-mail.com",  #ok
    ],
    "Folders/filter-andwendungen/samedi": [
        "info@mail.samedi.de",  # ok
        "dkluge@hanseatic-physio.de",  # hanseatic-physio
        "noreply@jameda.de", # ok
    ],
    "Folders/filter-andwendungen/webo-hosting": [
        "info@webo.hosting", # ok
    ],
    "Folders/filter-andwendungen/debeka": [
        "kundenservice@debeka.de", # ok
        "noreply-newsletter@debeka.de", # ok
    ],
    "Folders/filter-andwendungen/medium": [
        "members@medium.com", # ok
    ],
    "Folders/filter-andwendungen/vodafone": [
        "nicht.antworten@kundenservice.vodafone.com", # ok
    ],
    "Folders/filter-andwendungen/fiverr": [
        "no-reply@fiverr.com",  # ok
    ],
    "Folders/filter-andwendungen/eversports": [
        "no-reply@priority-send.eversports.com",  # ok
    ],
    "Folders/filter-andwendungen/github": [
        "noreply@github.com",  # ok
    ],
    "Folders/filter-andwendungen/discord": [
        "noreply@discordapp.com",  # ok
    ],
    "Folders/filter-andwendungen/buymeacoffee": [
        "notifications@buymeacoffee.com",   # ok
    ],
    "Folders/filter-andwendungen/google": [
        "no-reply@youtube.com",  # ok
        "noreply-utos@google.com",  # ok
    ],
    "Folders/filter-andwendungen/stadt-hamburg": [
        "automatischeantwort@finanzamt.hamburg.de", # not ok >  finanzamt-hamburg
        "do-not-reply@mgs-eportal.de", # not ok -> gesundheit
        "bremer-rheumatologie@hamburg.de", # not ok -> gesundheit
        "info@stadtradhamburg.de", # ok
    ],
    "Folders/filter-andwendungen/alternate": [
        "studio@djmerlin.com",  # ok
    ],
    "Folders/filter-andwendungen/freelancer-agenturen": [

    ],

    # --- Bestehende Ordner in Folders ---

    "Folders/shopping": [
        "coupons@galaxus.de", # not ok eigener ordner
        "team@notebooksbilliger.de",  # not ok eigener ordner
        "service@notebooksbilliger.de",  # not ok eigener ordner
        "pricezilla@versand-status.de", # not ok eigener ordner



        "noreply@notice-eu.roborock.com", # not ok eigener ordner
        "do.not.reply@ikea.com",  # not ok eigener ordner
        "noreply@ikea.com",# not ok eigener ordner
        "emails@mail.etsy.com", # not ok eigener ordner
        "noreply@etsy.com", # not ok eigener ordner
        "noreply@mail.etsy.com", # not ok eigener ordner
        "galaxus@galaxus.de", # not ok eigener ordner
        "galaxus@security.galaxus.de", # not ok eigener ordner

        "info@physiosupplies.de", # not ok eigener ordner

        "kundenservice@amorelie.de", # not ok eigener ordner

        "orderconfirmation@digitalriver.com", # amd

    ],
    "Folders/account management": [
        "billing@b.etesync.com", # etke-host
        "support-mailer@b.etesync.com", # etke-host

        "sepa-awpde@allianz.com", # allianz
        "service-reise@allianz.com", # allianz
        "hello@1password.com", # coinbase
        "no-reply@coinbase.com", # coinbase
        "info@cb.mail.coinbase.com", # coinbase

        "no-reply@transparenzregister.de", # transparenzregister
        "meineschufa@schufa.de", # schufa
        "no-reply-pk@schufa.de", # schufa
        "noreply@buhl.de", # delete
    ],
    "Folders/computer": [

    ],
    "Folders/Steuer-2022": [
        "svencarstens@carstens-stb.de", # steuer
        "vbs22@bafin.de", # flatex
    ],
    "Folders/wichtig": [  ## -> bitte in Folders/filter-andwendungen/persoenliche-kontakte umbenennen
        "andrearuff@gmx.de",
        "danja.kluever@gruene-hu.de",
        "ulf.kluever@gruene-hu.de",
        "ulf.kluever@gruene-se-kv.de",
        "ulf.kluever@protonmail.com",
        "dennis.hamann@ownly.de", # warburg
        "dennis@cubicl.de", # cubibl
        "uwe@harste.org", # ramona-mertens
        "safli@web.de",
        "pascal_dominik.greder@smail.th-koeln.de",
        "pia-info@pleugerindustries.com", # cubibl
    ],
    "Labels/INBOX.Wohnung": [
        "beratung@mieterverein-hamburg.de",  # not ok -> mietverein-hamburg
    ],

    # --- Verbleiben in to-be-deleted (wirklich loeschbar) ---

    "Folders/to-be-deleted": [

        "empfang@trude-hh.de", # tuhh

        "eta@1avisum.de", # eigener ordner
        "info@1avisum.de", # eigener ordner
        "failed-payments+acct_1apfzwjetinljgaa@stripe.com", # etke



        "help@paddle.com",
        "hoheluft@pokehamburg.de",
        "huami@email.huami.com",
        "mifit-feedback-auto@email.huami.com",
        "official@amazfit.com",

        "immigrationofficegovernmentcomplexchaengwattanard@imm1division.onmicrosoft.com", # 1a-visum

        "jan.steinke@ownly.de", # warburg

        "info@deltakonnect.de", # deltakonnect
        "info@dkb.de", # dbk

        "info@hnoamrothenbaum.de", # gesundheit



        "kundenservice@spb-garant.de", # alternate

        "mail@argon-orthopaedie.de", # gesundheit


        "message.npcefmledbcedhmecg@cpucommunications.com", # computershare
        "message.npcegbbemhfegllejg@cpucommunications.com", # computershare
        "message.npcegbbemhfehbdedd@cpucommunications.com", # computershare
        "message.npcegbbemhgecfbekl@cpucommunications.com", # computershare
        "message.npcegdmefddedfkejh@cpucommunications.com", # computershare



        "miguelchapero@icloud.com",   # persoenliche-kontatke
        "msb@atelier-bachert.de",  # persoenliche-kontatke
        "neugebauer_katharina@ymail.com", # persoenliche-kontatke

        "nm@activatio.de",  # activatio
        "no-reply@agoda-email.com", # agoda
        "no-reply@security.agoda.com", # agoda
        "no-reply@sg.sgt.agoda-email.com", # agoda
        "no-reply@announcements.soundcloud.com", # soundcloud


        "no-reply@jameda.de", # eigener ordner



        "noreply@astorius.net",  # warburg





        "noreply_mia@mieterverein-hamburg.de", # mietverein-hamburg
    ],
}













ZUORDNUNGEN = {


"Folders/to-be-deleted": [
    "noreply@notifs.matrix.org", # wrong -> delete
    "connect@data.nasdaq.com",  # -> just delete
    "connect@quandl.com",  # just delete
    "a.frietsch@computerfutures.de", # not ok, just delete
    "retoure@x-kom.de", # just delete

    "info@arena-supplements.de", # delete
    "info@aspire-shop.de", # delete
    "info@computeruniverse.net", # delete
    "info@morenutrition.de", # deltee
    "info@onlysports.de", # delete

    "info@rundetrends.com", # delete
    "info@sertronics.shop", # delete
    "no-reply@amorelie.de", # delete

    "kundenservice@pricezilla.de", # delete
    "noreply@frittenwerk-shop.de", # delete

    "upcoming-invoice+acct_1apfzwjetinljgaa@stripe.com", # delete
    "receipts+acct_1apfzwjetinljgaa@stripe.com", # delte
    "donotreply@godaddy.com", # delete

    "noreply@kaggle.com",  # delete
    "do-not-reply@stackoverflow.email",  # delete
    "no-reply@notify.docker.com",  # delete
    "noreply@notifications.getpostman.com",  # delete
    "noreply@discuss.grapheneos.org",  # delete
    "news@nvidia.com",  # delete

    "email@em.blizzard.com", # delete
    "noreply@blizzard.com", # delete
    "noreply@em.blizzard.com", # delete

    "ergebnis@testformular.de", # delete

    "flight_notification@bangkokair.com",  # delete
    "foundation@dfinity.org", # delete
    "irving.yang@dfinity.org", # delete
    "irving_yang@dfinity.org", # delete
    "michael_hunte@dfinity.org", # delete
    "hallo@getir.com", # delete
    "info@getir.com", # delete

    "hello@storj.io", # delete
    "help@disneyplus.com", # delete
    "member.services@disneyaccount.com", # delete
    "help@gotinder.com", # delete

    "heide@alex-kitchen.de", # delete
    "hello@filebase.com", # delete
    "hello@skynetlabs.com", # delete

    "igor@hiveon.net", # delte

    "info@ew.eurowings.com",  # delte
    "news@ew.eurowings.com",  # delte
    "no-answer@condor.com",  # delte
    "info@cryptomator.org",  # delte

    "inez@cubicl.de",# cubicl

    "info@feel-festival.de",  # delte

    "newsletter.de@clickandboat.com", # delete
    "nora.futaky@clickandboat.com", # delete
    "newsletter@eat-the-world.com", # delete
    "newsletter@news.eat-the-world.com", # delete
    "newsletterversand@pizzamax.de",  # delete

    "messenger@webex.com", # delete
    "learn@email1.asana.com", # delete

    "info@news.dominos.de", # delete
    "info@service.premiumkino.de", # delete
    "no-reply@asana.com",  # delete
    "no-reply@akash.network", # deltete
    "noreply@prosieben.de",
    "noreply@lfconnect.com",
    "noreply@newsletter.callabike-interaktiv.de",
    "noreply@tof.de",
    "notifications@tchncs.de",
    "noreply@trackmyshipment.co",
    "noreply@trymagic.com",

    "no-reply@xoom.com",
    "no-reply@zoom.us",
    "no-reply@notification.skype.com",
    "noreply@d.tube",
    "noreply@coinpayments.net",
    "noreply.invitations@trustpilotmail.com",
    "no-reply@restablo.de",
    "no-reply@quandl.com",

    "no-reply@mailer.opodo.com",
    "noreply@opodo.com",
    "noreply@impfterminservice.de",
    "noreply@europe-west-1.tardigrade.io",
    "no-reply@auth.appnotify.io",
    "info@dom-ticket.de",
    "info@dyndnss.net",
    "noreply@ddnss.de",
    "noreply@condor.com",

    "info@mail.termin2go.com",

    "info@whitebit.com",
    "marketing@mail.wolt.com",
    "mail@service.tvnow.de",
    "kundendialog@nah.sh",
    "julia@plattenmonster.com",
    "jc95573@gmail.com",
    "mail@testme.hamburg",
    "noreply@testproject.io",
    "meital.matsafi@testproject.io",
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

