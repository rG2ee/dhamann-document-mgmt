"""Verschiebt alle Mails bestimmter Absender aus einem Quellordner in einen Zielordner.

Schutzmechanismen (siehe README.md):
  * Gesendete Mails und Entwuerfe werden nie erfasst, weil jede Suche um
    NOT FROM <eigene Adresse> erweitert wird.
  * Sent und Drafts sind als Quellordner gesperrt.
  * Suchbegriffe, die auf die eigene Adresse passen, brechen den Lauf ab.
  * Geloescht wird erst, nachdem das COPY nachweislich erfolgreich war.
"""

from __future__ import annotations

import imaplib
import os
from pathlib import Path

from dotenv import load_dotenv

from email_regeln.imap_connection import connect

TARGET_FOLDER = "Folders/to-be-deleted"

# Aus diesen Ordnern darf nicht sortiert werden: sie enthalten ausschliesslich
# Mails mit der eigenen Adresse im From-Header.
PROTECTED_SOURCE_FOLDERS = frozenset({"Sent", "Drafts"})

# Suchbegriffe ohne @ sind Teilstring-Suchen ueber den ganzen From-Header und
# treffen unterhalb dieser Laenge viel zu breit.
_MIN_SENDER_LENGTH = 6

# Mehr IDs pro COPY/STORE macht die IMAP-Kommandozeile unnoetig lang.
_BATCH_SIZE = 200

# Protonmail liefert zu jedem Konto Aliasse auf diesen Domains. Gesendete Mails
# koennen jede davon im From-Header tragen.
_PROTON_DOMAINS = ("protonmail.com", "protonmail.ch", "pm.me", "proton.me")


def own_address() -> str:
    """Die primaere eigene Mailadresse aus der .env."""
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    return os.environ["IMAP_Username"]


def own_addresses() -> list[str]:
    """Alle Adressen, unter denen eigene Mails verschickt werden.

    Das sind die primaere Adresse, die Protonmail-Aliasse mit gleichem lokalen
    Teil und optional weitere aus ``OWN_ALIASES`` in der .env (kommagetrennt).
    """
    primary = own_address().lower()
    local = primary.split("@")[0]

    adressen = {primary}
    adressen |= {f"{local}@{domain}" for domain in _PROTON_DOMAINS}
    adressen |= {
        alias.strip().lower()
        for alias in os.environ.get("OWN_ALIASES", "").split(",")
        if alias.strip()
    }
    return sorted(adressen)


def validate_absender(absender: list[str], *, target_folder: str = "?") -> None:
    """Prueft die Suchbegriffe auf Muster, die den Sent-Ordner leerraeumen wuerden."""
    eigene = own_addresses()

    for sender in absender:
        needle = sender.strip().lower()
        if not needle:
            raise ValueError(f"Leerer Suchbegriff in der Zuordnung fuer {target_folder}.")

        treffer = next((own for own in eigene if needle in own or own in needle), None)
        if treffer:
            raise ValueError(
                f"Suchbegriff {sender!r} (Ziel {target_folder}) passt auf die eigene "
                f"Adresse {treffer}. Damit wuerde jede gesendete Mail mitverschoben. "
                "Bitte den Eintrag aus der Zuordnung entfernen."
            )

        if "@" not in needle and len(needle) < _MIN_SENDER_LENGTH:
            print(
                f"  WARNUNG: Suchbegriff {sender!r} (Ziel {target_folder}) ist sehr kurz "
                "und wird als Teilstring im gesamten From-Header gesucht."
            )


def _search_by_sender(
    mail: imaplib.IMAP4, sender: str, *, protect_own: bool = True
) -> list[bytes]:
    """Sucht in der aktuell selektierten Mailbox nach Mails eines Absenders.

    Gibt UIDs zurueck. Mit protect_own werden eigene Mails (Sent, Drafts,
    Notizen an sich selbst) vom Ergebnis ausgeschlossen.
    """
    criteria: list[str] = ["FROM", f'"{sender}"']
    if protect_own:
        for own in own_addresses():
            criteria += ["NOT", "FROM", f'"{own}"']

    if all(c.isascii() for c in criteria):
        status, data = mail.uid("SEARCH", None, *criteria)
    else:
        prev_encoding = mail._encoding
        mail._encoding = "utf-8"
        try:
            status, data = mail.uid("SEARCH", "CHARSET", "UTF-8", *criteria)
        finally:
            mail._encoding = prev_encoding

    if status != "OK" or not data or not data[0]:
        return []
    return data[0].split()


