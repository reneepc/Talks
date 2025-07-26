from pathlib import Path
import re
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def build_slides_export_pdf_url(slides_link: str) -> str | None:
    try:
        parsed = urlparse(slides_link)
        if parsed.netloc.endswith("docs.google.com") and "/presentation/d/" in parsed.path:
            m = re.search(r"/presentation/d/([^/]+)", parsed.path)
            if m:
                doc_id = m.group(1)
                return f"https://docs.google.com/presentation/d/{doc_id}/export?format=pdf"
    except Exception:
        pass
    return None

def is_pdf_file(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            return f.read(5) == b"%PDF-"
    except OSError:
        return False

def fetch_pdf(url: str, out_path: Path, timeout: int = 60) -> bool:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            data = resp.read()
    except (HTTPError, URLError) as e:
        print(f"Failed to fetch {url}: {e}")
        return False

    if not data.startswith(b"%PDF-"):
        print("Not a PDF file!")
        return False

    try:
        out_path.write_bytes(data)
    except OSError as e:
        print(f"Failed to write PDF to {out_path}: {e}")
        return False

    return True

def should_download(pdf_path: Path, force: bool) -> bool:
    if not pdf_path.exists():
        return True
    if force:
        return True

    return not is_pdf_file(pdf_path)


def download_pdf_files(talks: list, out_dir: str = ".", force: bool = False):
    if not talks:
        print("No talks to download")
        return

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    for p in talks:
        pdf_path = out_path / f'{p["title"]}.pdf'

        if not should_download(pdf_path, force):
            print(f"Skipping '{pdf_path}' (already exists and is a valid PDF)")
            continue
        if pdf_path.exists():
            print("Removing existing file:", pdf_path)
            pdf_path.unlink(missing_ok=True)

        export_url = build_slides_export_pdf_url(p["slides_link"]) or p["slides_link"]
        print(f"Downloading '{p['title']}' to '{pdf_path}'...")

        if fetch_pdf(export_url, pdf_path):
            print(f"Successfully downloaded {p['title']}")
        else:
            print(f"Couldn't download {p['title']}. Please check the link: {p['slides_link']}")