from src.utils.file_management import get_passwords


def get_available_pdfs(pdf_paths):
    pdfs = []
    for pdf_path in pdf_paths:
        password = get_passwords(pdf_path.name[:-4])
        if password is not None:
            pdfs.append([pdf_path, password])
    return pdfs
