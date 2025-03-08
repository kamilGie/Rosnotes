import os
from random import randint
from pathlib import Path
import datetime


def main():
    # Daty
    today = datetime.date.today().strftime("%m-%d")
    time = datetime.datetime.now().time().hour
    print(f"Dzisiejsza data (MM-DD): {today}")

    # Określ folder, z logami
    folder = Path("Organize/src/additional_scripts/main_logs/")

    # Ścieżki do plików: plik odpowiadający dacie oraz plik normal.md
    holiday_file = folder / f"{today}.md"
    normal_file = folder / "special.md" if randint(1, 10) == 7 else folder / "normal.md"
    thursday_file = folder / "czwartek.md"

    # Wybierz plik zastępczy:
    if os.path.exists(holiday_file):
        replacement_file = holiday_file
        print(f"Znaleziono plik dla dzisiejszej daty: {holiday_file}")
    elif 16.0 < time < 24 and datetime.datetime.now().weekday() == 3:
        replacement_file = thursday_file
    elif os.path.exists(normal_file):
        replacement_file = normal_file
        print(f"Nie znaleziono pliku dla daty {today}. Używam {normal_file}")
    else:
        print("Brak pliku. Nie mogę zaktualizować README.md.")
        return

    with open(replacement_file, "r", encoding="utf-8") as f:
        replacement_lines = f.read().splitlines()
    replacement_lines = replacement_lines[:8]
    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_lines = f.read().splitlines()

    new_readme_lines = replacement_lines + readme_lines[8:]
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_readme_lines) + "\n")

    print("Plik README.md został zaktualizowany.")


if __name__ == "__main__":
    main()
