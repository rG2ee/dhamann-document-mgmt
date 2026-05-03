import polars as pl

from alle_freelancer_rechnungen.rechnung_constants.rechnungen_2023 import (
    RECHNUNGEN_2023_F_PATHS,
    RECHNUNGEN_2023_BETRAG_STEUERN,
)


def process_rechnungen_constants() -> pl.DataFrame:
    rows = []
    for rechnung_id, datei_pfad in RECHNUNGEN_2023_F_PATHS.items():
        netto, umsatzsteuer = RECHNUNGEN_2023_BETRAG_STEUERN[rechnung_id]
        rows.append({
            "rechnung_id": rechnung_id,
            "datei_pfad": str(datei_pfad),
            "netto": netto,
            "umsatzsteuer": umsatzsteuer,
            "brutto": netto + umsatzsteuer,
        })
    return pl.DataFrame(rows)
