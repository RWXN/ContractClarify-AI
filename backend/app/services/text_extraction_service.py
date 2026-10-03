from pathlib import Path

from pypdf import PdfReader


def extract_text_from_txt(file_path: str) -> list[dict]:
    path = Path(file_path)

    text = path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    return [
        {
            "page_number": 1,
            "text": text
        }
    ]


def extract_text_from_pdf(file_path: str) -> list[dict]:
    reader = PdfReader(file_path)

    pages = []

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append(
                {
                    "page_number": index,
                    "text": text
                }
            )

    return pages


def extract_text_from_file(file_path: str, file_type: str) -> list[dict]:
    if file_type == "txt":
        return extract_text_from_txt(file_path)

    if file_type == "pdf":
        return extract_text_from_pdf(file_path)

    raise ValueError(f"Unsupported file type: {file_type}")