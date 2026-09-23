from pathlib import Path

from app.services.text_extraction_service import extract_text_from_txt


def test_extract_text_from_txt(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text(
        "This is a sample text document.",
        encoding="utf-8"
    )

    pages = extract_text_from_txt(str(test_file))

    assert len(pages) == 1
    assert pages[0]["page_number"] == 1
    assert pages[0]["text"] == "This is a sample text document."