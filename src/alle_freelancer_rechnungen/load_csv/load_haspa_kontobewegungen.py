from collections import OrderedDict
from pathlib import Path
from typing import Callable

import polars as pl

from alle_freelancer_rechnungen.constants import PROJECT_ROOT

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
    "Auftragskonto":                    {"dtype": pl.Utf8,    "target": "auftragskonto"},
    "Buchungstag":                      {"dtype": pl.Date,    "target": "buchungstag",                       "parse": _parse_german_date},
    "Valutadatum":                      {"dtype": pl.Date,    "target": "valutadatum",                       "parse": _parse_german_date},
    "Buchungstext":                     {"dtype": pl.Utf8,    "target": "buchungstext"},
    "Verwendungszweck":                 {"dtype": pl.Utf8,    "target": "verwendungszweck"},
    "Glaeubiger ID":                    {"dtype": pl.Utf8,    "target": "glaeubiger_id"},
    "Mandatsreferenz":                  {"dtype": pl.Utf8,    "target": "mandatsreferenz"},
    "Kundenreferenz (End-to-End)":      {"dtype": pl.Utf8,    "target": "kundenreferenz_end_to_end"},
    "Sammlerreferenz":                  {"dtype": pl.Utf8,    "target": "sammlerreferenz"},
    "Lastschrift Ursprungsbetrag":      {"dtype": pl.Utf8,    "target": "lastschrift_ursprungsbetrag"},
    "Auslagenersatz Ruecklastschrift":  {"dtype": pl.Utf8,    "target": "auslagenersatz_ruecklastschrift"},
    "Beguenstigter/Zahlungspflichtiger": {"dtype": pl.Utf8,   "target": "beguenstigter_zahlungspflichtiger"},
    "Kontonummer/IBAN":                 {"dtype": pl.Utf8,    "target": "kontonummer_iban"},
    "BIC (SWIFT-Code)":                 {"dtype": pl.Utf8,    "target": "bic_swift_code"},
    "Betrag":                           {"dtype": pl.Float64, "target": "betrag",                            "parse": _parse_german_decimal},
    "Waehrung":                         {"dtype": pl.Utf8,    "target": "waehrung"},
    "Info":                             {"dtype": pl.Utf8,    "target": "info"},
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


def _remove_empty_columns(df: pl.DataFrame) -> pl.DataFrame:
    empty_cols = [
        col for col in df.columns
        if df[col].is_null().all() or (df[col].cast(pl.Utf8).fill_null("") == "").all()
    ]
    return df.drop(empty_cols)


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
    dfs = _remove_empty_columns(dfs)
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
