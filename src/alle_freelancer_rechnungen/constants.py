from pathlib import Path

PROJECT_ROOT = Path("/home/user/alle-freelancer-rechnungen") # todo make dynamic


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


if __name__ == '__main__':
    print(len(RECHNUNGEN_2023))