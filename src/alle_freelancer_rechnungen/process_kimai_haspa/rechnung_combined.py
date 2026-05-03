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


def rechungs_combiner_to_xslx_sheet() -> None:
    rechnungs_combiners = load_rechnungs_combiner()

    for rechnungs_combiner in rechnungs_combiners:
        for kimai_rechnung in rechnungs_combiner.kimai_rechnungen:


            rechnungserstellungsdatum = kimai_rechnung.date
            rechnung_nr = kimai_rechnung.invoice_number
            betrag_ust = kimai_rechnung.tax
            betrag_netto = kimai_rechnung.subtotal
            betrag_brutto = kimai_rechnung.total_price
            # todo later dateipfad = kimai_rechnung.file

            zahlungsdatum = rechnungs_combiner.haspa_bewegung.buchungstag
            betrag_kontobewegung = rechnungs_combiner.haspa_bewegung.betrag



if __name__ == '__main__':

    load_rechnungs_combiner()
