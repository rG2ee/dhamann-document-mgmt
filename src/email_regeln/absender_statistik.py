"""Liest die INBOX via Protonmail Bridge (IMAP) und gibt eine Absender-Statistik pro Jahr aus."""

from __future__ import annotations

import imaplib
import json
import pprint
from collections import defaultdict
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime
from pathlib import Path

from email_regeln.imap_connection import connect

STATE_DIR = Path("/home/user/alle-freelancer-rechnungen/email-state")
_ABSENDER_FILE = STATE_DIR / "absender_statistik.json"
_HOST_FILE = STATE_DIR / "host_statistik.json"


def _decode_header_value(raw: str) -> str:
    """Dekodiert RFC-2047-kodierte Header-Werte (z.B. =?UTF-8?Q?...?=)."""
    parts: list[str] = []
    for fragment, charset in decode_header(raw):
        if isinstance(fragment, bytes):
            parts.append(fragment.decode(charset or "utf-8", errors="replace"))
        else:
            parts.append(fragment)
    return "".join(parts)


def _fetch_sender_stats(mail: imaplib.IMAP4) -> dict[str, dict[int, int]]:
    """Holt FROM+DATE Header aller INBOX-Nachrichten und aggregiert nach Absender/Jahr."""
    mail.select("INBOX", readonly=True)

    _status, data = mail.search(None, "ALL")
    msg_ids = data[0].split()
    total = len(msg_ids)
    if total == 0:
        return {}

    stats: dict[str, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    batch_size = 200

    for i in range(0, total, batch_size):
        batch = msg_ids[i : i + batch_size]
        id_range = b",".join(batch)
        print(f"  Fetche Nachrichten {i + 1}–{min(i + batch_size, total)} von {total} …")

        _status, response = mail.fetch(
            id_range, "(BODY.PEEK[HEADER.FIELDS (FROM DATE)])"
        )

        for item in response:
            if not isinstance(item, tuple):
                continue
            raw_header = item[1]
            if isinstance(raw_header, bytes):
                raw_header = raw_header.decode("utf-8", errors="replace")

            from_addr = ""
            year = None
            for line in raw_header.splitlines():
                lower = line.lower()
                if lower.startswith("from:"):
                    decoded = _decode_header_value(line[5:].strip())
                    _, from_addr = parseaddr(decoded)
                    from_addr = from_addr.lower()
                elif lower.startswith("date:"):
                    try:
                        dt = parsedate_to_datetime(line[5:].strip())
                        year = dt.year
                    except Exception:
                        pass

            if from_addr and year is not None:
                stats[from_addr][year] += 1

    return stats


def _aggregate_by_host(stats: dict[str, dict[int, int]]) -> dict[str, dict[int, int]]:
    """Gruppiert Absender-Statistiken nach Host/Domain (z.B. example.com)."""
    host_stats: dict[str, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    for addr, yearly in stats.items():
        host = addr.rsplit("@", 1)[-1] if "@" in addr else addr
        for year, count in yearly.items():
            host_stats[host][year] += count
    return host_stats


def _print_table(stats: dict[str, dict[int, int]], *, label: str = "Absender") -> None:
    if not stats:
        print("Keine Nachrichten in der INBOX gefunden.")
        return

    all_years = sorted({y for yearly in stats.values() for y in yearly})
    totals = {addr: sum(yearly.values()) for addr, yearly in stats.items()}
    sorted_addrs = sorted(totals, key=lambda a: totals[a], reverse=True)

    addr_width = max(len(a) for a in sorted_addrs)
    addr_width = max(addr_width, len(label))
    col_w = 6

    header = f"{label:<{addr_width}}"
    for y in all_years:
        header += f" | {y:>{col_w}}"
    header += f" | {'Gesamt':>{col_w}}"
    print(header)

    sep = "-" * addr_width
    for _ in all_years:
        sep += "-+-" + "-" * col_w
    sep += "-+-" + "-" * col_w
    print(sep)

    for addr in sorted_addrs:
        row = f"{addr:<{addr_width}}"
        for y in all_years:
            count = stats[addr].get(y, 0)
            row += f" | {count:>{col_w}}"
        row += f" | {totals[addr]:>{col_w}}"
        print(row)

    print(sep)
    print(f"{'TOTAL':<{addr_width}}", end="")
    for y in all_years:
        year_total = sum(stats[addr].get(y, 0) for addr in sorted_addrs)
        print(f" | {year_total:>{col_w}}", end="")
    grand_total = sum(totals.values())
    print(f" | {grand_total:>{col_w}}")


def _save_stats(
    stats: dict[str, dict[int, int]],
    host_stats: dict[str, dict[int, int]],
) -> None:
    """Speichert Absender- und Host-Statistiken als JSON-Dateien."""
    STATE_DIR.mkdir(exist_ok=True)

    def _serializable(d: dict[str, dict[int, int]]) -> dict[str, dict[str, int]]:
        return {addr: {str(y): c for y, c in yearly.items()} for addr, yearly in d.items()}

    _ABSENDER_FILE.write_text(json.dumps(_serializable(stats), indent=2, ensure_ascii=False, sort_keys=True))
    _HOST_FILE.write_text(json.dumps(_serializable(host_stats), indent=2, ensure_ascii=False, sort_keys=True))
    print(f"Statistiken gespeichert in {STATE_DIR}/")


def _load_stats() -> tuple[dict[str, dict[int, int]], dict[str, dict[int, int]]] | None:
    """Liest Statistiken aus JSON-Dateien. Gibt None zurück wenn die Dateien fehlen."""
    if not _ABSENDER_FILE.exists() or not _HOST_FILE.exists():
        return None

    def _parse(path: Path) -> dict[str, dict[int, int]]:
        raw: dict[str, dict[str, int]] = json.loads(path.read_text())
        return {addr: {int(y): c for y, c in yearly.items()} for addr, yearly in raw.items()}

    return _parse(_ABSENDER_FILE), _parse(_HOST_FILE)


def _inactive_since(stats: dict[str, dict[int, int]], since_year: int = 2023) -> list[str]:
    """Gibt alle Absender zurück, die seit *since_year* (inklusive) keine Mail mehr geschickt haben."""
    return sorted(
        addr
        for addr, yearly in stats.items()
        if max(yearly) < since_year
    )


def main(*, refresh: bool = False) -> None:
    if refresh:
        print("Verbinde mit Protonmail Bridge …")
        mail = connect()
        try:
            print("Lese INBOX …\n")
            stats = _fetch_sender_stats(mail)
            host_stats = _aggregate_by_host(stats)
            _save_stats(stats, host_stats)
        finally:
            mail.logout()
    else:
        cached = _load_stats()
        if cached is None:
            raise SystemExit(
                f"Keine Statistiken gefunden in {STATE_DIR}/.\n"
                "Bitte zuerst mit refresh=True ausführen."
            )
        stats, host_stats = cached
        print(f"Statistiken aus {STATE_DIR}/ geladen.\n")

    print()
    _print_table(stats)

    inactive = _inactive_since(stats, since_year=2023)
    print(f"\n\nAbsender ohne Mails seit 2023 ({len(inactive)}):\n")
    pprint.pprint(inactive)

    print("\n\n--- Statistik nach Host/Domain ---\n")
    _print_table(host_stats, label="Host")

    inactive_hosts = _inactive_since(host_stats, since_year=2023)
    print(f"\n\nHosts ohne Mails seit 2023 ({len(inactive_hosts)}):\n")
    pprint.pprint(inactive_hosts)


if __name__ == "__main__":
    import sys

    main(refresh=True)
