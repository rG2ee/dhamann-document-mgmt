"""Durchsucht Mails bestimmter Absender serverseitig per IMAP SEARCH nach Schluesselwoertern im Body."""

from __future__ import annotations

import imaplib
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime

from email_regeln.imap_connection import connect


def _decode_header_value(raw: str) -> str:
    parts: list[str] = []
    for fragment, charset in decode_header(raw):
        if isinstance(fragment, bytes):
            parts.append(fragment.decode(charset or "utf-8", errors="replace"))
        else:
            parts.append(fragment)
    return "".join(parts)


def _search_sender_word(mail: imaplib.IMAP4, sender: str, word: str) -> set[bytes]:
    """IMAP SEARCH FROM + BODY fuer einen Absender und ein Wort."""
    _status, data = mail.search(None, "FROM", f'"{sender}"', "BODY", f'"{word}"')
    ids = data[0].split()
    return set(ids)


def _fetch_headers(
    mail: imaplib.IMAP4, msg_ids: set[bytes],
) -> dict[bytes, tuple[str, str, str]]:
    """Holt FROM, DATE, SUBJECT fuer die gegebenen Message-IDs.

    Gibt {msg_id: (date_str, sender, subject)} zurueck.
    """
    if not msg_ids:
        return {}

    id_range = b",".join(sorted(msg_ids))
    _status, response = mail.fetch(
        id_range, "(BODY.PEEK[HEADER.FIELDS (FROM DATE SUBJECT)])"
    )

    results: dict[bytes, tuple[str, str, str]] = {}
    current_id: bytes | None = None

    for item in response:
        if not isinstance(item, tuple):
            continue

        meta = item[0]
        if isinstance(meta, bytes):
            seq = meta.split(b" ", 1)[0]
            current_id = seq

        raw_header = item[1]
        if isinstance(raw_header, bytes):
            raw_header = raw_header.decode("utf-8", errors="replace")

        date_str = ""
        sender = ""
        subject = ""

        for line in raw_header.splitlines():
            lower = line.lower()
            if lower.startswith("date:"):
                try:
                    dt = parsedate_to_datetime(line[5:].strip())
                    date_str = dt.strftime("%Y-%m-%d")
                except Exception:
                    date_str = line[5:].strip()
            elif lower.startswith("from:"):
                decoded = _decode_header_value(line[5:].strip())
                _, addr = parseaddr(decoded)
                sender = addr.lower() if addr else decoded
            elif lower.startswith("subject:"):
                subject = _decode_header_value(line[8:].strip())

        if current_id is not None:
            results[current_id] = (date_str, sender, subject)

    return results


def search_mail_content(
    emails_from_list: list[str],
    included_words: list[str],
) -> None:
    """Durchsucht die INBOX nach Mails der angegebenen Absender, deren Body
    mindestens eines der Schluesselwoerter enthaelt, und gibt Treffer aus.
    """
    print("Verbinde mit Protonmail Bridge …")
    mail = connect()

    try:
        mail.select("INBOX", readonly=True)
        print(
            f"Suche in INBOX nach {len(included_words)} Wort/Woertern "
            f"bei {len(emails_from_list)} Absender(n) …\n"
        )

        total_hits = 0
        senders_with_hits = 0

        for sender in emails_from_list:
            print(f"--- {sender} ---")

            id_to_words: dict[bytes, list[str]] = {}
            for word in included_words:
                ids = _search_sender_word(mail, sender, word)
                for mid in ids:
                    id_to_words.setdefault(mid, []).append(word)

            if not id_to_words:
                print("  Keine Treffer fuer die angegebenen Woerter.\n")
                continue

            senders_with_hits += 1
            headers = _fetch_headers(mail, set(id_to_words.keys()))

            for mid in sorted(id_to_words):
                date_str, _from, subject = headers.get(mid, ("?", "?", "?"))
                words = ", ".join(id_to_words[mid])
                total_hits += 1
                print(f'  [{date_str}] "{subject}" ({words})')

            print()

        print(
            f"Zusammenfassung: {total_hits} Treffer bei "
            f"{senders_with_hits} von {len(emails_from_list)} Absender(n)."
        )
    finally:
        mail.logout()


if __name__ == "__main__":
    some_suspicious_mails = [
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
    ]
    search_mail_content(some_suspicious_mails, [
        "barclays",
        "transaktion",
        "ING-Kunde",
        "Sprachnachricht erhalten",
        "Daten aktualisieren",
        "Steuererstattung",
        "Speicherlimit"
    ])
