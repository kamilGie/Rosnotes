def extract_exercise_info(page_text: str):
    if "@HIDDEN:" in page_text and "@DONE" not in page_text:
        pattern_start = page_text.find("@HIDDEN: ") + len("@HIDDEN: ")
        return page_text[pattern_start : pattern_start + 4]
    return None
