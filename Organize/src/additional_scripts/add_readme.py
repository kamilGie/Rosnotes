import datetime
import random
import fitz
import math
from pathlib import Path
import json


class Themes:
    def __init__(self) -> None:
        env_path = Path("./Organize/src/env.json")
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                self.env_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.env_data = {}

        # Bazowe wagi motywów
        self.theme = {
            "Black": 72,
            "White": 72,
            "Noxus": 20,
            "Tangled": 20,
            "Encrypted_I": 2,
            "Encrypted_II": 2,
            "Encrypted_III": 2,
            "Encrypted_IV": 2,
            "Encrypted_V": 2,
            "Encrypted_VI": 2,
            "Encrypted_VII": 1,
        }

        self.theme = {k: v for k, v in self.theme.items() if k in self.env_data}
        # Modyfikujemy wagi na podstawie aktualnej daty/godziny
        self.apply_weight_modifiers()

    def apply_weight_modifiers(self):
        """Modyfikuje wagi motywów na podstawie specjalnych warunków."""
        now = datetime.datetime.now()

        # Walentynki – Encrypted_III ma 90% szans
        if now.month == 2 and now.day == 14:
            for key in self.theme:
                if key == "Encrypted_III":
                    self.theme[key] = 100  # Przypisujemy wysoką wagę
                else:
                    self.theme[key] = max(
                        1, self.theme[key] // 3
                    )  # Reszta dostaje mniejszą wagę

        # Święta i mikołajki – tylko motywy "Encrypted"
        elif now.month == 12 and now.day in [6, 24, 25, 26]:
            for key in self.theme:
                if not key.startswith("Encrypted"):
                    self.theme[key] = 0  # Inne motywy są wykluczone
                else:
                    self.theme[key] *= 2  # Motywy "Encrypted" mają większą wagę

            # Jak motywy encrypted sa zablokowane
            if all(value == 0 for value in self.theme.values()) and self.theme:
                first_key = next(iter(self.theme))
                self.theme[first_key] = 1

        # Czwartki 16:00 - 24:00 – Encrypted_IV i Encrypted_V mają 10% więcej
        if now.weekday() == 3 and 16 <= now.hour < 24:
            for key in ["Encrypted_IV", "Encrypted_V"]:
                if key in self.theme:
                    self.theme[key] = math.ceil(self.theme[key] * 1.1)

        # Każdy dzień 16:00 - 24:00 – Encrypted_I i Encrypted_VI mają 2% więcej
        if 16 <= now.hour < 24:
            for key in ["Encrypted_I", "Encrypted_VI"]:
                if key in self.theme:
                    self.theme[key] = math.ceil(self.theme[key] * 1.02)

        # Każdy dzień 6:00 - 10:00 – Encrypted_II ma 2% więcej
        if 6 <= now.hour < 10:
            if "Encrypted_II" in self.theme:
                self.theme["Encrypted_II"] = math.ceil(
                    self.theme["Encrypted_II"] * 1.02
                )

    def get_random_theme(self):
        """Losuje motyw na podstawie zmodyfikowanych wag."""
        weighted_themes = [
            (theme, weight) for theme, weight in self.theme.items() if weight > 0
        ]

        if not weighted_themes:
            raise ValueError("Brak dostępnych motywów do wyboru!")

        # Tworzymy listę do losowania na podstawie wag
        choices, weights = zip(*weighted_themes)
        selected_theme = random.choices(choices, weights=weights, k=1)[0]

        return selected_theme, self.env_data.get(selected_theme, "Black")

    def chances_to_appear(self, theme):
        total_weight = sum(self.theme.values())
        theme_weight = self.theme[theme]
        return max(int((theme_weight / total_weight) * 100), 1)


def save_pdf_as_image(pdf_path, output_image_path, password=None, dpi=300):
    try:
        with fitz.open(pdf_path) as doc:
            doc.authenticate(password)
            for i, page in enumerate(doc):

                zoom = dpi / 72
                matrix = fitz.Matrix(zoom, zoom)

                pix = page.get_pixmap(matrix=matrix, alpha=False)
                pix.save(f"{ output_image_path }_{i}.png")
            return len(doc)  # sukcjes zwracam ilosci stron
    except FileNotFoundError:
        return 0


def update_readme(task_folder: Path, images_len: int, theme: str, chances: int):
    readme_path = task_folder / "README.md"
    with readme_path.open("w") as f:
        f.write("""<p align="center">\n""")
        for i in range(images_len):
            f.write(
                f""" <picture>
    <img src="./resources/solution_{i}.png" alt="task {i}" width="550">
 </picture>\n"""
            )
        if "Encrypted" in theme:
            f.write(
                """  <picture>
    <img src="../../..//Organize/src/assets/logo_Encrypted.png" alt="task 0" width="550">
  </picture>"""
            )

        f.write("</p>")
        if chances < 20:
            f.write(
                f"""<p align="center">
  Rozwiązanie pochodzi z motywu <strong>{theme}</strong> i było tylko <strong>{chances}%</strong> że się pojawi!
</p> """
            )


def main():
    for solution_path in Path("Solutions").glob("*/*"):
        if solution_path.is_dir():
            if not (solution_path / "resources" / "solution_0.png").exists():
                print(f"Dodaje readme do zadania {solution_path}")
                T = Themes()
                theme, password = T.get_random_theme()
                chances = T.chances_to_appear(theme)
                print(f"wylosowano motyw {theme} bylo na to {chances}% szans!")
                solution = Path(solution_path)
                resources = solution / "resources"
                pdfs = resources / "pdfs"
                len = save_pdf_as_image(
                    pdfs / f"{theme}.pdf", resources / f"solution", password
                )
                update_readme(solution, len, theme, chances)


if __name__ == "__main__":
    main()
