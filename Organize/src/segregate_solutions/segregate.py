import shutil
import random
import fitz
from src.utils.file_management import locate_set_folder, save_colors_json
from src.utils.colors import has_result_drawing, get_font_and_colors
from src.utils.page_managment import extract_exercise_info
from typing import List
from pathlib import Path


def create_task_folders(set_number: int, task_number: str, base_path: Path) -> Path:
    set_folder = locate_set_folder(set_number, base_path)
    if set_folder is None:
        raise FileNotFoundError(f"Nie istnieje Folder zestawu: {base_path}")

    task_folder = set_folder / task_number
    resources_folder = task_folder / "resources"
    resources_folder.mkdir(parents=True, exist_ok=True)
    return resources_folder


def process_pdf_pages(
    doc: fitz.Document,
    page_number: int,
    start_page: int,
    exercise_info: str,
    colors: list,
    base_path: Path,
) -> Path:
    # Rozdzielenie informacji – pierwsze 2 znaki to numer zadania, reszta to numer zestawu
    exercise_number, set_number = exercise_info[:2], exercise_info[2:]

    if exercise_number == "th":
        exercise_number = "Teoria"
        print(f"Stworzono Teorie  do zestawu {set_number}")

    # Tworzenie folderów zadania
    resources_folder = create_task_folders(int(set_number), exercise_number, base_path)
    pdfs_folder = resources_folder / "pdfs"
    pdfs_folder.mkdir(exist_ok=True)

    # Obsługa pliku opisu zadania
    desc_path = resources_folder / f"desc_{exercise_number}.png"
    if not desc_path.exists() and exercise_number.isdigit():
        print(
            f"Stworzono zadanie: \033[1m{exercise_number}\033[0m | Zestaw numer: \033[1m{set_number} \033[0m"
        )
        shutil.move(
            resources_folder.parent.parent / f"desc_{exercise_number}.png", desc_path
        )
    elif exercise_number.isdigit():
        for img in resources_folder.glob("solution_*.png"):
            img.unlink()  # Usuwam stare rozwiązanie ( workflow bedzie potem szukal folderu bez zdjec by wygenerwoac nowe )
        print(
            f"Poprawiono zadanie: \033[1m{exercise_number}\033[0m | Zestaw numer: {set_number}"
        )

    # Wyciąganie fragmentu PDF
    exercise_doc = fitz.open()
    exercise_doc.insert_pdf(doc, from_page=start_page, to_page=page_number)
    exercise_doc.ez_save(pdfs_folder / "source_raw.pdf")
    exercise_doc.close()

    # Zapis kolorów
    save_colors_json(colors, resources_folder / "source_raw_colors.json")

    return resources_folder.parent


def segregate_solutions(pdf_path: Path, Sets_to_update: List) -> List[Path]:
    updates_solutions = []
    with fitz.open(pdf_path) as doc:
        colors, _, _ = get_font_and_colors(doc[1])
        start_page = 0
        last_hidden_info = ""
        last_set = 0

        for page_number, page in enumerate(doc):
            # Szukam tagu zadania ktore definiuje do jakiego zadania jest szablon
            rect = fitz.Rect(-10, -10, 50, 50)
            text = page.get_textbox(rect)
            exercise_info = extract_exercise_info(text)

            if exercise_info and exercise_info != last_hidden_info:
                start_page = page_number
                last_hidden_info = exercise_info

            if exercise_info:
                set_number = int(exercise_info[2:]) - 1
                if not Sets_to_update[set_number]:
                    continue
                if set_number != last_set:
                    print(
                        f"Szukanie koloru wyniku w szablonach dla zestawu {set_number}"
                    )
                    if random.randint(1, 8) == 1:
                        print(
                            "Mozesz ograniczyc te wyszukiwanie, odpalajac skrypt z numerami zestawow do pominiecia, np.: python Organize/Organize.py 1 2 4 5"
                        )

                    last_set = set_number

            if exercise_info and has_result_drawing(page, colors):
                updates_solutions.append(
                    process_pdf_pages(
                        doc,
                        page_number,
                        start_page,
                        exercise_info,
                        colors,
                        Path("Solutions/"),
                    ),
                )
    print("\033[32mPomyslnie zaaktualizowano zadania!\033[0m")
    return updates_solutions
