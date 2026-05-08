"""Verschiebt Mails aus der INBOX in die passenden filter-andwendungen-Ordner."""

from __future__ import annotations

from email_regeln.move_to_delete import run

ZUORDNUNGEN: dict[str, list[str]] = {
    "Folders/filter-andwendungen/interactive-brokers": [
        "tradingassistant@interactivebrokers.com",
    ],
    "Folders/filter-andwendungen/dhl-post": [
        "noreply@dhl.de",
    ],
    "Folders/filter-andwendungen/freelancer-agenturen/freelancermap": [
        "noreply@freelancermap.de",
    ],
    "Folders/filter-andwendungen/miles-car-sharing": [
        "invoice@update.miles-mobility.com",
    ],
    "Folders/filter-andwendungen/flink": [
        "hello@news.goflink.com",
        "contact@goflink.com",
    ],
    "Folders/filter-andwendungen/uber": [
        "noreply@uber.com",
    ],
    "Folders/filter-andwendungen/audible": [
        "info@audible.de",
    ],
    "Folders/filter-andwendungen/american-express": [
        "americanexpress@welcome.americanexpress.com",
    ],
    "Folders/filter-andwendungen/netcup": [
        "mail@netcup.de",
        "donotreply@netcup.de",
    ],
    "Folders/filter-andwendungen/booking.com": [
        "noreply@booking.com",
    ],
    "Folders/filter-andwendungen/openai": [
        "noreply@tm.openai.com",
    ],
    "Folders/filter-andwendungen/remarkable": [
        "my@remarkable.com",
    ],
    "Folders/filter-andwendungen/qubes-os": [
        "qubes_os@discoursemail.com",
    ],
}

if __name__ == "__main__":
    for ordner, absender in ZUORDNUNGEN.items():
        print(f"\n--- Verschiebe nach: {ordner} ---")
        run(absender, target_folder=ordner, dry_run=False)
