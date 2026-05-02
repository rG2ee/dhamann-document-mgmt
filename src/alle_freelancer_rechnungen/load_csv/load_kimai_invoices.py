from collections import OrderedDict
from pathlib import Path
from typing import Callable

import polars as pl

from alle_freelancer_rechnungen.constants import PROJECT_ROOT

KIMAI_EXPORT_DIR = PROJECT_ROOT / "dokumente" / "kimai-export"

ColumnSpec = dict[str, pl.DataType | Callable[[pl.Expr], pl.Expr]]


def _normalize_nbsp(expr: pl.Expr) -> pl.Expr:
    """Replace non-breaking spaces (\xa0) with regular spaces."""
    return expr.str.replace_all("\u00a0", " ")


def _cast_to_int(expr: pl.Expr) -> pl.Expr:
    return expr.cast(pl.Int64)


def _cast_to_date(expr: pl.Expr) -> pl.Expr:
    return expr.cast(pl.Date)


KIMAI_XLSX_COLUMNS: OrderedDict[str, ColumnSpec] = OrderedDict({
    "ID":                   {"dtype": pl.Int64,    "target": "id",                 "parse": _cast_to_int},
    "Date":                 {"dtype": pl.Date,     "target": "date",               "parse": _cast_to_date},
    "Invoice number":       {"dtype": pl.Utf8,     "target": "invoice_number"},
    "Status":               {"dtype": pl.Utf8,     "target": "status"},
    "Customer":             {"dtype": pl.Utf8,     "target": "customer",           "parse": _normalize_nbsp},
    "Subtotal":             {"dtype": pl.Float64,  "target": "subtotal"},
    "Total price":          {"dtype": pl.Float64,  "target": "total_price"},
    "Tax":                  {"dtype": pl.Float64,  "target": "tax"},
    "Currency":             {"dtype": pl.Utf8,     "target": "currency"},
    "Tax rate":             {"dtype": pl.Float64,  "target": "tax_rate"},
    "Payment term in days": {"dtype": pl.Int64,    "target": "payment_term_days",  "parse": _cast_to_int},
    "Payment target":       {"dtype": pl.Date,     "target": "payment_target",     "parse": _cast_to_date},
    "Payment date":         {"dtype": pl.Utf8,     "target": "payment_date"},
    "User":                 {"dtype": pl.Utf8,     "target": "user"},
    "File":                 {"dtype": pl.Utf8,     "target": "file"},
    "Account":              {"dtype": pl.Utf8,     "target": "account"},
    "Comment":              {"dtype": pl.Utf8,     "target": "comment"},
})


def get_kimai_file_path(file_name: str) -> Path:
    return KIMAI_EXPORT_DIR / file_name


def _apply_column_parsing(df: pl.DataFrame) -> pl.DataFrame:
    parse_exprs = [
        spec["parse"](pl.col(name)).alias(name)
        for name, spec in KIMAI_XLSX_COLUMNS.items()
        if "parse" in spec and name in df.columns
    ]
    if parse_exprs:
        df = df.with_columns(parse_exprs)
    return df


def _rename_columns(df: pl.DataFrame) -> pl.DataFrame:
    rename_map = {
        name: spec["target"]
        for name, spec in KIMAI_XLSX_COLUMNS.items()
        if "target" in spec and name in df.columns
    }
    return df.rename(rename_map)


def _lowercase_strings(df: pl.DataFrame) -> pl.DataFrame:
    """riffq lowercases SQL string literals, so we match by lowering data too."""
    str_cols = [c for c, dt in zip(df.columns, df.dtypes) if dt == pl.Utf8]
    return df.with_columns(pl.col(c).str.to_lowercase() for c in str_cols)


def load_kimai_invoices(file_name: str) -> pl.DataFrame:
    file_path = get_kimai_file_path(file_name)

    df = pl.read_excel(file_path)

    df = _apply_column_parsing(df)
    df = _rename_columns(df)
    df = _lowercase_strings(df)

    return df


def load_kimai_history() -> pl.DataFrame:
    return load_kimai_invoices("kimai-invoices_20260430151004.xlsx")


if __name__ == "__main__":
    df = load_kimai_history()
    print(df)
