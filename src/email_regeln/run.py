"""Verschiebt Mails aus der INBOX in die passenden filter-andwendungen-Ordner."""

from __future__ import annotations

import time

from email_regeln.imap_connection import create_email_folder_in_filter_anwendungen
from email_regeln.move_to_delete import run

ZUORDNUNGEN: dict[str, list[str]] = {
    # --- Bestehende Ordner, neue Adressen ---

    # --- Neue Ordner (siehe FOLDERS_TO_BE_CREATED) ---

    "NOT-DELETIONofMAILSbefore2023":
    [
        "a.frietsch@computerfutures.de",
        'aine@etke.cc',
        'amdcommunity.mailer@amd.com',
        'andrearuff@gmx.de',
        'angebot@vattenfall.de',
        'automatischeantwort@finanzamt.hamburg.de',
        'beratung@mieterverein-hamburg.de',
        'billing@b.etesync.com',
        'bremer-rheumatologie@hamburg.de',


        'computershare.npcegbcecmgekcdecd@cpucommunications.com',
        'computershare.npcegbjemjgecdjejd@cpucommunications.com',
        'computershare.npcegdgemcjecdlebl@cpucommunications.com',
        'computershare.npcegdmeblcebhfemg@cpucommunications.com',
        'computershare.npceggkejdbedfgedf@cpucommunications.com',

        'connect@data.nasdaq.com',
        'connect@quandl.com',
        'contact@protonmail.com',
        'coupons@galaxus.de',
        'danja.kluever@gruene-hu.de',

        'dennis.hamann@ownly.de',
        'dennis@cubicl.de',
        'dkluge@hanseatic-physio.de',
        'do-not-reply@mgs-eportal.de',


        'team@mail.remarkable.com',
        'team@notebooksbilliger.de',
        'team@remarkable.com',
        'team@research.qubes-os.org',
        'upcoming-invoice+acct_1apfzwjetinljgaa@stripe.com',
        'usersfeedback@protonmail.com',
        'uwe@harste.org',
        'vbs22@bafin.de',
        'ulf.kluever@gruene-hu.de',
        'ulf.kluever@gruene-se-kv.de',
        'ulf.kluever@protonmail.com',
        'time@doodle.com',
        'thomas.weinmann@astorius.net',
        'svencarstens@carstens-stb.de',
        'support-mailer@b.etesync.com',
        'sophia@news.miles-mobility.com',
        'studio@djmerlin.com', # alternate
        'service@onvista-bank.de',
        'service@notebooksbilliger.de',
        'service@email.barclaycard.de',
        'sepa-awpde@allianz.com',
        'service-reise@allianz.com',
        'sburgsdorff@mmwarburg.com',
        'safli@web.de', # sarah flint
        'retoure@x-kom.de',
        'rbudinsky@mmwarburg.com',
        'paket@dhl.de',
        'pascal_dominik.greder@smail.th-koeln.de',
        'pia-info@pleugerindustries.com',
        'pricezilla@versand-status.de', # pixel 5 gekauft

        'noreply@ionos.com',
        'noreply@jameda.de',
        'noreply@kaggle.com',
        'noreply@notice-eu.roborock.com',
        'noreply@stakingrewards.com',
        'receipts+acct_1apfzwjetinljgaa@stripe.com',
    ],

    "Folders/to-be-deleted": [


         'do-not-reply@stackoverflow.email',
         'do.not.reply@ikea.com',
         'donotreply@godaddy.com',
         'donotreply@remarkable.com',
         'email@em.blizzard.com',
         'emails@mail.etsy.com',



         'empfang@trude-hh.de',
         'empfangen@dpd.de',
         'ergebnis@testformular.de',
         'eta@1avisum.de',
         'failed-payments+acct_1apfzwjetinljgaa@stripe.com',
         'feedback@gorillasapp.com',
         'feedback@mail.gorillasapp.es',
         'flight_notification@bangkokair.com',
         'foundation@dfinity.org',
         'funda.zurnaci@flink-44a615fa4e6a.intercom-mail.com',
         'galaxus@galaxus.de',
         'galaxus@security.galaxus.de',
         'hallo@getir.com',
         'heide@alex-kitchen.de',
         'hello@1password.com',
         'hello@filebase.com',
         'hello@goflink.com',
         'hello@skynetlabs.com',
         'hello@storj.io',
         'help@disneyplus.com',
         'help@gotinder.com',
         'help@paddle.com',
         'hoheluft@pokehamburg.de',
         'huami@email.huami.com',
         'igor@hiveon.net',
         'immigrationofficegovernmentcomplexchaengwattanard@imm1division.onmicrosoft.com',
         'inez@cubicl.de',
         'info@1avisum.de',
         'info@arena-supplements.de',
         'info@aspire-shop.de',
         'info@cb.mail.coinbase.com',
         'info@computeruniverse.net',
         'info@cryptomator.org',
         'info@deltakonnect.de',
         'info@dkb.de',
         'info@dom-ticket.de',
         'info@dyndnss.net',
         'info@ew.eurowings.com',
         'info@feel-festival.de',
         'info@flatex.de',
         'info@getir.com',
         'info@hnoamrothenbaum.de',
         'info@mail.samedi.de',
         'info@mail.termin2go.com',
         'info@morenutrition.de',
         'info@news.dominos.de',
         'info@onlysports.de',
         'info@paket.dpd.de',
         'info@physiosupplies.de',
         'info@rueckzahlung.barclays.de',
         'info@rundetrends.com',
         'info@sertronics.shop',
         'info@service.premiumkino.de',
         'info@stadtradhamburg.de',
         'info@webo.hosting',
         'info@whitebit.com',
         'interactive brokers client services',
         'irving.yang@dfinity.org',
         'irving_yang@dfinity.org',
         'jan.steinke@ownly.de',
         'jc95573@gmail.com',
         'jonah@flink-44a615fa4e6a.intercom-mail.com',
         'julia@plattenmonster.com',
         'kundendialog@nah.sh',
         'kundenservice@amorelie.de',
         'kundenservice@debeka.de',
         'kundenservice@pricezilla.de',
         'kundenservice@spb-garant.de',
         'learn@email1.asana.com',
         'mail@argon-orthopaedie.de',
         'mail@service.tvnow.de',
         'mail@testme.hamburg',
         'mailer-daemon@protonmail.com',
         'marketing@mail.wolt.com',
         'meineschufa@schufa.de',
         'meital.matsafi@testproject.io',
         'member.services@disneyaccount.com',
         'members@medium.com',
         'message.npcefmledbcedhmecg@cpucommunications.com',
         'message.npcegbbemhfegllejg@cpucommunications.com',
         'message.npcegbbemhfehbdedd@cpucommunications.com',
         'message.npcegbbemhgecfbekl@cpucommunications.com',
         'message.npcegdmefddedfkejh@cpucommunications.com',
         'messenger@webex.com',
         'michael_hunte@dfinity.org',
         'mifit-feedback-auto@email.huami.com',
         'miguelchapero@icloud.com',
         'msb@atelier-bachert.de',
         'neugebauer_katharina@ymail.com',
         'news@ew.eurowings.com',
         'news@nvidia.com',
         'newsletter.de@clickandboat.com',
         'newsletter@eat-the-world.com',
         'newsletter@news.eat-the-world.com',
         'newsletterversand@pizzamax.de',
         'nicht.antworten@kundenservice.vodafone.com',
         'nm@activatio.de',
         'no-answer@condor.com',
         'no-reply-pk@schufa.de',
         'no-reply@agoda-email.com',
         'no-reply@akash.network',
         'no-reply@amorelie.de',
         'no-reply@announcements.soundcloud.com',
         'no-reply@app.protonmail.com',
         'no-reply@app.protonvpn.com',
         'no-reply@asana.com',
         'no-reply@auth.appnotify.io',
         'no-reply@coinbase.com',
         'no-reply@fiverr.com',
         'no-reply@jameda.de',
         'no-reply@mailer.opodo.com',
         'no-reply@news.protonmail.com',
         'no-reply@notification.skype.com',
         'no-reply@notify.docker.com',
         'no-reply@notify.protonmail.com',
         'no-reply@notify.protonvpn.com',
         'no-reply@priority-send.eversports.com',
         'no-reply@quandl.com',
         'no-reply@qubes-os.opencollective.com',
         'no-reply@restablo.de',
         'no-reply@security.agoda.com',
         'no-reply@sg.sgt.agoda-email.com',
         'no-reply@transparenzregister.de',
         'no-reply@xoom.com',
         'no-reply@youtube.com',
         'no-reply@zoom.us',
         'nora.futaky@clickandboat.com',
         'noreply-newsletter@debeka.de',
         'noreply-utos@google.com',
         'noreply.invitations@trustpilotmail.com',
         'noreply.kundenkonto@dhl.de',
         'noreply@astorius.net',
         'noreply@blizzard.com',
         'noreply@buhl.de',
         'noreply@coinpayments.net',
         'noreply@condor.com',
         'noreply@d.tube',
         'noreply@ddnss.de',
         'noreply@dhl.com',
         'noreply@discordapp.com',
         'noreply@discuss.grapheneos.org',
         'noreply@em.blizzard.com',
         'noreply@etsy.com',
         'noreply@europe-west-1.tardigrade.io',
         'noreply@frittenwerk-shop.de',
         'noreply@github.com',
         'noreply@ikea.com',
         'noreply@impfterminservice.de',

         'noreply@lfconnect.com',
         'noreply@mail.etsy.com',
         'noreply@newsletter.callabike-interaktiv.de',

         'noreply@notifications.getpostman.com',

         'noreply@notifs.matrix.org',
         'noreply@opodo.com',
         'noreply@prosieben.de',
         'noreply@shop.amd.com',

         'noreply@testproject.io',
         'noreply@tof.de',
         'noreply@trackmyshipment.co',
         'noreply@trymagic.com',
         'noreply_mia@mieterverein-hamburg.de',
         'notifications@buymeacoffee.com',

         'notifications@tchncs.de',
         'official@amazfit.com',
         'operator@flink-44a615fa4e6a.intercom-mail.com',
         'orderconfirmation@digitalriver.com',

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

