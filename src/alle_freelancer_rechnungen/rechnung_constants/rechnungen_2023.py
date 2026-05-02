from collections import OrderedDict

from alle_freelancer_rechnungen.constants import PROJECT_ROOT

RECHNUNGEN_2023 = (

    # Pleuger
    "2022-12-LR",
    "2023-01-LR",

    # docu bot
    "2023-09-lemonade-research",
    "2023-10-lemonade-research",
    "2023-11-lemonade-research",
    "2023-12-lemonade-research",

    # human sign
    "2023-001-gintech-ag",
    "2023-002-gintech-ag",
    "2023-003-gintech-ag",
    "2023-004-gintech-ag",
    "2023-005-gintech-ag",
)


PATH_2023 = PROJECT_ROOT / "dokumente" / "rechnungen" / "2023"

RECHNUNGEN_2023_F_PATHS = OrderedDict((

    # Pleuger
    ("2022-12-LR", PATH_2023 / "pleuger" / "DennisHamann-2022-12-LR.pdf"),
    ("2023-01-LR", PATH_2023 / "pleuger" / "DennisHamann-2023-01-LR.pdf"),

    # docu bot
    ("2023-09-lemonade-research", PATH_2023 / "docu-bot" / "2023 - 09 - lemonade - research - Lemonade_Research_GmbH - DocuBot.pdf"),
    ("2023-10-lemonade-research", PATH_2023 / "docu-bot" / "2023 - 10 - lemonade - research - Lemonade_Research_GmbH - DocuBot.pdf"),
    ("2023-11-lemonade-research", PATH_2023 / "docu-bot" / "2023 - 11 - lemonade - research - Lemonade_Research_GmbH - DocuBot.pdf"),
    ("2023-12-lemonade-research", PATH_2023 / "docu-bot" / "2023 - 12 - lemonade - research - Lemonade_Research_GmbH.pdf"),

    # human sign
    ("2023-001-gintech-ag",  PATH_2023 / "human-sign" / "2023 - 001 - gintech - ag.pdf"),
    ("2023-002-gintech-ag",  PATH_2023 / "human-sign" / "2023 - 002 - gintech - ag - Gintech_AG.pdf"),
    ("2023-003-gintech-ag",  PATH_2023 / "human-sign" / "2023 - 003 - gintech - ag - Gintech_AG.pdf"),
    ("2023-004-gintech-ag",  PATH_2023 / "human-sign" / "2023 - 004 - gintech - ag - Gintech_AG.pdf"),
    ("2023-005-gintech-ag",  PATH_2023 / "human-sign" / "2023 - 005 - gintech - ag - Gintech_AG.pdf"),
))

if __name__ == '__main__':
    print(len(RECHNUNGEN_2023_F_PATHS))
