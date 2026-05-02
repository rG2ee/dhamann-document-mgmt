from alle_freelancer_rechnungen.load_csv.load_haspa_kontobewegungen import load_haspa_history
import polars as pl


def filter_beguenstigter_zahlungspflichtiger_and_kontonummer_iban(
        df: pl.DataFrame,
        beguenstigter_zahlungspflichtiger: str,
        kontonummer_iban: str
) -> pl.DataFrame:
    return df.filter(
        (pl.col("beguenstigter_zahlungspflichtiger") != beguenstigter_zahlungspflichtiger)
        & pl.col("kontonummer_iban") != kontonummer_iban)



def filter_dennis_private_ueberweisungen(df: pl.DataFrame) -> pl.DataFrame:
    #return df.filter(pl.col("kontonummer_iban") != "DE41250100300629948302")

    return filter_beguenstigter_zahlungspflichtiger_and_kontonummer_iban(
        df,
        beguenstigter_zahlungspflichtiger="Dennis Hamann",
        kontonummer_iban="DE41250100300629948302"
    )



def filter_finanzamt_ueberweisungen(df: pl.DataFrame) -> pl.DataFrame:
    return filter_beguenstigter_zahlungspflichtiger_and_kontonummer_iban(
        df,
        beguenstigter_zahlungspflichtiger="Dennis Hamann",
        kontonummer_iban="DE03200000000020001530"
    )

    return df.filter(pl.col("kontonummer_iban") != "DE03200000000020001530")



def filter_haspa_kosten(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(
        (pl.col("kontonummer_iban") != "0000000000")
        & (pl.col("betrag") != 0)
    )



"""SHBB StBges. mbH Kiel""","""DE81210900070091231000"""



def process_haspa() -> pl.DataFrame:
    df = load_haspa_history()
    df = filter_dennis_private_ueberweisungen(df)
    df = filter_finanzamt_ueberweisungen(df)
    df = filter_haspa_kosten(df)


    return df




if __name__ == '__main__':
    df_result = process_haspa()
    print(df_result)