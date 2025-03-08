import fitz
import unicodedata
import numpy as np
from functools import lru_cache
import random
import os
from src.utils.colors import decode_color, get_font_and_colors, normalize_color


class ThemeGenerator:
    def __init__(self, starter_path, password) -> None:
        self.password = password
        self.starter = fitz.open(starter_path)
        if not self.starter.authenticate(password):
            raise ValueError(f"Błędne hasło do pliku: {starter_path.name}")
        self.theme = starter_path.name
        self.theme_color = starter_path.parent.name
        self.source_colors = np.array([0, 0, 0])
        self.colors, self.font_name, self.font_path = get_font_and_colors(
            self.starter[16]
        )
        self._font_scaling = (
            0.85
            if self.font_name in ("Classic", "Pixel", "sot", "kings", "GOT")
            else 1.0
        )

    def get_template_doc(self):
        page_seed = random.randint(4, 8)
        return self.starter[page_seed]

    def update_exercise(self, exercise_doc: fitz.Document, pdfs_folder_path):

        theme_doc = fitz.open()
        self.color_reverser(theme_doc, exercise_doc)

        for page in theme_doc:

            hidden_text = "@DONE"
            page.insert_text(
                (20, 20),
                hidden_text,
                fontname="helv",
                fontsize=1,
                color=(1, 1, 1),
                fill_opacity=0.0,
            )
        output_path = os.path.join(pdfs_folder_path, self.theme)
        theme_doc.save(
            output_path,
            encryption=fitz.PDF_ENCRYPT_AES_256,
            user_pw=self.password,
            owner_pw=self.password,
            garbage=4,
        )
        theme_doc.close()

    def __del__(self) -> None:
        self.starter.close()

    @lru_cache(maxsize=512)
    def find_closest_color(self, original_color):
        original_np = np.array(original_color)
        distances = np.linalg.norm(self.source_colors - original_np, axis=1)
        return np.argmin(distances)

    def color_reverser(self, theme_doc, exercise_doc):
        # Cache atrybuty instancji
        starter = self.starter
        font_name = self.font_name
        font_path = self.font_path
        colors = self.colors
        find_closest_color = self.find_closest_color

        # Przetwarzam każdą stronę
        for page in exercise_doc:
            # Losowy seed dla strony startowej
            page_seed = random.randint(10, 14)
            theme_doc.insert_pdf(starter, from_page=page_seed, to_page=page_seed)
            new_page = theme_doc[-1]
            new_page.insert_font(fontname=font_name, fontfile=font_path)

            # Przetwarzanie obrazków
            for img_info in page.get_images(full=True):
                if img_info[1] != 0:
                    # sprawdzam czy obraz to jpeg poprzez sprawdzenia kanalu alfa zdjecia
                    continue

                xref = img_info[0]
                base_image = exercise_doc.extract_image(xref)
                image_bytes = base_image["image"]
                bboxes = page.get_image_rects(xref)
                if bboxes:
                    new_page.insert_image(bboxes[0], stream=image_bytes)

            # Przetwarzanie rysunków (drawings)
            for drawing in page.get_drawings():
                items = drawing.get("items")
                if not items:
                    continue

                drawing_color = drawing.get("color")
                if drawing_color is not None:
                    res_color = colors[find_closest_color(drawing_color)]
                    width = drawing.get("width", 1)
                    stroke_opacity = drawing.get("stroke_opacity", 1.0) or 1.0
                    fill = drawing.get("fill")
                    fill_opacity = drawing.get("fill_opacity", 1.0) or 1.0
                    even_odd = drawing.get("even_odd", False)
                    # Uproszczone pobieranie lineCap
                    line_cap_data = drawing.get("lineCap", (0,))
                    line_cap = (
                        int(line_cap_data[0])
                        if isinstance(line_cap_data, tuple) and line_cap_data
                        else 0
                    )
                    line_join = round(drawing.get("lineJoin", 0))
                    dashes_data = drawing.get("dashes", "[] 0")
                    dashes = None if dashes_data.strip() == "[] 0" else None
                    close_path = drawing.get("closePath", False)

                    shape = new_page.new_shape()
                    for item in items:
                        cmd = item[0]
                        if cmd == "l":
                            s, e = item[1], item[2]
                            shape.draw_line((s.x, s.y), (e.x, e.y))
                        elif cmd == "c":
                            p1, p2, p3, p4 = item[1:5]
                            shape.draw_bezier(
                                (p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y), (p4.x, p4.y)
                            )
                        elif cmd == "re":
                            # Sprawdzamy ramkę – pobieramy raz z pierwszego elementu
                            test_rect = items[0][1]
                            if (
                                test_rect.x0 == 0
                                or test_rect.y0 == 0
                                or test_rect.x1 == 0
                                or test_rect.y1 == 0
                            ):
                                continue
                            rect = item[1]
                            shape.draw_rect(
                                fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y1)
                            )
                        elif cmd == "qu":
                            # Pomijamy jeśli przezroczystość lub czarny kolor
                            if stroke_opacity == 0 or drawing_color == (0, 0, 0):
                                continue
                            shape.draw_quad(item[1])
                    shape.finish(
                        color=res_color,
                        width=width,
                        stroke_opacity=stroke_opacity,
                        fill=fill,
                        fill_opacity=fill_opacity,
                        even_odd=even_odd,
                        lineCap=line_cap,
                        lineJoin=line_join,
                        dashes=dashes,
                        closePath=close_path,
                    )
                    shape.commit(overlay=True)
                else:
                    continue
                    # Kod ponizej przepisuje tez dlugopis zalezny od nacisku,gumki prezycyjne srodku figur geometrycznych
                    # Jesli bedzie to potrzebne mozna odkomentowac ale
                    # Przepisuje rysunki z szablonow oraz bardzo spowalnia skyrpt!
                    shape = page.new_shape()
                    for item in items:
                        cmd = item[0]
                        if cmd == "l":
                            s, e = item[1], item[2]
                            shape.draw_line((s.x, s.y), (e.x, e.y))
                        elif cmd == "re":
                            rect = item[1]
                            shape.draw_rect(
                                fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y1)
                            )
                        elif cmd == "c":
                            p1, p2, p3, p4 = item[1:5]
                            shape.draw_bezier(
                                (p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y), (p4.x, p4.y)
                            )
                        else:
                            print(item)
                    fill = drawing.get("fill")
                    fill_opacity = drawing.get("fill_opacity", 1.0)
                    if fill_opacity == 0.0:
                        fill = None
                    stroke_opacity = drawing.get("stroke_opacity", 1.0) or 1.0
                    color = (0, 0, 0)
                    close_path = drawing.get("closePath", False)
                    shape.finish(
                        color=color,
                        fill=fill,
                        fill_opacity=fill_opacity,
                        stroke_opacity=stroke_opacity,
                        even_odd=drawing.get("even_odd", False),
                        closePath=close_path,
                    )
                    shape.commit(overlay=True)

            # Przetwarzanie tekstu
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span["text"]

                        if "@HIDDEN:" in text:
                            continue

                        bbox = span["bbox"]
                        font_size = span["size"] * self._font_scaling
                        orig_color = span.get("color", 0)
                        norm_color = normalize_color(decode_color(orig_color))
                        res_color = colors[find_closest_color(norm_color)]

                        shape = new_page.new_shape()
                        rect = fitz.Rect(bbox)
                        # Obliczamy increased_bbox przy użyciu szerokości i wysokości
                        w, h = rect.width, rect.height
                        increased_bbox = fitz.Rect(
                            rect.x0 - w * 0.4,
                            rect.y0 - h * 0.4,
                            rect.x1 + w * 0.4,
                            rect.y1 + h * 0.4,
                        )

                        shape.insert_textbox(
                            increased_bbox,
                            unicodedata.normalize("NFC", text),
                            fontsize=font_size,
                            fontname=font_name,
                            color=res_color,
                            align=1,
                            rotate=0,
                            render_mode=0,
                        )
                        shape.finish()
                        shape.commit(overlay=True)
