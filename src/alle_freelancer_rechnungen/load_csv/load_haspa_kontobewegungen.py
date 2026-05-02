from pathlib import Path

from src.alle_freelancer_rechnungen.constants import PROJECT_ROOT


def get_haspa_file_path(file_name: str) -> Path:
    return PROJECT_ROOT / "haspa-export" / file_name


def load_haspa_kontobewegungen_camt52v8(file_name: str):
    file_path = get_haspa_file_path("20260502-1238211435-umsatz-camt52v8.CSV")


# dokumente/haspa-export
if __name__ == '__main__':
    pass