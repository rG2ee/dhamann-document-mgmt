"""Kopiert/exportiert alle Mails aus All Mail (enthaelt bereits alle Ordner).

Zwei Modi:
  1. IMAP-COPY: Kopiert Mails serverseitig in Backup-Ordner
  2. Lokaler Export: Laedt Mails als .eml-Dateien auf die Festplatte
"""

from __future__ import annotations

import email.policy
import imaplib
import re
import time
from datetime import date
from email import message_from_bytes
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime
from pathlib import Path

from email_regeln.imap_connection import connect, list_folders

BATCH_SIZE = 500


def _fmt_duration(seconds: float) -> str:
    """Formatiert Sekunden als lesbaren String (z.B. '2m 35s')."""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h {m}m {s}s"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"


def _fmt_bytes(n: int) -> str:
    """Formatiert Bytes als lesbaren String (z.B. '1.2 GB')."""
    for unit in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024  # type: ignore[assignment]
    return f"{n:.1f} TB"


_UNSAFE_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_NON_ASCII_CONTROL = re.compile(r'[^\x20-\x7e\x80-\xff]')
_MAX_FILENAME_LEN = 150


def _decode_header_value(raw: str) -> str:
    """Dekodiert RFC-2047-kodierte Header-Werte."""
    parts: list[str] = []
    for fragment, charset in decode_header(raw):
        if isinstance(fragment, bytes):
            parts.append(fragment.decode(charset or "utf-8", errors="replace"))
        else:
            parts.append(fragment)
    return "".join(parts)


def _build_eml_filename(raw_mail: bytes, counter: int) -> str:
    """Baut einen Dateinamen aus Datum, Absender und Betreff der Mail."""
    try:
        msg = message_from_bytes(raw_mail, policy=email.policy.default)
    except Exception:
        return f"{counter:05d}.eml"

    date_str = ""
    try:
        date_raw = msg.get("Date", "")
        if date_raw:
            dt = parsedate_to_datetime(date_raw)
            date_str = dt.strftime("%Y-%m-%d_%H%M")
    except Exception:
        pass

    sender = ""
    try:
        from_raw = msg.get("From", "")
        if from_raw:
            _, addr = parseaddr(from_raw)
            sender = addr.lower().split("@")[0] if addr else ""
    except Exception:
        pass

    subject = ""
    try:
        subj_raw = msg.get("Subject", "")
        if subj_raw:
            subject = _decode_header_value(subj_raw) if isinstance(subj_raw, str) else str(subj_raw)
            subject = subject.strip()
    except Exception:
        pass

    parts = [p for p in (date_str, sender, subject) if p]
    name = "_".join(parts) if parts else str(counter)
    name = _UNSAFE_CHARS.sub("_", name)
    name = _NON_ASCII_CONTROL.sub("", name)
    name = name.encode("ascii", errors="ignore").decode("ascii")
    name = name.replace(" ", "_")
    name = re.sub(r"_+", "_", name).strip("_.")

    if len(name) > _MAX_FILENAME_LEN:
        name = name[:_MAX_FILENAME_LEN]

    return f"{counter:05d}_{name}.eml"


def _create_folder(mail: imaplib.IMAP4, folder: str) -> None:
    """Erstellt einen IMAP-Ordner und abonniert ihn (idempotent)."""
    status, _ = mail.create(folder)
    if status == "OK":
        print(f"  Ordner erstellt: {folder}")
    else:
        print(f"  Ordner existiert bereits: {folder}")
    mail.subscribe(folder)


def _quote_folder(folder: str) -> str:
    """Setzt Ordnernamen in Anfuehrungszeichen falls noetig (z.B. 'All Mail')."""
    if " " in folder and not folder.startswith('"'):
        return f'"{folder}"'
    return folder


def _get_all_msg_ids(mail: imaplib.IMAP4, folder: str) -> list[bytes]:
    """Selektiert *folder* (readonly) und gibt alle Message-IDs zurueck."""
    mail.select(_quote_folder(folder), readonly=True)
    _status, data = mail.search(None, "ALL")
    ids = data[0].split()
    return ids


# ---------------------------------------------------------------------------
# Teil 1: IMAP-COPY
# ---------------------------------------------------------------------------


def copy_mailbox(
    mail: imaplib.IMAP4,
    source_folder: str,
    *,
    dry_run: bool = True,
) -> int:
    """Kopiert alle Mails aus *source_folder* in einen Backup-Ordner.

    Zielordner: ``Folders/backup/<source_folder>_<datum>``

    Gibt die Anzahl der kopierten Nachrichten zurueck.
    """
    today = date.today().isoformat()
    target_folder = f"Folders/backup/{source_folder}_{today}"

    print(f"\n{'='*60}")
    print(f"Quelle:  {source_folder}")
    print(f"Ziel:    {target_folder}")
    print(f"{'='*60}")

    msg_ids = _get_all_msg_ids(mail, source_folder)
    total = len(msg_ids)
    print(f"  {total} Nachrichten gefunden")

    if total == 0:
        return 0

    if dry_run:
        print(f"  [DRY RUN] {total} Nachrichten wuerden kopiert")
        return 0

    _create_folder(mail, target_folder)
    mail.select(_quote_folder(source_folder), readonly=True)

    copied = 0
    t0 = time.monotonic()
    for i in range(0, total, BATCH_SIZE):
        batch = msg_ids[i : i + BATCH_SIZE]
        id_set = b",".join(batch)
        mail.copy(id_set, target_folder)
        copied += len(batch)
        elapsed = time.monotonic() - t0
        rate = copied / elapsed if elapsed > 0 else 0
        eta = (total - copied) / rate if rate > 0 else 0
        print(
            f"  {copied}/{total} kopiert "
            f"({_fmt_duration(elapsed)} vergangen, ~{_fmt_duration(eta)} verbleibend)"
        )

    elapsed = time.monotonic() - t0
    print(f"  Fertig: {copied} Nachrichten kopiert in {_fmt_duration(elapsed)}")
    return copied


