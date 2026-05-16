"""Liest die lokalen JSON-Statistiken und gibt eine gefilterte Übersicht aus.

Filtert nach Jahren und Mindestanzahl Mails und zeigt in der Host-Statistik
die zugehörigen echten E-Mail-Adressen an.
"""

from __future__ import annotations

import json
from pathlib import Path

_STATE_DIR = Path(__file__).resolve().parents[2] / "email-state"
_ABSENDER_FILE = _STATE_DIR / "absender_statistik.json"
_HOST_FILE = _STATE_DIR / "host_statistik.json"

type YearlyStats = dict[str, dict[int, int]]


def _parse_json(path: Path) -> YearlyStats:
    raw: dict[str, dict[str, int]] = json.loads(path.read_text())
    return {addr: {int(y): c for y, c in yearly.items()} for addr, yearly in raw.items()}


def _load_stats() -> tuple[YearlyStats, YearlyStats] | None:
    if not _ABSENDER_FILE.exists() or not _HOST_FILE.exists():
        return None
    return _parse_json(_ABSENDER_FILE), _parse_json(_HOST_FILE)


def _print_table(stats: YearlyStats, *, label: str = "Absender") -> None:
    if not stats:
        print("Keine Daten gefunden.")
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


def _filter_stats(
    stats: YearlyStats,
    *,
    years: list[int] | None = None,
    min_num_mails: int = 1,
) -> YearlyStats:
    """Filtert Statistiken nach Jahren und Mindestanzahl Mails."""
    filtered: YearlyStats = {}
    for addr, yearly in stats.items():
        if years is not None:
            yearly = {y: c for y, c in yearly.items() if y in years}
        if not yearly:
            continue
        total = sum(yearly.values())
        if total >= min_num_mails:
            filtered[addr] = yearly
    return filtered


def _build_host_to_emails(stats: YearlyStats) -> dict[str, list[str]]:
    """Mappt jeden Host auf die zugehörigen echten E-Mail-Adressen."""
    mapping: dict[str, list[str]] = {}
    for addr in stats:
        if "@" in addr:
            host = addr.rsplit("@", 1)[-1]
        else:
            host = addr
        mapping.setdefault(host, []).append(addr)
    return mapping


def _print_host_with_emails(
    host_stats: YearlyStats,
    host_to_emails: dict[str, list[str]],
) -> None:
    """Gibt die Host-Tabelle aus mit den zugehörigen E-Mail-Adressen pro Host."""
    if not host_stats:
        print("Keine Hosts gefunden.")
        return

    all_years = sorted({y for yearly in host_stats.values() for y in yearly})
    totals = {host: sum(yearly.values()) for host, yearly in host_stats.items()}
    sorted_hosts = sorted(totals, key=lambda h: totals[h], reverse=True)

    col_w = 6
    addr_width = max(
        max((len(h) for h in sorted_hosts), default=4),
        max(
            (len(f"  {e}") for emails in host_to_emails.values() for e in emails),
            default=4,
        ),
        len("Host"),
    )

    header = f"{'Host':<{addr_width}}"
    for y in all_years:
        header += f" | {y:>{col_w}}"
    header += f" | {'Gesamt':>{col_w}}"
    print(header)

    sep = "-" * addr_width
    for _ in all_years:
        sep += "-+-" + "-" * col_w
    sep += "-+-" + "-" * col_w
    print(sep)

    for host in sorted_hosts:
        row = f"{host:<{addr_width}}"
        for y in all_years:
            count = host_stats[host].get(y, 0)
            row += f" | {count:>{col_w}}"
        row += f" | {totals[host]:>{col_w}}"
        print(row)

        emails = host_to_emails.get(host, [])
        for email in sorted(emails):
            print(f"  {email}")

    print(sep)
    print(f"{'TOTAL':<{addr_width}}", end="")
    for y in all_years:
        year_total = sum(host_stats[h].get(y, 0) for h in sorted_hosts)
        print(f" | {year_total:>{col_w}}", end="")
    grand_total = sum(totals.values())
    print(f" | {grand_total:>{col_w}}")


def main(
    *,
    years: list[int] | None = None,
    min_num_mails: int = 1,
) -> None:
    cached = _load_stats()
    if cached is None:
        raise SystemExit(
            "Keine Statistiken gefunden. "
            "Bitte zuerst absender_statistik.main(refresh=True) ausführen."
        )
    absender_stats, host_stats = cached

    absender_filtered = _filter_stats(
        absender_stats, years=years, min_num_mails=min_num_mails,
    )
    host_filtered = _filter_stats(
        host_stats, years=years, min_num_mails=min_num_mails,
    )

    parts: list[str] = []
    if years:
        parts.append(f"Jahre={years}")
    if min_num_mails > 1:
        parts.append(f"min_mails={min_num_mails}")
    label = ", ".join(parts) if parts else "alle Daten, kein Filter"
    print(f"[{label}]\n")

    print("--- Absender-Statistik ---\n")
    _print_table(absender_filtered)

    print("\n\n--- Host-Statistik (mit E-Mails) ---\n")
    absender_year_filtered = _filter_stats(absender_stats, years=years, min_num_mails=1)
    host_to_emails_map = _build_host_to_emails(absender_year_filtered)
    _print_host_with_emails(host_filtered, host_to_emails_map)


if __name__ == "__main__":
    main(#years=[2025, 2026],
         min_num_mails=5)
