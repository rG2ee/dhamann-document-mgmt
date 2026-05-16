"""Kopiert/exportiert alle Mails aus All Mail (enthaelt bereits alle Ordner).

Zwei Modi:
  1. IMAP-COPY: Kopiert Mails serverseitig in Backup-Ordner
  2. Lokaler Export: Laedt Mails als .eml-Dateien auf die Festplatte
"""

from __future__ import annotations

import imaplib
import time
from datetime import date
from pathlib import Path

from email_regeln.imap_connection import connect

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
    output_dir: Path,
    *,
    dry_run: bool = True,
) -> int:
    """Laedt alle Mails aus *source_folder* und speichert sie als .eml-Dateien.

    Gibt die Anzahl der exportierten Nachrichten zurueck.
    """
    today = date.today().isoformat()
    safe_name = source_folder.replace(" ", "_")
    folder_dir = output_dir / f"{safe_name}_{today}"

    print(f"\n{'='*60}")
    print(f"Quelle:      {source_folder}")
    print(f"Zielordner:  {folder_dir}")
    print(f"{'='*60}")

    msg_ids = _get_all_msg_ids(mail, source_folder)
    total = len(msg_ids)
    print(f"  {total} Nachrichten gefunden")

    if total == 0:
        return 0

    if dry_run:
        print(f"  [DRY RUN] {total} Nachrichten wuerden exportiert nach {folder_dir}")
        return 0

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
            eml_path = folder_dir / f"{exported:05d}.eml"
            eml_path.write_bytes(raw)

        elapsed = time.monotonic() - t0
        rate = exported / elapsed if elapsed > 0 else 0
        eta = (total - exported) / rate if rate > 0 else 0
        print(
            f"  {exported}/{total} exportiert | {_fmt_bytes(total_bytes)} "
            f"| {_fmt_duration(elapsed)} vergangen, ~{_fmt_duration(eta)} verbleibend"
        )

    elapsed = time.monotonic() - t0
    print(
        f"  Fertig: {exported} Nachrichten ({_fmt_bytes(total_bytes)}) "
        f"exportiert in {_fmt_duration(elapsed)}"
    )
    return exported


def export_all_mail(
    output_dir: str | Path | None = None,
    *,
    dry_run: bool = True,
) -> None:
    """Exportiert All Mail als .eml-Dateien auf die Festplatte."""
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[2] / "backup"
    else:
        output_dir = Path(output_dir)

    if dry_run:
        print("=== DRY RUN – es werden keine Mails exportiert ===")

    print(f"Verbinde mit Protonmail Bridge …")
    print(f"Ausgabeverzeichnis: {output_dir}")
    mail = connect()

    try:
        export_mailbox_to_eml(mail, "All Mail", output_dir, dry_run=dry_run)
    finally:
        mail.logout()


if __name__ == "__main__":
    # copy_all_mail(dry_run=True)
    export_all_mail(dry_run=True, output_dir=Path("/home/user/alle-freelancer-rechnungen/dokumente/backup-mails/inbox-dir-backup"))
