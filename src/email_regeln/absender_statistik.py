"""Liest die INBOX via Protonmail Bridge (IMAP) und gibt eine Absender-Statistik pro Jahr aus."""

from __future__ import annotations

import imaplib
import os
import ssl
from collections import defaultdict
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime
from pathlib import Path

from dotenv import load_dotenv


def _decode_header_value(raw: str) -> str:
    """Dekodiert RFC-2047-kodierte Header-Werte (z.B. =?UTF-8?Q?...?=)."""
    parts: list[str] = []
    for fragment, charset in decode_header(raw):
        if isinstance(fragment, bytes):
            parts.append(fragment.decode(charset or "utf-8", errors="replace"))
        else:
            parts.append(fragment)
    return "".join(parts)


def _connect() -> imaplib.IMAP4:
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(env_path)

    host = os.environ["IMAP_Address"]
    port = int(os.environ["IMAP_port"])
    username = os.environ["IMAP_Username"]
    password = os.environ["IMAP_Password"]

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    mail = imaplib.IMAP4(host, port)
    mail.starttls(ssl_context=ctx)
    mail.login(username, password)
    return mail


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


def _print_table(stats: dict[str, dict[int, int]]) -> None:
    if not stats:
        print("Keine Nachrichten in der INBOX gefunden.")
        return

    all_years = sorted({y for yearly in stats.values() for y in yearly})
    totals = {addr: sum(yearly.values()) for addr, yearly in stats.items()}
    sorted_addrs = sorted(totals, key=lambda a: totals[a], reverse=True)

    addr_width = max(len(a) for a in sorted_addrs)
    addr_width = max(addr_width, len("Absender"))
    col_w = 6

    header = f"{'Absender':<{addr_width}}"
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


def main() -> None:
    print("Verbinde mit Protonmail Bridge …")
    mail = _connect()
    try:
        print("Lese INBOX …\n")
        stats = _fetch_sender_stats(mail)
        print()
        _print_table(stats)
    finally:
        mail.logout()


if __name__ == "__main__":
    main()
