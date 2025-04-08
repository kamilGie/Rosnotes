from logging import exception
from openai import OpenAI
import shutil
from pathlib import Path
import subprocess
import base64
import os

secret_key = os.getenv("OPEN_AI_KEY")
client = OpenAI(api_key=secret_key)


# Function to encode the image
def encode_image(image_path: Path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def craate_ai_sol(path):
    # Path to your image
    # Getting the Base64 string
    base64_image = encode_image(path)
    print(path)

    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": """Jestem studentem informatyki. Mam do rozwiązania to zadanie.

Rozwiąż to zadanie krok po kroku, podając wszystkie wzory od podstawowych, przekształcając je logicznie aż do końcowego rozwiązania. Każdy krok powinien być dokładnie uzasadniony i wynikać bezpośrednio z poprzedniego.

Zacznij od podania pełnych danych wejściowych, następnie pokaż:

ogólny wzór,

przekształcenie wzoru (jeśli potrzebne),

podstawienie danych,

przeliczenie krok po kroku,

wynik końcowy z jednostką.

Całość przedstaw w formacie LaTeX, stosując estetyczne formatowanie matematyczne (oddzielne bloki równań, wyrównanie, pogrubienie wyniku końcowego).

Nie dodawaj żadnych dodatkowych sugestii, komentarzy, tłumaczeń, uproszczeń, wariantów ani podsumowań — wyłącznie rozwiąż zadanie zgodnie z powyższą strukturą.""",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
    )

    response_text = response.output_text

    # Prepare LaTeX content
    latex_code = f"""
    \\documentclass{{article}}
    \\usepackage[a4paper, left=2cm, right=2cm, top=1cm, bottom=2cm]{{geometry}}
    \\usepackage{{amsmath}}
    \\usepackage{{graphicx}}
    \\begin{{document}}

    \\begin{{center}}
        \\Large \\textbf{{ROZWIĄZANIE WYGENEROWANE PRZEZ CHAT GPT}}
    \\end{{center}}
    \\vspace{{1cm}}

    \\begin{{figure}}[h!]
        \\centering
        \\includegraphics[width=1\\textwidth]{{{path}}}
    \\end{{figure}}

    \\begin{{quote}}
    {response_text}
    \\end{{quote}}
    \\end{{document}}
    """

    # Write LaTeX content to a .tex file
    output = "source_raw.tex"
    with open(output, "w") as f:
        f.write(latex_code)

    desc_nr = str(path)[-6:-4]
    output_folder = Path(Path(path).parent / desc_nr / "resources" / "pdfs")

    # Tworzenie folderu, jeśli nie istnieje
    output_folder.mkdir(parents=True, exist_ok=True)

    # Run pdflatex to convert LaTeX to PDF
    subprocess.run(
        [
            "pdflatex",
            "-interaction=nonstopmode",
            "-output-directory",
            str(output_folder),
            output,
        ]
    )

    shutil.move(path, output_folder.parent)
    # Now you have output.pdf in your directory
    print("PDF has been created!")


for folder_set in Path("Solutions/").glob("Zestaw*"):
    for path in Path(folder_set).glob("desc_*"):
        try:
            craate_ai_sol(path)
        except exception as e:
            print(f"Nieudano {path}: przerywam")
            break
