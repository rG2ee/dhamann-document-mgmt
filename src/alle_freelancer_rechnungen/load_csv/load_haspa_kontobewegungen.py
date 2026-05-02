from collections import OrderedDict
from pathlib import Path
from typing import Callable

import polars as pl

from src.alle_freelancer_rechnungen.constants import PROJECT_ROOT

HASPA_EXPORT_DIR = PROJECT_ROOT / "dokumente" / "haspa-export"


def _parse_german_decimal(expr: pl.Expr) -> pl.Expr:
    """'1.380,00' -> 1380.00 / '-16,40' -> -16.40"""
    return (
        expr.str.replace_all(r"\.", "")
        .str.replace(",", ".")
        .cast(pl.Float64)
    )


def _parse_german_date(expr: pl.Expr) -> pl.Expr:
    """'30.04.26' -> date(2026, 4, 30)"""
    return expr.str.to_date("%d.%m.%y")


ColumnSpec = dict[str, pl.DataType | Callable[[pl.Expr], pl.Expr]]

HASPA_CSV_COLUMNS: OrderedDict[str, ColumnSpec] = OrderedDict({
    "Auftragskonto":                    {"dtype": pl.Utf8,    "target": "AUFTRAGSKONTO"},
    "Buchungstag":                      {"dtype": pl.Date,    "target": "BUCHUNGSTAG",                       "parse": _parse_german_date},
    "Valutadatum":                      {"dtype": pl.Date,    "target": "VALUTADATUM",                       "parse": _parse_german_date},
    "Buchungstext":                     {"dtype": pl.Utf8,    "target": "BUCHUNGSTEXT"},
    "Verwendungszweck":                 {"dtype": pl.Utf8,    "target": "VERWENDUNGSZWECK"},
    "Glaeubiger ID":                    {"dtype": pl.Utf8,    "target": "GLAEUBIGER_ID"},
    "Mandatsreferenz":                  {"dtype": pl.Utf8,    "target": "MANDATSREFERENZ"},
    "Kundenreferenz (End-to-End)":      {"dtype": pl.Utf8,    "target": "KUNDENREFERENZ_END_TO_END"},
    "Sammlerreferenz":                  {"dtype": pl.Utf8,    "target": "SAMMLERREFERENZ"},
    "Lastschrift Ursprungsbetrag":      {"dtype": pl.Utf8,    "target": "LASTSCHRIFT_URSPRUNGSBETRAG"},
    "Auslagenersatz Ruecklastschrift":  {"dtype": pl.Utf8,    "target": "AUSLAGENERSATZ_RUECKLASTSCHRIFT"},
    "Beguenstigter/Zahlungspflichtiger": {"dtype": pl.Utf8,   "target": "BEGUENSTIGTER_ZAHLUNGSPFLICHTIGER"},
    "Kontonummer/IBAN":                 {"dtype": pl.Utf8,    "target": "KONTONUMMER_IBAN"},
    "BIC (SWIFT-Code)":                 {"dtype": pl.Utf8,    "target": "BIC_SWIFT_CODE"},
    "Betrag":                           {"dtype": pl.Float64, "target": "BETRAG",                            "parse": _parse_german_decimal},
    "Waehrung":                         {"dtype": pl.Utf8,    "target": "WAEHRUNG"},
    "Info":                             {"dtype": pl.Utf8,    "target": "INFO"},
})


def get_haspa_file_path(file_name: str) -> Path:
    return HASPA_EXPORT_DIR / file_name


def _apply_column_parsing(df: pl.DataFrame) -> pl.DataFrame:
    parse_exprs = [
        spec["parse"](pl.col(name)).alias(name)
        for name, spec in HASPA_CSV_COLUMNS.items()
        if "parse" in spec
    ]
    if parse_exprs:
        df = df.with_columns(parse_exprs)
    return df


def _rename_columns(df: pl.DataFrame) -> pl.DataFrame:
    rename_map = {
        name: spec["target"]
        for name, spec in HASPA_CSV_COLUMNS.items()
        if "target" in spec
    }
    return df.rename(rename_map)


def load_haspa_kontobewegungen_camt52v8(file_name: str) -> pl.DataFrame:
    file_path = get_haspa_file_path(file_name)

    df = pl.read_csv(
        file_path,
        separator=";",
        has_header=True,
        encoding="utf8-lossy",
        infer_schema=False,
    )

    df = _apply_column_parsing(df)
    df = _rename_columns(df)

    return df


def load_multiple_haspa_kontobewegungen_camt52v8(file_names: list[str]) -> pl.DataFrame:
    dfs = pl.concat([load_haspa_kontobewegungen_camt52v8(x) for x in file_names])
    return dfs

def load_haspa_history() -> pl.DataFrame:
    file_names = [
        "20260502-1238211435-umsatz-camt52v8-von2023_05_02bis2024_05_02.CSV",
        "20260502-1238211435-umsatz-camt52v8-von2024_05_03bis2026_05_02.CSV",
    ]
    return load_multiple_haspa_kontobewegungen_camt52v8(file_names)

if __name__ == "__main__":
    df = load_haspa_history()
    print(df)
