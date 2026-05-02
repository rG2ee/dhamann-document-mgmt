import polars as pl

from alle_freelancer_rechnungen.load_csv.load_kimai_invoices import load_kimai_history
# ['id', 'date', 'invoice_number', 'status', 'customer', 'subtotal', 'total_price', 'tax', 'currency', 'tax_rate', 'payment_term_days', 'payment_target', 'payment_date', 'user', 'file', 'account', 'comment']

def remove_df_cols(df: pl.DataFrame, column_names: tuple[str, ...]) -> pl.DataFrame:
    return df


def remove_always_unused_colums(df: pl.DataFrame) -> pl.DataFrame:
    always_unused_columns = (
        # always superadmin
        "user",
        # always null
        "comment",
    )

    return remove_df_cols(always_unused_columns)



def remove_currently_unused_colums(df: pl.DataFrame) -> pl.DataFrame:
    currently_unused_columns = (
        # payment date may be used in kimai
        "payment_date",

        # currently unused in further evaluations
        "payment_target",

        # always 30
        "payment_term_days",
    )

    return remove_df_cols(currently_unused_columns)




def process_kimai() -> pl.DataFrame:
    df = load_kimai_history()
    return df




if __name__ == '__main__':
    df_result = process_kimai()

    print(df_result)