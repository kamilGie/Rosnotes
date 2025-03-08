import re
import unicodedata
import random
import fitz
import os
import multiprocessing
from functools import partial
from pathlib import Path
from ..utils.colors import get_font_and_colors
from src.utils.pdfs_managment import get_available_pdfs


def create_theme_desc(doc: fitz.Document, starter, theme_name):
    content_path = Path(f"Organize/src/assets/")
    tmpl_path = content_path / f"{theme_name}_tmpl_0.png"
    sol_path = content_path / f"{theme_name}_sol_0.png"
    doc.insert_pdf(starter, from_page=16, to_page=19)
    first_page = doc[-4]

    rect_tmpl = fitz.Rect(13, 110, 170, 315)
    rect_sol = fitz.Rect(285, 110, 445, 315)

    first_page.insert_image(rect_tmpl, filename=tmpl_path)
    first_page.insert_image(rect_sol, filename=sol_path)
    return doc


def insert_template(output_doc, theme_doc, content_path, task_number, set_number):
    page_seed = random.randint(4, 8)
    page_count_before = len(output_doc)
    output_doc.insert_pdf(theme_doc, from_page=page_seed, to_page=page_seed)

    # Index of the newly inserted page:
    new_page_index = page_count_before
    # Retrieve the page for modification
    page = output_doc[new_page_index]

    rect = page.rect

    horizontal_margin = rect.width * 0.03
    top_margin = rect.height * 0.02

    pixmap = fitz.Pixmap(content_path)
    image_width = pixmap.width
    image_height = pixmap.height

    available_width = rect.width - (2 * horizontal_margin)
    scale_factor = available_width / image_width

    scaled_height = image_height * scale_factor
    adjusted_x0 = rect.x0 + horizontal_margin
    adjusted_x1 = rect.x1 - horizontal_margin
    adjusted_y0 = rect.y0 + top_margin
    adjusted_y1 = adjusted_y0 + scaled_height

    img_rect = fitz.Rect(adjusted_x0, adjusted_y0, adjusted_x1, adjusted_y1)

    page.insert_image(img_rect, filename=content_path)

    hidden_text = f"@HIDDEN:{task_number}{(set_number):02}"
    page.insert_text(
        (20, 20),
        hidden_text,
        fontname="helv",
        fontsize=1,
        color=(1, 1, 1),
        fill_opacity=0.0,
    )

    return output_doc


def create_theme_front(doc, starter, name):
    doc.insert_pdf(starter, from_page=2, to_page=2)  # okladka
    page = doc[-1]  # pobranie ostatniej strony
    text = starter[1].get_text("text")
    # Podziel tekst na linie
    lines = text.splitlines()
    title_color = (1, 1, 1)
    title_height = 0.4
    for line in lines:
        if "Kolor:" in line:
            numbers_str = line.replace("Kolor: ", "").strip("()")
            numbers_list = numbers_str.split(",")
            title_color = tuple(map(int, numbers_list))
        if "Wysokości:" in line:
            title_height = int(line[11:])

    page_rect = page.rect
    textbox_width = 450
    textbox_height = 50
    left = (page_rect.width - textbox_width) / 2
    top = page_rect.height * title_height / 100
    rect = fitz.Rect(left, top, left + textbox_width, top + textbox_height)

    page.insert_font(fontname="arial", fontfile="./Organize/src/assets/fonts/arial.ttf")
    page.insert_textbox(
        rect, name, fontsize=20, fontname="arial", align=1, color=title_color
    )
    return doc


