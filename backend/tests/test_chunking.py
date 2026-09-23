from app.services.chunking_service import (
    clean_text,
    estimate_token_count,
    split_text_into_chunks,
    chunk_pages,
)


def test_clean_text_removes_extra_spaces():
    text = "This   is\n\n a     test."

    result = clean_text(text)

    assert result == "This is a test."


def test_estimate_token_count_returns_positive_number():
    text = "This is a sample contract."

    result = estimate_token_count(text)

    assert result > 0


def test_split_short_text_into_one_chunk():
    text = "This is a short document."

    chunks = split_text_into_chunks(text)

    assert len(chunks) == 1
    assert chunks[0] == "This is a short document."


def test_split_long_text_into_multiple_chunks():
    text = "a" * 2000

    chunks = split_text_into_chunks(
        text,
        chunk_size=500,
        chunk_overlap=100
    )

    assert len(chunks) > 1


def test_chunk_pages_preserves_page_number():
    pages = [
        {
            "page_number": 3,
            "text": "This is page three."
        }
    ]

    chunks = chunk_pages(pages)

    assert len(chunks) == 1
    assert chunks[0]["page_number"] == 3
    assert chunks[0]["chunk_index"] == 0