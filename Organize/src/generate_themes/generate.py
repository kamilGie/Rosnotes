from typing import Iterator
import shutil
from typing import Dict
from typing import List
import multiprocessing
from pathlib import Path
import json
import io
import numpy as np
import fitz
from PIL import Image
from .ThemeGenerator import ThemeGenerator
from src.utils.file_management import get_passwords
from src.build_notebooks.build import insert_template, create_theme_front


def generate_all_sol_paths() -> Iterator[Path]:
    """
    Przechodzi przez katalog './Solutions/' i zwraca posortowane ścieżki do katalogów ćwiczeń,
    pomijając pliki.
    """
    solutions_dir = Path("./Solutions/")
    for set_path in sorted(solutions_dir.iterdir(), key=lambda p: p.name):
        if not set_path.is_dir():
            continue
        for exercise_path in sorted(set_path.iterdir(), key=lambda p: p.name):
            if exercise_path.is_file():
                continue
            yield exercise_path


def overlay_pdf_on_image(doc: fitz.Document, bg_image_path: Path, output_path: Path):
    page = doc.load_page(0)
    zoom = 2
    matrix = fitz.Matrix(zoom, zoom)
    rect = page.rect
    rect.x1 -= 1  # dodawalo jakies biale paski z prawa wiec usuwam
    pix = page.get_pixmap(matrix=matrix, alpha=False, clip=rect)
    pdf_image = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGBA")

    bg = Image.open(bg_image_path).convert("RGBA")

    max_width = bg.width - 40
    max_height = bg.height - 340

    width_ratio = max_width / pdf_image.width
    height_ratio = max_height / pdf_image.height
    ratio = min(width_ratio, height_ratio)

    new_size = (int(pdf_image.width * ratio), int(pdf_image.height * ratio))
    resized_pdf = pdf_image.resize(new_size, Image.Resampling.LANCZOS)

    # Oblicz pozycję
    x_position = (bg.width - resized_pdf.width) // 2  # Wyśrodkowanie poziome
    y_position = 293  # Stała odległość od góry

    # Nałóż i zapisz
    bg.paste(resized_pdf, (x_position, y_position), resized_pdf)
    bg.save(output_path, "png")


def create_desc_img(path: Path, theme: ThemeGenerator, theme_name: str, name: str):
    resources_folder = Path(path / "resources")
    assets_folder = Path(f"Organize/src/assets/")
    background_path = assets_folder / "goodnotes_background.jpeg"

    # rozwiązanie
    solution = fitz.open(path / "resources" / "pdfs" / f"{theme_name}.pdf")
    solution.authenticate(get_passwords(theme_name))
    overlay_pdf_on_image(
        solution, background_path, assets_folder / f"{theme_name}_sol_0.png"
    )
    solution.close()

    # szablon
    template = fitz.open()
    template = insert_template(
        template, theme.starter, resources_folder / f"desc_{path.name}.png", 1, 1
    )
    overlay_pdf_on_image(
        template, background_path, assets_folder / f"{theme_name}_tmpl_0.png"
    )
    template.close()

    # okładka
    front = fitz.open()
    front = create_theme_front(front, theme.starter, name)
    overlay_pdf_on_image(
        front, background_path, assets_folder / f"{theme_name}_name_0.png"
    )
    front.close()


def regenerate_theme(
    theme_name: str,
    updated_sol: list,
    is_init: bool,
    desc_solution: str,
    notebook_name: str,
    no_sol_theme: Path,
):
    try:
        # Ustalanie ścieżki do startera dla danego motywu
        starter = Path("./Organize/src/starters") / f"{theme_name}.pdf"
        theme = ThemeGenerator(starter, get_passwords(theme_name))

        # Wybór rozwiązań do generowania – jeżeli is_init to generujemy wszystkie, w przeciwnym razie używamy updated_sol
        sol_to_generate = generate_all_sol_paths() if is_init else updated_sol
        previous_set = ""
        any_sol_to_generate = any(
            True for _ in (generate_all_sol_paths() if is_init else updated_sol)
        )
        if is_init and not any_sol_to_generate:
            # jesli nie ma zadnych rozwiązań
            png_file = next(Path("./Solutions").rglob("*.png"), None)
            desc_solution = "./Organize/src/assets/no_sol_theme/"
            if png_file:
                shutil.copy(
                    png_file,
                    Path(desc_solution) / "resources" / "desc_no_sol_theme.png",
                )

            sol_to_generate = [Path(desc_solution)]
            # oznaczam ze opis jest bez zadania by móc potem zaaktualizowac przy pierwszym dodaniu
            with open(Path(desc_solution) / "resources" / "active", "w"):
                pass

        for path in sol_to_generate:
            if path.parent.name != previous_set:
                print(
                    f"Generowanie {path.parent.name[:11]}dla motywu: \033[1m{theme_name:15}\033[0m",
                    end="\r",
                    flush=True,
                )
                previous_set = path.parent.name

            resources_path = path / "resources"

            # Wczytywanie pliku z kolorami
            colors_file = resources_path / "source_raw_colors.json"
            if colors_file.exists():
                with open(colors_file, "r") as f:
                    color = json.load(f)
                    theme.source_colors = np.array(color)
            else:
                print(f"\033[33m Ostrzezenie: Plik {colors_file} nie istnieje \033[0m")

            # Otwieranie pliku PDF źródłowego
            pdf_source = resources_path / "pdfs" / "source_raw.pdf"
            if pdf_source.exists():
                with fitz.open(str(pdf_source)) as doc:
                    theme.update_exercise(doc, resources_path / "pdfs")
            else:
                print(f"\033[33m Ostrzezenie: Plik {pdf_source} nie istnieje \033[0m")

        # Jeśli mamy inicjalizację, przetwarzamy opis rozwiązania
        if is_init or no_sol_theme.exists():
            if desc_solution:
                # Jeśli użytkownik podał ścieżkę, sprawdź jej format i dostosuj ją
                if len(desc_solution) > 1 and desc_solution[1] == ".":
                    desc_solution = desc_solution[3:]
                create_desc_img(Path(desc_solution), theme, theme_name, notebook_name)
            else:
                # Jeżeli nie podano opisu, próbujemy wygenerować opis z pierwszego zadania, którego nazwa jest liczbą
                for sol in generate_all_sol_paths():
                    if sol.name.isdigit():
                        create_desc_img(sol, theme, theme_name, notebook_name)
                        break

        return None
    except Exception as e:
        error_msg = f"Error in theme {theme_name}: {e}"
        print(error_msg)
        return error_msg


def generate_themes(
    init_theme: Dict[str, bool],
    updated_sol: List[Path],
    desc_solution: str,
    notebook_name: str,
):
    themes_to_update = []
    for theme, should_init in init_theme.items():
        if get_passwords(theme) is not None:
            themes_to_update.append(
                [theme, updated_sol, should_init, desc_solution, notebook_name]
            )

    no_sol_theme_active = (
        Path("./Organize/src/assets/no_sol_theme/") / "resources" / "active"
    )
    with multiprocessing.Pool() as pool:
        pool.starmap(
            regenerate_theme,
            [
                (
                    theme,
                    updated_sol,
                    should_regenerate,
                    desc_solution,
                    notebook_name,
                    no_sol_theme_active,
                )
                for theme, updated_sol, should_regenerate, desc_solution, notebook_name in themes_to_update
            ],
        )

    if no_sol_theme_active.exists() and updated_sol:
        no_sol_theme_active.unlink()
    print(f"\033[32mPomyslnie wygenerowano motywy!\033[0m { ' ' * 30}", end="\r")
