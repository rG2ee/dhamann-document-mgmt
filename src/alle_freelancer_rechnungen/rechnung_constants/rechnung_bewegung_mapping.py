from pydantic import BaseModel


class VerwendungszweckRechnungMapping(BaseModel):
    rechnung_nr: str
    verwendungszweck: str


VERWENDUNGSZWECK_RECHNUNG_MAPPINGS: list[VerwendungszweckRechnungMapping] = [
    # =========================================================================
    # 2024-3-ownly
    # =========================================================================
    VerwendungszweckRechnungMapping(verwendungszweck="2024-3-ownly - umzugshilfe rg v. 28.4.2024 ", rechnung_nr="2024-3-ownly"),
    # =========================================================================
    # Lemonade Research
    # =========================================================================
    VerwendungszweckRechnungMapping(verwendungszweck="2023-09-lemonade-research ", rechnung_nr="2023-09-lemonade-research"),
    VerwendungszweckRechnungMapping(verwendungszweck="rnr. 2023-10-lemonade-research rdat. 15.11.2023 ", rechnung_nr="2023-10-lemonade-research"),
    VerwendungszweckRechnungMapping(verwendungszweck="2023-11-lemonade-research ", rechnung_nr="2023-11-lemonade-research"),
    VerwendungszweckRechnungMapping(verwendungszweck="rnr. 2023-12-lemonade-research rdat. 31.12.2023 ", rechnung_nr="2023-12-lemonade-research"),
    VerwendungszweckRechnungMapping(verwendungszweck="2024-1-lemonade-research ", rechnung_nr="2024-1-lemonade-research"),
    # =========================================================================
    # Gintech AG
    # =========================================================================
    VerwendungszweckRechnungMapping(verwendungszweck="2023-001-gintech-ag awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2023-001-gintech-ag"),
    VerwendungszweckRechnungMapping(verwendungszweck="2023-002-gintech-ag awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2023-002-gintech-ag"),
    VerwendungszweckRechnungMapping(verwendungszweck="2023-003-gintech-ag awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2023-003-gintech-ag"),
    VerwendungszweckRechnungMapping(verwendungszweck="2023-004-gintech-ag awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2023-004-gintech-ag"),
    VerwendungszweckRechnungMapping(verwendungszweck="2023-005-gintech-ag awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2023-005-gintech-ag"),
    VerwendungszweckRechnungMapping(verwendungszweck="2024-2-gintech-ag awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2024-2-gintech-ag"),
    # =========================================================================
    # Allgeier
    # =========================================================================
    VerwendungszweckRechnungMapping(verwendungszweck="2025-06-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2025-06-allgeier"),
    VerwendungszweckRechnungMapping(verwendungszweck="2025-07-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2025-07-allgeier"),
    VerwendungszweckRechnungMapping(verwendungszweck="2025-08-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2025-08-allgeier"),
    VerwendungszweckRechnungMapping(verwendungszweck="2025-09-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2025-09-allgeier"),
    VerwendungszweckRechnungMapping(verwendungszweck="2025-10-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2025-10-allgeier"),
    VerwendungszweckRechnungMapping(verwendungszweck="2025-11-allgeier 2x awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2025-11-allgeier"),
    VerwendungszweckRechnungMapping(verwendungszweck="2025-11-allgeier 2x awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2025-11-allgeier-spesen"),
    VerwendungszweckRechnungMapping(verwendungszweck="re 2025-12-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2025-12-allgeier"),
    VerwendungszweckRechnungMapping(verwendungszweck="dennis hamann, 2026-01-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2026-01-allgeier"),
    VerwendungszweckRechnungMapping(verwendungszweck="dennis hamann, rechnungsnummer2026-02-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2026-02-allgeier"),
    VerwendungszweckRechnungMapping(verwendungszweck="dennis hamann, 2026-03 awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ", rechnung_nr="2026-03-allgeier"),
    # =========================================================================
    # KaDeWe / KDW
    # =========================================================================
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2024-4-kdw 30.4.2024-leistungszeitraum ab 29.01.24 ", rechnung_nr="2024-4-kdw"),
    # 2024-5-kdw (doppelt bezahlt)
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2024-4-kdw 15.4.2024-leistungszeitraum ab 29.01.24 ", rechnung_nr="2024-5-kdw"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/vk2024-7-kdw 24.6.2024-leistungszeitraum ab 29.01.24 ", rechnung_nr="2024-7-kdw"),
    # 2024-8-kadewe (vier verschiedene Verwendungszwecke -> selbe Rechnung)
    VerwendungszweckRechnungMapping(verwendungszweck="doppelt bezahlte rechnung f\u00fcr bestellung 4510000552 - storno.rechnungsnummer 2024-8-kadewe datum 26.09.2024, 15.17 uhr ", rechnung_nr="2024-8-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2024-8-kdw 22.7.2024-leistungszeitraum ab 29.01.24 ", rechnung_nr="2024-8-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="ust zu po 4510000552 ", rechnung_nr="2024-8-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="am zirkus 2de10117 berlinbetrag:eur 16000,00 entgeltregelung:shar vwz:angebot powerbi, warehousing banf 13270869 uetr: 2a6c22bf-f884-46bb-8a7b-19cdb63df803 erst:cobadeffxxx ", rechnung_nr="2024-8-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2024-9-kadewe 3.10.2024-leistungszeitraum ab 29.01.24 ", rechnung_nr="2024-9-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2024-10-kadewe 8.11.2024-leistungszeitraum ab 29.01.24 ", rechnung_nr="2024-10-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2024-11-kadewe 6.12.2024-leistungszeitraum ab 29.01.24 ", rechnung_nr="2024-11-kadewe"),
    # Jahresbeginn -> falsch benannte Rechnung -> eigentlich 2024-12-kadewe
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2025-12-kadewe 5.1.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-12-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2025-01-kadewe 10.2.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-01-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2025-02-kadewe 4.3.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-02-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2025-03-kadewe 10.4.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-03-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2025-04-kadewe 10.5.2025-leistungszeitraum ab 29.01.24/inv/2025-05-kadewe 3.6.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-04-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2025-04-kadewe 10.5.2025-leistungszeitraum ab 29.01.24/inv/2025-05-kadewe 3.6.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-05-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2025-06-kadewe 29.7.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-06-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2025-07-kadewe 1.9.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-07-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2025-08-kadewe 2.10.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-08-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2025-09-kadewe 13.11.2025-leistungszeitraum ab 29.01.24/inv/2025-10-kadewe 13.11.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-09-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2025-09-kadewe 13.11.2025-leistungszeitraum ab 29.01.24/inv/2025-10-kadewe 13.11.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-10-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/adv/2000065969 9.12.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-09-kadewe-R1"),
    VerwendungszweckRechnungMapping(verwendungszweck="/adv/2000065969 9.12.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-10-kadewe-R1"),
    VerwendungszweckRechnungMapping(verwendungszweck="/adv/2000065969 9.12.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-11-kadewe"),
    VerwendungszweckRechnungMapping(verwendungszweck="/adv/2000065969 9.12.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-12-kadewe-R0"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/25-11-kadewe-r1 24.12.2025-leistungszeitraum ab 29.01.24/inv/25-12-kadewe-r1 24.12.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-11-kadewe-r1"),
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/25-11-kadewe-r1 24.12.2025-leistungszeitraum ab 29.01.24/inv/25-12-kadewe-r1 24.12.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2025-12-kadewe-r1"),
    # =========================================================================
    # KI Rechnungen
    # =========================================================================
    VerwendungszweckRechnungMapping(verwendungszweck="/inv/2024-07-kadewe-k 20.12.2025-leistungszeitraum ab 29.01.24 ", rechnung_nr="2024-07-kadewe-ki"),
]
