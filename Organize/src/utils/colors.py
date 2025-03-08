import numpy as np


def normalize_color(color):
    return tuple(c / 255.0 for c in color)


def decode_color(color_int) -> tuple:
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    return r, g, b


def get_font_and_colors(source_page):
    font_path = "Organize/src/assets/fonts/"
    font_name = ""
    colors = [None, None, None]
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
                    if "Czcionka" in span["text"]:
                        font_name = span["text"][len("Czcionka ") :]
                        font_path += span["text"][len("Czcionka ") :] + ".ttf"
    return colors, font_name, font_path


def has_result_drawing(page, theme_colors):
    theme_colors = np.array(theme_colors)

    def is_similar_color(original_color):
        original_np = np.array(original_color)
        distances = np.linalg.norm(theme_colors - original_np, axis=1)
        return np.argmin(distances) == 2

    def check_colors_in_drawings(items):
        """Sprawdza kolory w rysunkach."""
        for item in items:
            color = item.get("color")
            if color is None:
                continue

            if isinstance(color, tuple) and len(color) == 3:
                r, g, b = color
            else:
                color = decode_color(color)
                r, g, b = color

            if is_similar_color((r, g, b)):
                return True
        return False

    def check_colors_in_text(text_dict):
        for block in text_dict["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["text"] == "Teoria" or span["text"] == "Definicje":
                        continue
                    color = span.get("color")
                    if color is None:
                        continue

                    color = normalize_color(decode_color(color))
                    if is_similar_color(color):
                        return True
        return False

    if check_colors_in_drawings(page.get_drawings()):
        return True

    if check_colors_in_text(page.get_text("dict")):
        return True

    return False
