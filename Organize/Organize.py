import sys
from pathlib import Path
from src.segregate_solutions.segregate import segregate_solutions
from src.build_notebooks.build import build_notebooks
from src.generate_themes.generate import generate_themes
from src.utils.file_management import first_use, get_passwords, set_password


class Config:
    # Notebook settings

    # Nazwa przedmiotu
    NOTEBOOK_NAME = "Nazwa przedmiotu"  # Ustaw tu nazwe przedmiotu

    THEMES = [
        "Black",
        "White",
        "Noxus",
        "Tangled",
        "Encrypted_I",
        "Encrypted_II",
        "Encrypted_III",
        "Encrypted_IV",
        "Encrypted_V",
        "Encrypted_VI",
        "Encrypted_VII",
        # Jeśli dodasz nowy motyw, dodaj tutaj nazwę startera
    ]
    # Ścieżka do zadania, które będzie użyte w README i opisie
    DESC_SOLUTION = ""  # Jeśli puste, wybierze pierwsze wykonane


def main(args):

    # Analizuje argumenty użytkownika
    sets_to_update = [True] * len(list(Path("./Solutions/").iterdir()))
    init_theme = {theme: False for theme in Config.THEMES}
    raw_update = False
    for arg in args:
        if arg.casefold() in (theme.casefold() for theme in Config.THEMES):
            init_theme[arg.capitalize()] = True
        elif arg.isdigit():
            sets_to_update[int(arg) - 1] = False
        elif arg.upper() == "INIT":
            init_theme = {theme: True for theme in Config.THEMES}
        elif arg.upper() == "RAW":  # dodaje jedynie zadania
            raw_update = True
        else:
            print(f"\033[33m Nieznana komenda: {arg} \033[0m")

    # Jeżeli jest to pierwsze użycie skryptu przez użytkownika, inicjalizuje domyślne motywy
    if first_use() and not any(init_theme.values()) and not raw_update:
        print("Pierwsze uzycie skryptu, inicjowanie domyslnych motywow...")
        for theme in ["Noxus", "Tangled", "White", "Black"]:
            init_theme[theme] = True

    # Ustawia hasła
    for theme, should_init in init_theme.items():
        if should_init and get_passwords(theme) is None:
            init_theme[theme] = set_password(theme)

    # Wczytuje zeszyt PDF
    pdf_file = list(Path("./Organize").glob("*.pdf"))

    updated_sol = []
    if pdf_file:
        # Segregowanie surowych rozwiązań do folderu Solutions
        updated_sol = segregate_solutions(pdf_file[0], sets_to_update)

    # Jak podano argumenty by tylko dodaz zadania
    if raw_update:
        return

    # Generowanie rozwiązań dla dostępnych motywów
    generate_themes(init_theme, updated_sol, Config.DESC_SOLUTION, Config.NOTEBOOK_NAME)

    # Sklejanie rozwiązań motywów
    build_notebooks(Config.NOTEBOOK_NAME)


if __name__ == "__main__":
    arguments = [] if len(sys.argv) < 2 else sys.argv[1:]
    main(arguments)