def create_notebook(starter_path, image_folders, name, password):
    background_doc = fitz.open(starter_path)

    if not background_doc.authenticate(password):
        return

    theme_name = starter_path.stem
    output_pdf_path = f"./Notebooks/Rosnotes {name}-{theme_name}.pdf"

    colors, font_name, font_path = get_font_and_colors(background_doc[16])

    output_doc = fitz.open()
    output_doc = create_theme_front(output_doc, background_doc, name)
    output_doc = create_theme_desc(output_doc, background_doc, theme_name)

    for i, image_folder in enumerate(image_folders):
        print(
            f"Budowanie rozwiazan motywu: \033[1m{theme_name}\033[0m | Zestaw numer: \033[1m{i+1}\033[0m        ",
            end="\r",
            flush=True,
        )

        cover_index = 21
        output_doc.insert_pdf(
            background_doc, from_page=cover_index, to_page=cover_index
        )

        cover_page = output_doc[-1]
        page_width = cover_page.rect.width
        page_height = cover_page.rect.height
        cover_page_name = image_folder.name
        if "Zadania" in cover_page_name or "Zestaw" in cover_page_name:
            cover_page_name = re.sub(
                r"(?:Zadania|Zestaw) \d+\s*-?", "", cover_page_name
            )
        cover_page_name = cover_page_name.strip().capitalize()
        cover_page_name = unicodedata.normalize("NFC", cover_page_name)

        cover_page.insert_font(fontname=font_name, fontfile=font_path)

        rect1 = fitz.Rect(
            0,
            page_height * 0.35 - 100,
            page_width,
            page_height * 0.35 + 100,
        )

        glow_color = colors[2]

        offsets = [
            (-1, -1),
            (1, -1),
            (-1, 1),
            (1, 1),
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
        ]

        # Tworzenie poświaty dla numeru zadania
        for dx, dy in offsets:
            glow_rect = fitz.Rect(
                rect1.x0 + dx, rect1.y0 + dy, rect1.x1 + dx, rect1.y1 + dy
            )
            cover_page.insert_textbox(
                glow_rect,
                f"{i+1}",
                fontname=font_name,
                fontsize=90,
                color=glow_color,
                align=1,
            )

        # Właściwy numer zadania na wierzchu (biały kolor)
        cover_page.insert_textbox(
            rect1,
            f"{i+1}",
            fontname=font_name,
            fontsize=90,
            color=(1, 1, 1),  # Biały kolor (RGB)
            align=1,
        )

        rect2 = fitz.Rect(
            page_width * 0.1,
            page_height * 0.25 + 100,
            page_width * 0.9,
            page_height * 0.25 + 400,
        )
        glow_color = colors[1]

        offsets = [
            (-1, -1),
            (1, -1),
            (-1, 1),
            (1, 1),
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
        ]

        for dx, dy in offsets:
            glow_rect = fitz.Rect(
                rect2.x0 + dx, rect2.y0 + dy, rect2.x1 + dx, rect2.y1 + dy
            )

            cover_page.insert_textbox(
                glow_rect,
                cover_page_name,
                fontname=font_name,
                fontsize=30,
                color=glow_color,
                align=1,
            )
        cover_page.insert_textbox(
            rect2,
            cover_page_name,
            fontname=font_name,
            fontsize=30,
            color=(1, 1, 1),
            align=1,
        )
        folder_items = sorted(os.listdir(image_folder))

        if "Teoria" not in folder_items:
            page_seed = random.randint(4, 8)
            output_doc.insert_pdf(
                background_doc, from_page=page_seed, to_page=page_seed
            )
            theory_page = output_doc[-1]
            page_width = theory_page.rect.width
            page_height = theory_page.rect.height
            theory_page.insert_font(fontname=font_name, fontfile=font_path)
            rect1 = fitz.Rect(
                0,
                page_height * 0.03,
                page_width,
                page_height * 0.03 + 100,
            )
            theory_page.insert_textbox(
                rect1,
                "Teoria",
                fontname=font_name,
                fontsize=25,
                color=colors[2],
                align=1,
            )
            hidden_text = f"@HIDDEN:th{i+1}"
            theory_page.insert_text(
                (20, 20),
                hidden_text,
                fontname="helv",
                fontsize=1,
                color=(1, 1, 1),
                fill_opacity=0.0,
            )
        else:
            theory_pdf_path = os.path.join(
                image_folder, "Teoria", "resources", "pdfs", f"{ theme_name }.pdf"
            )
            theory_pdf = fitz.open(theory_pdf_path)
            theory_pdf.authenticate(password)
            output_doc.insert_pdf(theory_pdf, from_page=0, to_page=-1)

        page_seed = random.randint(4, 8)
        output_doc.insert_pdf(background_doc, from_page=page_seed, to_page=page_seed)

        for item in folder_items:
            item_path = os.path.join(image_folder, item)

            if item.isdigit():
                task_number = item
                content_path = os.path.join(item_path, "resources", f"desc_{item}.png")
                solution_pdf_path = os.path.join(
                    item_path, "resources", "pdfs", f"{theme_name}.pdf"
                )
            elif item.startswith("desc_"):
                task_number = item[-6:-4]
                content_path = item_path
                solution_pdf_path = None
            else:
                continue

            output_doc = insert_template(
                output_doc, background_doc, content_path, task_number, i + 1
            )

            if solution_pdf_path and os.path.exists(solution_pdf_path):
                try:
                    solution_doc = fitz.open(solution_pdf_path)
                    solution_doc.authenticate(password)
                    output_doc.insert_pdf(solution_doc, from_page=0, to_page=-1)
                    solution_doc.close()
                except Exception as e:
                    print(f"Error while reading {solution_pdf_path}: {e}")

        page_seed = random.randint(4, 8)
        output_doc.insert_pdf(background_doc, from_page=page_seed, to_page=page_seed)
    bgc_len = len(background_doc)
    output_doc.insert_pdf(background_doc, from_page=bgc_len, to_page=bgc_len)
    background_doc.close()
    output_path = Path(output_pdf_path)
    try:
        output_doc.save(
            output_path,
            encryption=fitz.PDF_ENCRYPT_AES_256,
            user_pw=password,
            owner_pw=password,
            deflate=True,
            garbage=4,
        )
        output_doc.close()

    except Exception as e:
        print(f"Blad podczas zapisywania {output_path}: {e}")
        return


def process_task(pdf_path, password, subfolders, name):
    subfolders = [Path(sub) for sub in subfolders]
    create_notebook(pdf_path, subfolders, name, password)


def build_notebooks(name):
    base_folder = Path("./Solutions/")
    # Konwertujemy Path na stringi, aby uniknąć potencjalnych problemów
    subfolders = [str(folder) for folder in base_folder.iterdir() if folder.is_dir()]

    def extract_last_number(name):
        numbers = re.findall(r"\d+", name)
        return int(numbers[-1]) if numbers else 0

    subfolders.sort(key=lambda x: extract_last_number(Path(x).name))

    pdf_paths = list(Path("./Organize/src/starters/").rglob("*.pdf"))
    tasks = get_available_pdfs(pdf_paths)

    # Worker przekazujemy tylko proste typy; wewnątrz process_task odtwórz np. Path z stringa
    worker = partial(process_task, subfolders=subfolders, name=name)
    print()  # aby zrobic nowa linie
    with multiprocessing.Pool() as pool:
        pool.starmap(worker, tasks)

    print(f"\033[32mPomyslnie zbudowano zeszyty!\033[0m { ' ' * 30} ")


if __name__ == "__main__":
    # do testów
    theme = input("Podaj nazwe zeszytu do wygenerowania")
    build_notebooks(theme)
