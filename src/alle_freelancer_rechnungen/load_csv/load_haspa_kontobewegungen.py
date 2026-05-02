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
    "Auftragskonto":                    {"dtype": pl.Utf8},
    "Buchungstag":                      {"dtype": pl.Date,    "parse": _parse_german_date},
    "Valutadatum":                      {"dtype": pl.Date,    "parse": _parse_german_date},
    "Buchungstext":                     {"dtype": pl.Utf8},
    "Verwendungszweck":                 {"dtype": pl.Utf8},
    "Glaeubiger ID":                    {"dtype": pl.Utf8},
    "Mandatsreferenz":                  {"dtype": pl.Utf8},
    "Kundenreferenz (End-to-End)":      {"dtype": pl.Utf8},
    "Sammlerreferenz":                  {"dtype": pl.Utf8},
    "Lastschrift Ursprungsbetrag":      {"dtype": pl.Utf8},
    "Auslagenersatz Ruecklastschrift":  {"dtype": pl.Utf8},
    "Beguenstigter/Zahlungspflichtiger": {"dtype": pl.Utf8},
    "Kontonummer/IBAN":                 {"dtype": pl.Utf8},
    "BIC (SWIFT-Code)":                 {"dtype": pl.Utf8},
    "Betrag":                           {"dtype": pl.Float64, "parse": _parse_german_decimal},
    "Waehrung":                         {"dtype": pl.Utf8},
    "Info":                             {"dtype": pl.Utf8},
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

    return df


if __name__ == "__main__":
    df = load_haspa_kontobewegungen_camt52v8(
        "20260502-1238211435-umsatz-camt52v8.CSV"
    )
    print(df)
