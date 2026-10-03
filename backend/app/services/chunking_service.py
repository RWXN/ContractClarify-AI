import re


DEFAULT_CHUNK_SIZE = 900
DEFAULT_CHUNK_OVERLAP = 150


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def estimate_token_count(text: str) -> int:
    # Rough estimate: 1 token is about 4 characters in English text.
    # This is not exact, but good enough before adding real tokenizer support.
    return max(1, len(text) // 4)


def split_text_into_chunks(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
) -> list[str]:
    cleaned_text = clean_text(text)

    if not cleaned_text:
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks = []
    start = 0

    while start < len(cleaned_text):
        end = start + chunk_size
        chunk = cleaned_text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - chunk_overlap

    return chunks


def chunk_pages(pages: list[dict]) -> list[dict]:
    all_chunks = []
    chunk_index = 0

    for page in pages:
        page_number = page["page_number"]
        text = page["text"]

        page_chunks = split_text_into_chunks(text)

        for content in page_chunks:
            all_chunks.append(
                {
                    "chunk_index": chunk_index,
                    "page_number": page_number,
                    "content": content,
                    "token_count_estimate": estimate_token_count(content)
                }
            )

            chunk_index += 1

    return all_chunks