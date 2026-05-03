from alle_freelancer_rechnungen.load_csv.load_haspa_kontobewegungen import load_haspa_history
import polars as pl
from pydantic import BaseModel
import datetime
from decimal import Decimal

def remove_empty_columns(df: pl.DataFrame) -> pl.DataFrame:
    empty_cols = [
        col for col in df.columns
        if df[col].is_null().all() or (df[col].cast(pl.Utf8).fill_null("") == "").all()
    ]
    return df.drop(empty_cols)



def filter_beguenstigter_zahlungspflichtiger_and_kontonummer_iban(
        df: pl.DataFrame,
        beguenstigter_zahlungspflichtiger: str,
        kontonummer_iban: str
) -> pl.DataFrame:
    return df.filter(
        ~((pl.col("beguenstigter_zahlungspflichtiger") == beguenstigter_zahlungspflichtiger)
        & (pl.col("kontonummer_iban") == kontonummer_iban)))



def filter_dennis_private_ueberweisungen(df: pl.DataFrame) -> pl.DataFrame:


    return filter_beguenstigter_zahlungspflichtiger_and_kontonummer_iban(
        df,
        beguenstigter_zahlungspflichtiger="Dennis Hamann",
        kontonummer_iban="DE41250100300629948302"
    )


def filter_finanzamt_ueberweisungen(df: pl.DataFrame) -> pl.DataFrame:

    # aktive Zahlungen
    df = filter_beguenstigter_zahlungspflichtiger_and_kontonummer_iban(
        df,
        beguenstigter_zahlungspflichtiger="Finanzamt Hambug - Am Tierpark",
        kontonummer_iban="DE03200000000020001530"
    )
    # Pfändung
    df = filter_beguenstigter_zahlungspflichtiger_and_kontonummer_iban(
        df,
        beguenstigter_zahlungspflichtiger="Steuerkasse Hamburg",
        kontonummer_iban="DE03200000000020001530"
    )

    # Rückerstattungm
    return filter_beguenstigter_zahlungspflichtiger_and_kontonummer_iban(
        df,
        beguenstigter_zahlungspflichtiger="Freie und Hansestadt Hamburg Steuerkasse Hamburg",
        kontonummer_iban="DE03200000000020001530"
    )




def filter_haspa_kosten(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(
        ~((pl.col("bic_swift_code") == '20050550')
          & (pl.col("kontonummer_iban") == '')))



def filter_null_ueberweisungen(df: pl.DataFrame) -> pl.DataFrame:
    return df.filter(pl.col("betrag") != 0)


def filter_steuerberater_kosten(df: pl.DataFrame) -> pl.DataFrame:
    return filter_beguenstigter_zahlungspflichtiger_and_kontonummer_iban(
        df,
        beguenstigter_zahlungspflichtiger="SHBB StBges. mbH Kiel",
        kontonummer_iban="DE81210900070091231000"
    )


def filter_storno_rechnung_kdw_2024_8(df: pl.DataFrame) -> pl.DataFrame:
    # rueckuberweisung
    df =  df.filter(
        ~((pl.col("verwendungszweck") == 'Doppelt bezahlte Rechnung f�r Bestellung 4510000552 - STORNO.Rechnungsnummer 2024-8-kadewe DATUM 26.09.2024, 15.17 UHR ')
          & (pl.col("beguenstigter_zahlungspflichtiger") == 'KaDeWe GmbH')
          & (pl.col("betrag") == -19040.0)
          ))

    # netto doppelt
    df =  df.filter(
        ~((pl.col("verwendungszweck") == 'Am Zirkus 2DE10117 BerlinBETRAG:EUR 16000,00 ENTGELTREGELUNG:SHAR VWZ:Angebot PowerBI, Warehousing BanF 13270869 UETR: 2a6c22bf-f884-46bb-8a7b-19cdb63df803 ERST:COBADEFFXXX ')
          & (pl.col("beguenstigter_zahlungspflichtiger") == 'KaDeWe GmbH')
          & (pl.col("betrag") == 16000.0)
    ))

    # ust doppel
    return df.filter(
        ~((pl.col("verwendungszweck") == 'UST zu PO 4510000552 ')
          & (pl.col("beguenstigter_zahlungspflichtiger") == 'KaDeWe GmbH')
          & (pl.col("betrag") == 3040.0)
          ))


def process_haspa() -> pl.DataFrame:

    df = load_haspa_history()
    df = filter_dennis_private_ueberweisungen(df)
    df = filter_finanzamt_ueberweisungen(df)
    df = filter_haspa_kosten(df)
    df = filter_null_ueberweisungen(df)
    df = filter_steuerberater_kosten(df)
    df = filter_storno_rechnung_kdw_2024_8(df)


    df = remove_empty_columns(df)

    return df



class HaspaKontobewegung(BaseModel):
    buchungstag: datetime.date
    verwendungszweck: str
    betrag: Decimal
    beguenstigter_zahlungspflichtiger: str


def get_haspa_kontobewegungen_pydantic() -> list[HaspaKontobewegung]:
    df_result = process_haspa()
    rows = df_result.select(
        "buchungstag", "verwendungszweck", "betrag", "beguenstigter_zahlungspflichtiger"
    ).to_dicts()
    return [HaspaKontobewegung(**row) for row in rows]



if __name__ == '__main__':
    df_result = process_haspa()
    print(df_result)
