from pydantic import BaseModel


class RechnungOhneKontobewegung(BaseModel):
    rechnung_nr: str
    grund: str


RECHNUNGEN_OHNE_KONTOBEWEGUNGEN: list[RechnungOhneKontobewegung] = [
    RechnungOhneKontobewegung(rechnung_nr="2026-04-allgeier", grund="letzte woche gestellt"),

    # messy abrechungen
    RechnungOhneKontobewegung(rechnung_nr="2024-6-kdw", grund="verrechnet mit 2024-6-kdw-korrektur"),
    RechnungOhneKontobewegung(rechnung_nr="2024-6-kdw-korrektur", grund="verrechnet mit 2024-6-kdw"),
    RechnungOhneKontobewegung(rechnung_nr="2024-8-kdw", grund="umgezogen auf newco 2024-8-kadewe"),

    # unbezahlt, aber ok
    RechnungOhneKontobewegung(rechnung_nr="2026-01-kadewe-r1", grund="letzte woche gestellt"),
    RechnungOhneKontobewegung(rechnung_nr="2026-01-kadewe-r2", grund="letzte woche gestellt"),
    RechnungOhneKontobewegung(rechnung_nr="2026-02-kadewe", grund="letzte woche gestellt"),
    RechnungOhneKontobewegung(rechnung_nr="2026-03-kadewe", grund="letzte woche gestellt"),

]