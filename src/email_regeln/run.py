"""Verschiebt Mails aus der INBOX in die passenden filter-andwendungen-Ordner."""

from __future__ import annotations

from email_regeln.move_to_delete import run

ZUORDNUNGEN: dict[str, list[str]] = {
  # TODO next run
}

if __name__ == "__main__":
    for ordner, absender in ZUORDNUNGEN.items():
        print(f"\n--- Verschiebe nach: {ordner} ---")
        run(absender, target_folder=ordner, dry_run=True)
