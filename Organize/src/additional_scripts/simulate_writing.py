import fitz
import json
from pathlib import Path


def normalize_color(color):
    return tuple(c / 255.0 for c in color)


def decode_color(color_int) -> tuple:
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    return r, g, b


def get_colors(source_page):
    colors = [(), (), ()]
    text_dict = source_page.get_text("dict")
    for block in text_dict["blocks"]:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    if "Kolor treści" in span["text"]:
                        colors[0] = normalize_color(decode_color(span["color"]))
                    if "Kolor poboczny" in span["text"]:
                        colors[1] = normalize_color(decode_color(span["color"]))
                    if "Kolor wyniku" in span["text"]:
                        colors[2] = normalize_color(decode_color(span["color"]))
    return colors


def extract_exercise_info(page_text: str):
    if "@HIDDEN:" in page_text and "@DONE" not in page_text:
        pattern_start = page_text.find("@HIDDEN: ") + len("@HIDDEN: ")
        return page_text[pattern_start : pattern_start + 4]
    return None


def draw_pen(page, color):
    """
    Rysuje kształt symulujący 'długopis' z GoodNotes, czyli swobodny szkic.
    """
    pen_points = [(50, 50), (60, 55), (70, 45), (80, 60), (90, 50)]
    shape = page.new_shape()
    # Rysujemy kolejne segmenty linii łącząc punkty
    for i in range(len(pen_points) - 1):
        shape.draw_line(pen_points[i], pen_points[i + 1])
    shape.finish(color=color, width=2)
    shape.commit()


def draw_square(page, color):
    shape = page.new_shape()
    rect = fitz.Rect(150, 150, 300, 250)
    shape.draw_rect(rect)
    shape.finish(color=color, width=2)
    shape.commit()


def draw_circle(page, color):
    shape = page.new_shape()
    center = (225, 200)
    radius = 50
    shape.draw_circle(center, radius)
    shape.finish(color=color, width=2)
    shape.commit()


def insert_text(page, text, color):
    page.insert_text((100, 100), text, fontsize=12, color=color)


def draw(page, cycle_index, color):
    if cycle_index % 4 == 0:
        draw_square(page, color)
    elif cycle_index % 4 == 1:
        insert_text(page, "Napis", color)
    elif cycle_index % 4 == 2:
        draw_circle(page, color)
    else:
        draw_pen(page, color)


def main():
    env_path = Path("./Organize/src/env.json")
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            env_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        env_data = {}

    with fitz.open("./Notebooks/input.pdf") as doc:
        for passwords in env_data.values():
            if doc.authenticate(passwords):
                break
        color = get_colors(doc[1])
        assert color is not [(), (), ()]
        cycle_index = 0  # Indeks do cyklu trzech operacji

        for page in doc:
            rect = fitz.Rect(-10, -10, 50, 50)
            text = page.get_textbox(rect)
            exercise_info = extract_exercise_info(text)
            if exercise_info == None:
                continue
            if not exercise_info[:2].isdigit() or int(exercise_info[:2]) % 2 == 0:
                draw(page, cycle_index, color[cycle_index % 2])
                continue

            # Następnie, w zależności od cyklu, wykonujemy jedną z trzech operacji:
            draw(page, cycle_index, color[2])
            cycle_index += 1

        doc.save("Organize/output.pdf")


if __name__ == "__main__":
    main()