def copy_all_mail(*, dry_run: bool = True) -> None:
    """Kopiert All Mail in einen serverseitigen Backup-Ordner."""
    if dry_run:
        print("=== DRY RUN – es werden keine Mails kopiert ===")

    print("Verbinde mit Protonmail Bridge …")
    mail = connect()

    try:
        copy_mailbox(mail, "All Mail", dry_run=dry_run)
    finally:
        mail.logout()


# ---------------------------------------------------------------------------
# Teil 2: Lokaler Export als .eml-Dateien
# ---------------------------------------------------------------------------


def export_mailbox_to_eml(
    mail: imaplib.IMAP4,
    source_folder: str,
    folder_dir: Path,
    *,
    dry_run: bool = True,
) -> int:
    """Laedt alle Mails aus *source_folder* und speichert sie als .eml-Dateien.

    Gibt die Anzahl der exportierten Nachrichten zurueck.
    """
    print(f"\n  {source_folder:<45} ", end="", flush=True)

    try:
        msg_ids = _get_all_msg_ids(mail, source_folder)
    except imaplib.IMAP4.error as exc:
        print(f"FEHLER: {exc}")
        return 0

    total = len(msg_ids)

    if total == 0:
        print("(leer)")
        return 0

    if dry_run:
        print(f"{total} Nachrichten [DRY RUN]")
        return 0

    print(f"{total} Nachrichten → {folder_dir}")
    folder_dir.mkdir(parents=True, exist_ok=True)

    mail.select(_quote_folder(source_folder), readonly=True)

    exported = 0
    total_bytes = 0
    t0 = time.monotonic()
    for i in range(0, total, BATCH_SIZE):
        batch = msg_ids[i : i + BATCH_SIZE]
        id_range = b",".join(batch)
        _status, response = mail.fetch(id_range, "(RFC822)")

        for item in response:
            if not isinstance(item, tuple):
                continue
            exported += 1
            raw = item[1]
            total_bytes += len(raw)
            filename = _build_eml_filename(raw, exported)
            eml_path = folder_dir / filename
            eml_path.write_bytes(raw)

        elapsed = time.monotonic() - t0
        rate = exported / elapsed if elapsed > 0 else 0
        eta = (total - exported) / rate if rate > 0 else 0
        print(
            f"    {exported}/{total} | {_fmt_bytes(total_bytes)} "
            f"| {_fmt_duration(elapsed)} vergangen, ~{_fmt_duration(eta)} verbleibend"
        )

    elapsed = time.monotonic() - t0
    print(
        f"    Fertig: {exported} Nachrichten ({_fmt_bytes(total_bytes)}) "
        f"in {_fmt_duration(elapsed)}"
    )
    return exported


def export_all_folders(
    output_dir: str | Path | None = None,
    *,
    dry_run: bool = True,
) -> None:
    """Exportiert alle IMAP-Ordner als .eml-Dateien mit originaler Ordnerstruktur."""
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[2] / "backup"
    else:
        output_dir = Path(output_dir)

    today = date.today().isoformat()
    base_dir = output_dir / today

    if dry_run:
        print("=== DRY RUN – es werden keine Mails exportiert ===")

    print(f"Verbinde mit Protonmail Bridge …")
    mail = connect()

    try:
        folders = list_folders(mail)
        print(f"{len(folders)} Ordner gefunden")
        print(f"Ausgabeverzeichnis: {base_dir}\n")
        print("=" * 60)

        total_exported = 0
        t0 = time.monotonic()

        for folder in folders:
            safe_path = folder.replace(" ", "_")
            folder_dir = base_dir / safe_path
            total_exported += export_mailbox_to_eml(
                mail, folder, folder_dir, dry_run=dry_run
            )

        elapsed = time.monotonic() - t0
        print("\n" + "=" * 60)
        print(
            f"Gesamt: {total_exported} Nachrichten aus {len(folders)} Ordnern "
            f"in {_fmt_duration(elapsed)}"
        )
    finally:
        mail.logout()


if __name__ == "__main__":
    # copy_all_mail(dry_run=True)
    export_all_folders(dry_run=False, output_dir=Path("/home/user/alle-freelancer-rechnungen/dokumente/backup-mails/inbox-dir-backup"))
