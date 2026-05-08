"""Verschiebt Mails aus der INBOX in die passenden filter-andwendungen-Ordner."""

from __future__ import annotations

import time

from email_regeln.imap_connection import create_email_folder_in_filter_anwendungen
from email_regeln.move_to_delete import run

ZUORDNUNGEN: dict[str, list[str]] = {
    # --- Bestehende Ordner in filter-andwendungen ---

    "Folders/filter-andwendungen/etke-host": [
        "aine@etke.cc",
        "noreply@notifs.matrix.org",
    ],
    "Folders/filter-andwendungen/amd": [
        "amdcommunity.mailer@amd.com",
        "noreply@shop.amd.com",
    ],
    "Folders/filter-andwendungen/vattenfall": [
        "angebot@vattenfall.de",
    ],
    "Folders/filter-andwendungen/proton": [
        "contact@protonmail.com",
        "usersfeedback@protonmail.com",
        "no-reply@app.protonmail.com",
        "no-reply@app.protonvpn.com",
        "no-reply@news.protonmail.com",
        "no-reply@notify.protonmail.com",
        "no-reply@notify.protonvpn.com",
        "mailer-daemon@protonmail.com",
    ],
    "Folders/filter-andwendungen/remarkable": [
        "team@mail.remarkable.com",
        "team@remarkable.com",
        "donotreply@remarkable.com",
    ],
    "Folders/filter-andwendungen/qubes-os": [
        "team@research.qubes-os.org",
        "no-reply@qubes-os.opencollective.com",
    ],
    "Folders/filter-andwendungen/doodle": [
        "time@doodle.com",
    ],
    "Folders/filter-andwendungen/miles-car-sharing": [
        "sophia@news.miles-mobility.com",
    ],
    "Folders/filter-andwendungen/barclays": [
        "service@email.barclaycard.de",
        "info@rueckzahlung.barclays.de",
    ],
    "Folders/filter-andwendungen/dhl-post": [
        "paket@dhl.de",
        "noreply@dhl.com",
        "noreply.kundenkonto@dhl.de",
    ],
    "Folders/filter-andwendungen/ionos": [
        "noreply@ionos.com",
    ],
    "Folders/filter-andwendungen/stakingrewards": [
        "noreply@stakingrewards.com",
    ],
    "Folders/filter-andwendungen/interactive-brokers": [
        "computershare.npcegbcecmgekcdecd@cpucommunications.com",
        "computershare.npcegbjemjgecdjejd@cpucommunications.com",
        "computershare.npcegdgemcjecdlebl@cpucommunications.com",
        "computershare.npcegdmeblcebhfemg@cpucommunications.com",
        "computershare.npceggkejdbedfgedf@cpucommunications.com",
        "connect@data.nasdaq.com",
        "connect@quandl.com",
        "service@onvista-bank.de",
        "sburgsdorff@mmwarburg.com",
        "rbudinsky@mmwarburg.com",
        "thomas.weinmann@astorius.net",
        "interactive brokers client services",
        "info@flatex.de",
    ],
    "Folders/filter-andwendungen/dpd": [
        "empfangen@dpd.de",
        "info@paket.dpd.de",
    ],
    "Folders/filter-andwendungen/gorillas": [
        "feedback@gorillasapp.com",
        "feedback@mail.gorillasapp.es",
    ],
    "Folders/filter-andwendungen/flink": [
        "funda.zurnaci@flink-44a615fa4e6a.intercom-mail.com",
        "hello@goflink.com",
        "jonah@flink-44a615fa4e6a.intercom-mail.com",
        "operator@flink-44a615fa4e6a.intercom-mail.com",
    ],
    "Folders/filter-andwendungen/samedi": [
        "info@mail.samedi.de",
        "dkluge@hanseatic-physio.de",
        "noreply@jameda.de",
    ],
    "Folders/filter-andwendungen/webo-hosting": [
        "info@webo.hosting",
    ],
    "Folders/filter-andwendungen/debeka": [
        "kundenservice@debeka.de",
        "noreply-newsletter@debeka.de",
    ],
    "Folders/filter-andwendungen/medium": [
        "members@medium.com",
    ],
    "Folders/filter-andwendungen/vodafone": [
        "nicht.antworten@kundenservice.vodafone.com",
    ],
    "Folders/filter-andwendungen/fiverr": [
        "no-reply@fiverr.com",
    ],
    "Folders/filter-andwendungen/eversports": [
        "no-reply@priority-send.eversports.com",
    ],
    "Folders/filter-andwendungen/github": [
        "noreply@github.com",
    ],
    "Folders/filter-andwendungen/discord": [
        "noreply@discordapp.com",
    ],
    "Folders/filter-andwendungen/buymeacoffee": [
        "notifications@buymeacoffee.com",
    ],
    "Folders/filter-andwendungen/google": [
        "no-reply@youtube.com",
        "noreply-utos@google.com",
    ],
    "Folders/filter-andwendungen/stadt-hamburg": [
        "automatischeantwort@finanzamt.hamburg.de",
        "do-not-reply@mgs-eportal.de",
        "bremer-rheumatologie@hamburg.de",
        "info@stadtradhamburg.de",
    ],
    "Folders/filter-andwendungen/alternate": [
        "studio@djmerlin.com",
    ],
    "Folders/filter-andwendungen/freelancer-agenturen": [
        "a.frietsch@computerfutures.de",
    ],

    # --- Bestehende Ordner in Folders ---

    "Folders/shopping": [
        "coupons@galaxus.de",
        "team@notebooksbilliger.de",
        "service@notebooksbilliger.de",
        "pricezilla@versand-status.de",
        "retoure@x-kom.de",
        "noreply@notice-eu.roborock.com",
        "do.not.reply@ikea.com",
        "noreply@ikea.com",
        "emails@mail.etsy.com",
        "noreply@etsy.com",
        "noreply@mail.etsy.com",
        "galaxus@galaxus.de",
        "galaxus@security.galaxus.de",
        "info@arena-supplements.de",
        "info@aspire-shop.de",
        "info@computeruniverse.net",
        "info@morenutrition.de",
        "info@onlysports.de",
        "info@physiosupplies.de",
        "info@rundetrends.com",
        "info@sertronics.shop",
        "kundenservice@amorelie.de",
        "no-reply@amorelie.de",
        "kundenservice@pricezilla.de",
        "orderconfirmation@digitalriver.com",
        "noreply@frittenwerk-shop.de",
    ],
    "Folders/account management": [
        "billing@b.etesync.com",
        "support-mailer@b.etesync.com",
        "upcoming-invoice+acct_1apfzwjetinljgaa@stripe.com",
        "receipts+acct_1apfzwjetinljgaa@stripe.com",
        "sepa-awpde@allianz.com",
        "service-reise@allianz.com",
        "hello@1password.com",
        "no-reply@coinbase.com",
        "info@cb.mail.coinbase.com",
        "donotreply@godaddy.com",
        "no-reply@transparenzregister.de",
        "meineschufa@schufa.de",
        "no-reply-pk@schufa.de",
        "noreply@buhl.de",
    ],
    "Folders/computer": [
        "noreply@kaggle.com",
        "do-not-reply@stackoverflow.email",
        "no-reply@notify.docker.com",
        "noreply@notifications.getpostman.com",
        "noreply@discuss.grapheneos.org",
        "news@nvidia.com",
    ],
    "Folders/Steuer-2022": [
        "svencarstens@carstens-stb.de",
        "vbs22@bafin.de",
    ],
    "Folders/wichtig": [
        "andrearuff@gmx.de",
        "danja.kluever@gruene-hu.de",
        "ulf.kluever@gruene-hu.de",
        "ulf.kluever@gruene-se-kv.de",
        "ulf.kluever@protonmail.com",
        "dennis.hamann@ownly.de",
        "dennis@cubicl.de",
        "uwe@harste.org",
        "safli@web.de",
        "pascal_dominik.greder@smail.th-koeln.de",
        "pia-info@pleugerindustries.com",
    ],
    "Labels/INBOX.Wohnung": [
        "beratung@mieterverein-hamburg.de",
    ],

    # --- Verbleiben in to-be-deleted (wirklich loeschbar) ---

    "Folders/to-be-deleted": [
        "email@em.blizzard.com",
        "noreply@blizzard.com",
        "noreply@em.blizzard.com",
        "empfang@trude-hh.de",
        "ergebnis@testformular.de",
        "eta@1avisum.de",
        "info@1avisum.de",
        "failed-payments+acct_1apfzwjetinljgaa@stripe.com",
        "flight_notification@bangkokair.com",
        "foundation@dfinity.org",
        "irving.yang@dfinity.org",
        "irving_yang@dfinity.org",
        "michael_hunte@dfinity.org",
        "hallo@getir.com",
        "info@getir.com",
        "heide@alex-kitchen.de",
        "hello@filebase.com",
        "hello@skynetlabs.com",
        "hello@storj.io",
        "help@disneyplus.com",
        "member.services@disneyaccount.com",
        "help@gotinder.com",
        "help@paddle.com",
        "hoheluft@pokehamburg.de",
        "huami@email.huami.com",
        "mifit-feedback-auto@email.huami.com",
        "official@amazfit.com",
        "igor@hiveon.net",
        "immigrationofficegovernmentcomplexchaengwattanard@imm1division.onmicrosoft.com",
        "inez@cubicl.de",
        "jan.steinke@ownly.de",
        "info@cryptomator.org",
        "info@deltakonnect.de",
        "info@dkb.de",
        "info@dom-ticket.de",
        "info@dyndnss.net",
        "noreply@ddnss.de",
        "info@ew.eurowings.com",
        "news@ew.eurowings.com",
        "no-answer@condor.com",
        "noreply@condor.com",
        "info@feel-festival.de",
        "info@hnoamrothenbaum.de",
        "info@mail.termin2go.com",
        "info@news.dominos.de",
        "info@service.premiumkino.de",
        "info@whitebit.com",
        "jc95573@gmail.com",
        "julia@plattenmonster.com",
        "kundendialog@nah.sh",
        "kundenservice@spb-garant.de",
        "learn@email1.asana.com",
        "mail@argon-orthopaedie.de",
        "mail@service.tvnow.de",
        "mail@testme.hamburg",
        "marketing@mail.wolt.com",
        "meital.matsafi@testproject.io",
        "noreply@testproject.io",
        "message.npcefmledbcedhmecg@cpucommunications.com",
        "message.npcegbbemhfegllejg@cpucommunications.com",
        "message.npcegbbemhfehbdedd@cpucommunications.com",
        "message.npcegbbemhgecfbekl@cpucommunications.com",
        "message.npcegdmefddedfkejh@cpucommunications.com",
        "messenger@webex.com",
        "miguelchapero@icloud.com",
        "msb@atelier-bachert.de",
        "neugebauer_katharina@ymail.com",
        "newsletter.de@clickandboat.com",
        "nora.futaky@clickandboat.com",
        "newsletter@eat-the-world.com",
        "newsletter@news.eat-the-world.com",
        "newsletterversand@pizzamax.de",
        "nm@activatio.de",
        "no-reply@agoda-email.com",
        "no-reply@security.agoda.com",
        "no-reply@sg.sgt.agoda-email.com",
        "no-reply@akash.network",
        "no-reply@announcements.soundcloud.com",
        "no-reply@asana.com",
        "no-reply@auth.appnotify.io",
        "no-reply@jameda.de",
        "no-reply@mailer.opodo.com",
        "noreply@opodo.com",
        "no-reply@notification.skype.com",
        "no-reply@quandl.com",
        "no-reply@restablo.de",
        "no-reply@xoom.com",
        "no-reply@zoom.us",
        "noreply.invitations@trustpilotmail.com",
        "noreply@astorius.net",
        "noreply@coinpayments.net",
        "noreply@d.tube",
        "noreply@europe-west-1.tardigrade.io",
        "noreply@impfterminservice.de",
        "noreply@lfconnect.com",
        "noreply@newsletter.callabike-interaktiv.de",
        "noreply@prosieben.de",
        "noreply@tof.de",
        "noreply@trackmyshipment.co",
        "noreply@trymagic.com",
        "noreply_mia@mieterverein-hamburg.de",
        "notifications@tchncs.de",
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

