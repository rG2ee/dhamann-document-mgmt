import polars as pl
from pydantic import BaseModel
import datetime
from decimal import Decimal
from alle_freelancer_rechnungen.load_csv.load_kimai_invoices import load_kimai_history

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
    return [KimaiRechnung(**row) for row in rows]



if __name__ == '__main__':
    df_result = process_kimai()

    print(df_result)