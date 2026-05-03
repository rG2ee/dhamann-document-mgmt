import pprint
from decimal import Decimal
from pathlib import Path

import polars as pl
from pydantic import BaseModel

from alle_freelancer_rechnungen.process_kimai_haspa.process_haspa import HaspaKontobewegung,get_haspa_kontobewegungen_pydantic
from alle_freelancer_rechnungen.process_kimai_haspa.process_kimai import KimaiRechnung, get_kimai_rechnungen_pydantic
from alle_freelancer_rechnungen.rechnung_constants.rechnung_bewegung_mapping import VerwendungszweckRechnungMapping,VERWENDUNGSZWECK_RECHNUNG_MAPPINGS


class RechnungCombiner(BaseModel):

    kimai_rechnungen: list[KimaiRechnung]

    # der einzige Fall in dem es hier eine Liste wäre ist die messy Storno Rechnnung 2024-8-kdw
    haspa_bewegung: HaspaKontobewegung
    verwendungszweck_mappers: list[VerwendungszweckRechnungMapping]


    def validate_no_reason_kimais(self):
        for kimai_rechnung in self.kimai_rechnungen:
            assert kimai_rechnung.keine_bewegung_grund is None, kimai_rechnung

    def validate_betrag(self):
        betrag_kimai =  sum([x.total_price for x in self.kimai_rechnungen])

        # this 20Eur typo is ok..
        if (betrag_kimai == 2866) and ( self.haspa_bewegung.betrag == 2886) and self.kimai_rechnungen[0].invoice_number == '2023-005-gintech-ag':
            return

        assert betrag_kimai == self.haspa_bewegung.betrag


def load_rechnungs_combiner() -> list[RechnungCombiner]:
    kimai_rechnungen = get_kimai_rechnungen_pydantic()
    haspa_bewegungen = get_haspa_kontobewegungen_pydantic()


    remaining_kimai_rechnungen = kimai_rechnungen

    rechnung_combiners: list[RechnungCombiner] = []

    for haspa_bewegung in haspa_bewegungen:
        verwendungszweck_mapper = [x for x in VERWENDUNGSZWECK_RECHNUNG_MAPPINGS if x.verwendungszweck.lower() == haspa_bewegung.verwendungszweck.lower()]
        related_rechnung_nrs = [x.rechnung_nr for x in verwendungszweck_mapper]
        related_kimai_rechnungen = [x for x in remaining_kimai_rechnungen if x.invoice_number in related_rechnung_nrs]
        remaining_kimai_rechnungen = [x for x in remaining_kimai_rechnungen if x.invoice_number not in related_rechnung_nrs]


        rechnung_combiner = RechnungCombiner(
            haspa_bewegung=haspa_bewegung,
            kimai_rechnungen=related_kimai_rechnungen,
            verwendungszweck_mappers=verwendungszweck_mapper
        )

        rechnung_combiners.append(rechnung_combiner)

    for rechnung_combiner in rechnung_combiners:
        rechnung_combiner.validate_no_reason_kimais()
        rechnung_combiner.validate_betrag()


    remaining_reasons = [(x.invoice_number ,x.keine_bewegung_grund) for x in remaining_kimai_rechnungen]

    return rechnung_combiners


XLSX_OUTPUT_PATH = Path(__file__).parents[3] / "rechnungsuebersicht.xlsx"


def yearly_checker() -> None:

    rechnungs_combiners = load_rechnungs_combiner()

    years = {
        2023: {
            "brutto": Decimal("0"),
            "netto": Decimal("0"),
            "ust": Decimal("0"),
        },
        2024: {
            "brutto": Decimal("0"),
            "netto": Decimal("0"),
            "ust": Decimal("0"),
        },
        2025: {
            "brutto": Decimal("0"),
            "netto": Decimal("0"),
            "ust": Decimal("0"),
        },
        2026: {
            "brutto": Decimal("0"),
            "netto": Decimal("0"),
            "ust": Decimal("0"),
        }
    }

    for rechnungs_combiner in rechnungs_combiners:
        for kimai_rechnung in rechnungs_combiner.kimai_rechnungen:

            year = kimai_rechnung.date.year

            years[year]["brutto"]  += kimai_rechnung.total_price
            years[year]["netto"] += kimai_rechnung.subtotal
            years[year]["ust"] += kimai_rechnung.tax

            assert years[year]["brutto"]  == years[year]["netto"] + years[year]["ust"]

    total = {
        "brutto": Decimal("0"),
        "netto": Decimal("0"),
        "ust": Decimal("0"),
    }

    for values in years.values():
        total["brutto"] += values["brutto"]
        total["netto"] += values["netto"]
        total["ust"] += values["ust"]

    years["total"] = total

    pprint.pprint(years)




def rechungs_combiner_to_xslx_sheet() -> Path:
    rechnungs_combiners = load_rechnungs_combiner()

    rows: list[dict] = []
    for rechnungs_combiner in rechnungs_combiners:
        for kimai_rechnung in rechnungs_combiner.kimai_rechnungen:
            rows.append({
                "rechnungserstellungsdatum": kimai_rechnung.date,
                "rechnung_nr": kimai_rechnung.invoice_number,
                "kunde": kimai_rechnung.customer,
                "betrag_ust": float(kimai_rechnung.tax),
                "betrag_netto": float(kimai_rechnung.subtotal),
                "betrag_brutto": float(kimai_rechnung.total_price),
                "zahlungsdatum": rechnungs_combiner.haspa_bewegung.buchungstag,
                "betrag_kontobewegung": float(rechnungs_combiner.haspa_bewegung.betrag),
            })

    df = pl.DataFrame(rows)
    df.write_excel(XLSX_OUTPUT_PATH)
    print(f"XLSX geschrieben: {XLSX_OUTPUT_PATH}")
    return XLSX_OUTPUT_PATH


if __name__ == '__main__':
    #yearly_checker()
    rechungs_combiner_to_xslx_sheet()
