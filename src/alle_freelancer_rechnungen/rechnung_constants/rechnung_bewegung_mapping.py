from pydantic import BaseModel


class VerwendungszweckRechnungMapping(BaseModel):
    rechnung_nr: str
    verwendungszweck: str


CREATE OR REPLACE VIEW v_verwendungszweck_mapping AS
-- =============================================================================
-- 2024-3-ownly
-- =============================================================================
select '2024-3-ownly - umzugshilfe rg v. 28.4.2024 ' as verwendungszweck,
'2024-3-ownly'                               as rechnung_nr
union all
-- =============================================================================
-- Lemonade Research
-- =============================================================================
select '2023-09-lemonade-research ',                              '2023-09-lemonade-research' union all
select 'rnr. 2023-10-lemonade-research rdat. 15.11.2023 ',        '2023-10-lemonade-research' union all
select '2023-11-lemonade-research ',                              '2023-11-lemonade-research' union all
select 'rnr. 2023-12-lemonade-research rdat. 31.12.2023 ',        '2023-12-lemonade-research' union all
select '2024-1-lemonade-research ',                               '2024-1-lemonade-research'  union all
-- =============================================================================
-- Gintech AG
-- =============================================================================
select '2023-001-gintech-ag awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ', '2023-001-gintech-ag' union all
select '2023-002-gintech-ag awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ', '2023-002-gintech-ag' union all
select '2023-003-gintech-ag awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ', '2023-003-gintech-ag' union all
select '2023-004-gintech-ag awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ', '2023-004-gintech-ag' union all
select '2023-005-gintech-ag awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ', '2023-005-gintech-ag' union all
select '2024-2-gintech-ag awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ',   '2024-2-gintech-ag'   union all
-- =============================================================================
-- Allgeier
-- =============================================================================
select '2025-06-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ',    '2025-06-allgeier' union all
select '2025-07-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ',    '2025-07-allgeier' union all
select '2025-08-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ',    '2025-08-allgeier' union all
select '2025-09-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ',    '2025-09-allgeier' union all
select '2025-10-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ',    '2025-10-allgeier' union all
select '2025-11-allgeier 2x awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ', '2025-11-allgeier' union all
select '2025-11-allgeier 2x awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ', '2025-11-allgeier-spesen' union all

select 're 2025-12-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ', '2025-12-allgeier' union all