def _move_messages(mail: imaplib.IMAP4, uids: list[bytes], target_folder: str) -> int:
    """Verschiebt Nachrichten per UID COPY + STORE \\Deleted + EXPUNGE.

    Bricht ab, bevor etwas geloescht wird, wenn das COPY fehlschlaegt.
    """
    moved = 0
    for start in range(0, len(uids), _BATCH_SIZE):
        chunk = uids[start : start + _BATCH_SIZE]
        id_set = ",".join(uid.decode() for uid in chunk)

        status, response = mail.uid("COPY", id_set, f'"{target_folder}"')
        if status != "OK":
            raise RuntimeError(
                f"COPY nach {target_folder} fehlgeschlagen ({status}: {response!r}). "
                f"Es wurde nichts geloescht ({moved} Mail(s) vorher verschoben)."
            )

        status, response = mail.uid("STORE", id_set, "+FLAGS", "\\Deleted")
        if status != "OK":
            raise RuntimeError(
                f"STORE \\Deleted fehlgeschlagen ({status}: {response!r}). "
                f"Die Mails liegen jetzt zusaetzlich in {target_folder}."
            )

        mail.expunge()
        moved += len(chunk)
    return moved


def run(
    absender: list[str],
    *,
    target_folder: str = TARGET_FOLDER,
    folder: str = "INBOX",
    dry_run: bool = True,
    mail: imaplib.IMAP4 | None = None,
    protect_own: bool = True,
) -> int:
    """Verschiebt alle Mails der gegebenen Absender aus *folder* in den Zielordner.

    Gibt die Gesamtanzahl (gefunden bzw. verschoben) zurueck.
    Wird *mail* uebergeben, wird die Verbindung NICHT geschlossen (Caller verwaltet sie).
    """
    if folder in PROTECTED_SOURCE_FOLDERS:
        raise ValueError(
            f"{folder} ist als Quellordner gesperrt. Dort liegen ausschliesslich "
            "eigene Mails, die von jedem Absender-Filter erfasst wuerden."
        )

    validate_absender(absender, target_folder=target_folder)

    own_connection = mail is None
    if own_connection:
        if dry_run:
            print("=== DRY RUN – es werden keine Mails verschoben ===\n")
        print(f"Verbinde mit Protonmail Bridge … Quelle: {folder}, Ziel: {target_folder}")
        mail = connect()

    try:
        quoted = f'"{folder}"' if " " in folder else folder
        mail.select(quoted, readonly=dry_run)
        total = 0

        for sender in absender:
            uids = _search_by_sender(mail, sender, protect_own=protect_own)
            count = len(uids)

            if count == 0:
                continue

            if dry_run:
                print(f"  {sender}: {count} Mail(s) wuerden verschoben")
                total += count
            else:
                moved = _move_messages(mail, uids, target_folder)
                total += moved
                print(f"  {sender}: {moved} Mail(s) verschoben")

        if own_connection:
            print()
            if dry_run:
                print("Dry-Run abgeschlossen. Mit dry_run=False ausfuehren zum Verschieben.")
            else:
                print(f"Fertig. {total} Mail(s) insgesamt verschoben.")

        return total
    finally:
        if own_connection:
            mail.logout()


def undo(*, dry_run: bool = True) -> None:
    """Verschiebt alle Mails aus Folders/to-be-deleted zurueck in die INBOX."""
    if dry_run:
        print("=== DRY RUN – es werden keine Mails verschoben ===\n")

    print("Verbinde mit Protonmail Bridge …")
    mail = connect()

    try:
        mail.select(TARGET_FOLDER, readonly=dry_run)
        _status, data = mail.uid("SEARCH", None, "ALL")
        uids = data[0].split() if data and data[0] else []

        if not uids:
            print("Keine Mails in Folders/to-be-deleted gefunden.")
            return

        if dry_run:
            print(f"{len(uids)} Mail(s) wuerden zurueck in INBOX verschoben.")
        else:
            moved = _move_messages(mail, uids, "INBOX")
            print(f"{moved} Mail(s) zurueck in INBOX verschoben.")
    finally:
        mail.logout()


if __name__ == '__main__':
    undo(dry_run=True)
