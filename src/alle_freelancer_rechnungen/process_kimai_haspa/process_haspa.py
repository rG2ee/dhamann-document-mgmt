from alle_freelancer_rechnungen.load_csv.load_haspa_kontobewegungen import load_haspa_history
import polars as pl


def filter_dennis_private_ueberweisungen(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(pl.col("kontonummer_iban") == "DE41250100300629948302")



def process_haspa() -> pl.DataFrame:
    df = load_haspa_history()
    df = filter_dennis_private_ueberweisungen(df)


    return df




if __name__ == '__main__':
    process_haspa()