select 'dennis hamann, 2026-01-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ',                '2026-01-allgeier' union all
select 'dennis hamann, rechnungsnummer2026-02-allgeier awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ', '2026-02-allgeier' union all
select 'dennis hamann, 2026-03 awv-meldepflicht beachten hotline bundesbank (0800) 1234-111 ',                         '2026-03-allgeier' union all
-- =============================================================================
-- KaDeWe / KDW
-- =============================================================================
select '/inv/2024-4-kdw 30.4.2024-leistungszeitraum ab 29.01.24 ',    '2024-4-kdw' union all
-- 2024-5-kdw (doppelt bezahlt)
select '/inv/2024-4-kdw 15.4.2024-leistungszeitraum ab 29.01.24 ',    '2024-5-kdw' union all
select '/inv/vk2024-7-kdw 24.6.2024-leistungszeitraum ab 29.01.24 ',  '2024-7-kdw' union all
-- 2024-8-kadewe (vier verschiedene Verwendungszwecke -> selbe Rechnung)
select 'doppelt bezahlte rechnung f�r bestellung 4510000552 - storno.rechnungsnummer 2024-8-kadewe datum 26.09.2024, 15.17 uhr ', '2024-8-kadewe' union all
select '/inv/2024-8-kdw 22.7.2024-leistungszeitraum ab 29.01.24 ',                                                                '2024-8-kadewe' union all
select 'ust zu po 4510000552 ',                                                                                                   '2024-8-kadewe' union all
select 'am zirkus 2de10117 berlinbetrag:eur 16000,00 entgeltregelung:shar vwz:angebot powerbi, warehousing banf 13270869 uetr: 2a6c22bf-f884-46bb-8a7b-19cdb63df803 erst:cobadeffxxx ', '2024-8-kadewe' union all
select '/inv/2024-9-kadewe 3.10.2024-leistungszeitraum ab 29.01.24 ',  '2024-9-kadewe'  union all
select '/inv/2024-10-kadewe 8.11.2024-leistungszeitraum ab 29.01.24 ', '2024-10-kadewe' union all
select '/inv/2024-11-kadewe 6.12.2024-leistungszeitraum ab 29.01.24 ', '2024-11-kadewe' union all
-- Jahresbeginn -> falsch benannte Rechnung -> eigentlich 2024-12-kadewe
select '/inv/2025-12-kadewe 5.1.2025-leistungszeitraum ab 29.01.24 ',  '2025-12-kadewe' union all
select '/inv/2025-01-kadewe 10.2.2025-leistungszeitraum ab 29.01.24 ', '2025-01-kadewe' union all
select '/inv/2025-02-kadewe 4.3.2025-leistungszeitraum ab 29.01.24 ',  '2025-02-kadewe' union all
select '/inv/2025-03-kadewe 10.4.2025-leistungszeitraum ab 29.01.24 ', '2025-03-kadewe' union all
select '/inv/2025-04-kadewe 10.5.2025-leistungszeitraum ab 29.01.24/inv/2025-05-kadewe 3.6.2025-leistungszeitraum ab 29.01.24 ', '2025-04-kadewe' union all
select '/inv/2025-04-kadewe 10.5.2025-leistungszeitraum ab 29.01.24/inv/2025-05-kadewe 3.6.2025-leistungszeitraum ab 29.01.24 ', '2025-05-kadewe' union all
select '/inv/2025-06-kadewe 29.7.2025-leistungszeitraum ab 29.01.24 ', '2025-06-kadewe' union all
select '/inv/2025-07-kadewe 1.9.2025-leistungszeitraum ab 29.01.24 ',  '2025-07-kadewe' union all
select '/inv/2025-08-kadewe 2.10.2025-leistungszeitraum ab 29.01.24 ', '2025-08-kadewe' union all
select '/inv/2025-09-kadewe 13.11.2025-leistungszeitraum ab 29.01.24/inv/2025-10-kadewe 13.11.2025-leistungszeitraum ab 29.01.24 ', '2025-09-kadewe' union all
select '/inv/2025-09-kadewe 13.11.2025-leistungszeitraum ab 29.01.24/inv/2025-10-kadewe 13.11.2025-leistungszeitraum ab 29.01.24 ', '2025-10-kadewe' union all
select '/adv/2000065969 9.12.2025-leistungszeitraum ab 29.01.24 ',     '2025-09-kadewe-R1' union all
select '/adv/2000065969 9.12.2025-leistungszeitraum ab 29.01.24 ',     '2025-10-kadewe-R1' union all
select '/adv/2000065969 9.12.2025-leistungszeitraum ab 29.01.24 ',     '2025-11-kadewe' union all
select '/adv/2000065969 9.12.2025-leistungszeitraum ab 29.01.24 ',     '2025-12-kadewe-R0' union all
select '/inv/25-11-kadewe-r1 24.12.2025-leistungszeitraum ab 29.01.24/inv/25-12-kadewe-r1 24.12.2025-leistungszeitraum ab 29.01.24 ', '2025-11-kadewe-r1' union all
select '/inv/25-11-kadewe-r1 24.12.2025-leistungszeitraum ab 29.01.24/inv/25-12-kadewe-r1 24.12.2025-leistungszeitraum ab 29.01.24 ', '2025-12-kadewe-r1' union all
-- =============================================================================
-- KI Rechnungen
-- =============================================================================
select '/inv/2024-07-kadewe-k 20.12.2025-leistungszeitraum ab 29.01.24 ', '2024-07-kadewe-ki'
;
