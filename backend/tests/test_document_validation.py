from fastapi import HTTPException, UploadFile

from app.services.document_service import validate_upload_file


class DummyUploadFile:
    def __init__(self, filename: str, content_type: str):
        self.filename = filename
        self.content_type = content_type


def test_validate_txt_file():
    file = DummyUploadFile(
        filename="contract.txt",
        content_type="text/plain"
    )

    file_type = validate_upload_file(
        file=file,
        file_bytes=b"Sample contract"
    )

    assert file_type == "txt"


def test_validate_pdf_file():
    file = DummyUploadFile(
        filename="contract.pdf",
        content_type="application/pdf"
    )

    file_type = validate_upload_file(
        file=file,
        file_bytes=b"%PDF-1.4"
    )

    assert file_type == "pdf"


def test_reject_invalid_extension():
    file = DummyUploadFile(
        filename="contract.exe",
        content_type="application/octet-stream"
    )

    try:
        validate_upload_file(
            file=file,
            file_bytes=b"bad file"
        )
        assert False
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "Only PDF and TXT files are allowed"


def test_reject_large_file():
    file = DummyUploadFile(
        filename="large.txt",
        content_type="text/plain"
    )

    large_content = b"a" * (10 * 1024 * 1024 + 1)

    try:
        validate_upload_file(
            file=file,
            file_bytes=large_content
        )
        assert False
    except HTTPException as exc:
        assert exc.status_code == 413
        assert exc.detail == "File size must be less than 10MB"