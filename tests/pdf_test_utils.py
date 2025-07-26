from pathlib import Path
from bootstrap.naming import pdf_filename

PDF_MAGIC = b"%PDF-"
PDF_HEADER_TXT = "%PDF-1.4\n"

def make_pdf_bytes(test_file_tag: str = "FAKE") -> bytes:
    body = f"% {test_file_tag}\n"
    trailer = "%%EOF\n"
    return (PDF_HEADER_TXT + body + trailer).encode("ascii")

def pdf_path(pdf_dir: str | Path, title: str) -> Path:
    return Path(pdf_dir) / pdf_filename(title)
