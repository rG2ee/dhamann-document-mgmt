"""Liest die IMAP-Ordnerstruktur und persistiert sie als JSON in email-state/."""

from __future__ import annotations

import json
from pathlib import Path

from email_regeln.imap_connection import connect, list_folders, _folder_message_count

_STATE_DIR = Path(__file__).resolve().parents[2] / "email-state"
_TREE_FILE = _STATE_DIR / "folder_tree.json"


def _fetch_folder_tree(mail) -> dict[str, int | None]:
    """Holt alle Ordner mit Nachrichtenanzahl via IMAP."""
    folders = list_folders(mail)
    tree: dict[str, int | None] = {}
    for folder in folders:
        tree[folder] = _folder_message_count(mail, folder)
    return tree


def _save_tree(tree: dict[str, int | None]) -> None:
    """Speichert den Folder-Tree als JSON."""
    _STATE_DIR.mkdir(exist_ok=True)
    _TREE_FILE.write_text(json.dumps(tree, indent=2, ensure_ascii=False))
    print(f"Folder-Tree gespeichert in {_TREE_FILE}")


def _load_tree() -> dict[str, int | None] | None:
    """Liest den Folder-Tree aus dem Cache. Gibt None zurueck wenn die Datei fehlt."""
    if not _TREE_FILE.exists():
        return None
    raw = json.loads(_TREE_FILE.read_text())
    return raw


def _print_tree(tree: dict[str, int | None]) -> None:
    """Gibt die Ordnerstruktur als Baum auf stdout aus."""
    for folder, count in tree.items():
        depth = folder.count("/")
        name = folder.rsplit("/", 1)[-1]
        count_str = f" ({count})" if count is not None else ""
        print(f"{'  ' * depth}{name}{count_str}")


def main(*, refresh: bool = False) -> None:
    if refresh:
        print("Verbinde mit Protonmail Bridge …")
        mail = connect()
        try:
            print("Lese Ordnerstruktur …\n")
            tree = _fetch_folder_tree(mail)
            _save_tree(tree)
        finally:
            mail.logout()
    else:
        tree = _load_tree()
        if tree is None:
            raise SystemExit(
                f"Kein Folder-Tree gefunden in {_STATE_DIR}/.\n"
                "Bitte zuerst mit refresh=True ausfuehren."
            )
        print(f"Folder-Tree aus {_TREE_FILE} geladen.\n")

    _print_tree(tree)


if __name__ == "__main__":
    main(refresh=True)
