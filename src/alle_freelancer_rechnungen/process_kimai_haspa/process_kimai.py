import polars as pl
from pydantic import BaseModel
import datetime
from decimal import Decimal
from alle_freelancer_rechnungen.load_csv.load_kimai_invoices import load_kimai_history
from alle_freelancer_rechnungen.rechnung_constants.rechnungen_ohne_kontobewegungen import \
    RECHNUNGEN_OHNE_KONTOBEWEGUNGEN


def remove_df_cols(df: pl.DataFrame, column_names: tuple[str, ...]) -> pl.DataFrame:
    return df.drop(*column_names)


def remove_always_unused_colums(df: pl.DataFrame) -> pl.DataFrame:
    always_unused_columns = (
        # always superadmin
        "user",
        # always null
        "comment",
    )

    return remove_df_cols(df, always_unused_columns)



def remove_currently_unused_colums(df: pl.DataFrame) -> pl.DataFrame:
    currently_unused_columns = (
        # may be used for ordering?
        "id",

        # payment date may be used in kimai
        "payment_date",

        # currently unused in further evaluations
        "payment_target",

        # always 30
        "payment_term_days",
    )

    return remove_df_cols(df, currently_unused_columns)




def process_kimai() -> pl.DataFrame:
    df = load_kimai_history()
    df = remove_always_unused_colums(df)
    df = remove_currently_unused_colums(df)

    return df



class KimaiRechnung(BaseModel):
    date: datetime.date
    invoice_number: str
    subtotal: Decimal
    total_price: Decimal
    tax: Decimal
    tax_rate: Decimal
    customer: str
    file: str

    @property
    def keine_bewegung_grund(self) -> str | None:
        related_bewegung = [x for x in RECHNUNGEN_OHNE_KONTOBEWEGUNGEN if x.rechnung_nr == self.invoice_number]
        if len(related_bewegung) == 0:
            return None
        return related_bewegung[0].grund


def missing_pleuger_rechnungen() -> list[KimaiRechnung]:
    return [
        KimaiRechnung(
            date=datetime.date(2023, 1, 2),
            invoice_number="2022-12-LR",
            subtotal=Decimal("7000"),
            total_price=Decimal("7000"),
            tax=Decimal("0"),
            tax_rate=Decimal("0"),
            customer="lemonade research gmbh",
            file = "DennisHamann-2022-12-LR.pdf",
        ),
        KimaiRechnung(
            date=datetime.date(2023, 1, 27),
            invoice_number="2023-01-LR",
            subtotal=Decimal("5880"),
            total_price=Decimal("6997.20"),
            tax=Decimal("1117.20"),
            tax_rate=Decimal("19"),
            customer="lemonade research gmbh",
            file = "DennisHamann-2023-01-LR.pdf",
        ),
    ]


def get_kimai_rechnungen_pydantic() -> list[KimaiRechnung]:
    df_result = process_kimai()
    rows = df_result.select(
        "date",
        "invoice_number",
        "subtotal",
        "total_price",
        "tax",
        "tax_rate",
        "customer",
        "file"
    ).to_dicts()
    return [KimaiRechnung(**row) for row in rows] + missing_pleuger_rechnungen()



if __name__ == '__main__':
    df_result = process_kimai()
    rechnungen = get_kimai_rechnungen_pydantic()

    print(df_result)