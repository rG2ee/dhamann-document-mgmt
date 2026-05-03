from collections import OrderedDict

from alle_freelancer_rechnungen.constants import PROJECT_ROOT


"""
kimai:
+----------+------------------------+
|date      |invoice_number          |
+----------+------------------------+
|2024-02-29|2024-1-lemonade-research|
|2024-02-29|2024-2-gintech-ag       |
|2024-04-17|2024-4-kdw              |
|2024-04-28|2024-3-ownly            |
|2024-05-23|2024-5-kdw              |
|2024-05-29|2024-6-kdw              |
|2024-06-24|2024-7-kdw              |
|2024-07-05|2024-6-kdw-korrektur    |
|2024-07-22|2024-8-kdw              |
|2024-08-15|2024-8-kadewe           |
|2024-10-03|2024-9-kadewe           |
|2024-11-08|2024-10-kadewe          |
|2024-12-06|2024-11-kadewe          |
+----------+------------------------+


+----------+------------------------+
|date      |invoice_number          |
+----------+------------------------+
|2024-02-29|2024-1-lemonade-research| --> erst 2026 bezahlt?

|2024-04-28|2024-3-ownly            |

|2024-02-29|2024-2-gintech-ag       |


# kdw oldco
|2024-04-17|2024-4-kdw              |
|2024-05-23|2024-5-kdw              |
|2024-05-29|2024-6-kdw              |
|2024-06-24|2024-7-kdw              |
|2024-07-05|2024-6-kdw-korrektur    |
|2024-07-22|2024-8-kdw              |

# kdw newco
|2024-08-15|2024-8-kadewe           |
|2024-10-03|2024-9-kadewe           |
|2024-11-08|2024-10-kadewe          |
|2024-12-06|2024-11-kadewe          |
+----------+------------------------+



Kaufhaus des Westens (ab nun vollzeit d.h. andere Steuerklasse??)

2024-4-KDW - 28.560,00 EUR - 25.04.2024 (mit ust)
2024-7-KDW - 28.560,00 EUR - 10.07.2024 (mit ust)
2024-8-KDW - 19.040,00 EUR - 23.08.2024 (mit ust)
"""

RECHNUNGEN_2024 = (

    # wz-fintech gmbh
    "2024-3-ownly"  # 190,40 EUR - 25.04.2024 (mit ust)
    
    # humansign
    "2024-2-gintech-ag" # - 3000 Eur - 22.03.2024 (ohne ust (reverse charging lichtenstein))   ->  Transaktion gematcht
    
    # docu bot
    "2024-1-lemonade-research" # --> erst in 2026 bezahl
    
    # old corp
    "2024-4-kdw", # 4500017604 / (24000,00 / 4560,00 )  15.04.2024 – 31.05.2024   ->  Transaktion gematcht
    "2024-5-kdw", # 450001898 / (24000,00 / 4560,00 )   01.06.2024 – 15.07.2024   ->  Transaktion gematcht (doppelte Zahlunng)
    #"2024-6-kdw", # 4500021811 / (24000,00 / 4560,00 )  01.06.2024 – 15.07.2024
    #"2024-6-kdw-korrektur",
    "2024-7-kdw", # 4500023941  / (24000,00 / 4560,00 ) 16.07.2024 – 31.08.2024  ->  Transaktion gematcht
    #"2024-8-kdw", #  4500027810: / (16000,00 / 3040,00)    01.08.2024 – 31.08.2024 -> Storniert und auf NewCo übertragen



    # kdw newco
    "2024-8-kadewe"  # 4510000552   (01.08.2024 – 31.08.2024)     ->  Transaktion gematcht
    "2024-9-kadewe"  # 4510005924 - 00010  23.09.2024 – 30.09.2024    ->  Transaktion gematcht
    "2024-10-kadewe" # 4510005924 - 00020  01.10.2024 – 31.10.2024  ->  Transaktion gematcht
    "2024-11-kadewe" # 4510005924 - 00030  01.11.2024 – 30.11.2024  ->  Transaktion gematcht
)




PATH_2023 = PROJECT_ROOT / "dokumente" / "rechnungen" / "2024"

"""
"2024-2-gintech-ag" -> 3000,00 0,00
"2024-3-ownly" ->      0160,00 30,40

 "2024-4-kdw"  ->  15.04.2024 – 31.05.2024  24000,00 / 4560,00  
 "2024-5-kdw"  ->  01.06.2024 – 15.07.2024  24000,00 / 4560,00
 "2024-7-kdw", ->  16.07.2024 – 31.08.2024  24000,00 / 4560,00
 
 "2024-8-kadewe -> (16000,00 / 3040,00)
 "2024-9-kadewe" -> (5000,00 / 950,00)
 "2024-10-kadewe" -> (15000,00 / 2850,00)
 "2024-11-kadewe" -> (15000,00 / 2850,00)
 
 
-> kdw 1230h * 1000 = (123000, 23370)
gesamt 2024: 

    netto: 123000 + 3000 + 160 = 126160
    ust = 30,04 + 23370 =    23400,04  


>>> tax_2024 = (35000 + 191000*0.4)
>>> tax_2024
111400.0
>>>

"""
