import polars as pl

from alle_freelancer_rechnungen.load_csv.load_kimai_invoices import load_kimai_history


def process_kimai() -> pl.DataFrame:
    df = load_kimai_history()
    return df




if __name__ == '__main__':
    df_result = process_kimai()

    print(df_result)