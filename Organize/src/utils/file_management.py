import re
import json
from pathlib import Path
import fitz


def first_use():
    env_path = Path("./Organize/src/env.json")
    # Jeśli plik nie istnieje, utwórz go jako pusty słownik
    if not env_path.exists():
        env_path.parent.mkdir(parents=True, exist_ok=True)
        with open(env_path, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)
        return True
    return False


def get_passwords(theme_name):
    env_path = Path("./Organize/src/env.json")
    # Wczytaj dane z pliku env.json
    # potrzeba hasla jest tylko na poczatku
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            env_data = json.load(f)
    except json.JSONDecodeError:
        env_data = {}

    # Zwróć wartość dla danego theme_name, lub None, jeśli nie istnieje
    return env_data.get(theme_name, None)


def set_password(theme_name):
    env_path = Path("./Organize/src/env.json")

    # Wczytaj dane z pliku env.json
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            env_data = json.load(f)
    except json.JSONDecodeError:
        env_data = {}

    # Ścieżka do pliku PDF dla danego motywu
    pdf_path = Path(f"./Organize/src/starters/{theme_name}.pdf")
    if not pdf_path.exists():
        print(f"Plik PDF '{pdf_path}' nie istnieje.")
        return False

    # Otwieramy dokument PDF
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Nie udalo się otworzyc PDF: {e}")
        return False

    # Sprawdź, czy dokument jest zabezpieczony
    if doc.needs_pass:
        success = False
        for attempt in range(1, 4):
            pwd = input(
                f"Podaj haslo dla motywu {pdf_path.name[:-4]} (proba {attempt}/3): "
            )
            doc = fitz.open(str(pdf_path))
            if doc.authenticate(pwd):
                env_data[theme_name] = pwd
                print("\033[32mHaslo zostalo zapisane.\033[0m")
                success = True
                break
            else:
                print("Niepoprawne haslo.")
        if not success:
            print("\033[31mPrzekroczono liczbę prob.\033[0m")
            return False
    else:
        # Jeśli dokument nie jest zabezpieczony, ustawiamy wartość na True
        env_data[theme_name] = ""

    # Zapisz zaktualizowaną bazę do pliku env.json
    with open(env_path, "w", encoding="utf-8") as f:
        json.dump(env_data, f, indent=4)
    return True


def locate_set_folder(zestaw_numer, base_folder):
    for folder in base_folder.iterdir():
        if folder.is_dir():
            match = re.search(r"\d+", folder.name)
            if match and int(match.group()) == zestaw_numer:
                return folder


def extract_starters_pdfs(folder_path):
    background = []
    folder = Path(folder_path)

    for pdf_file in folder.rglob("*.pdf"):
        doc = fitz.open(pdf_file)
        background.append((pdf_file.name, doc))

    return background


def save_colors_json(colors, path):
    with open(path, "w") as file:
        json.dump(colors, file)
