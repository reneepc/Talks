from pathlib import Path
import re
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def build_slides_export_pdf_url(slides_link: str):
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

def download_pdfs(presentations):
    if not presentations:
        print("No talks to download")
        return

    for p in presentations:
        pdf_path = Path(f'{p["title"]}.pdf')

        if pdf_path.exists():
            if is_pdf_file(pdf_path):
                print(f"Skipping '{pdf_path}' (already exists and is a valid PDF)")
                continue
            else:
                print(f"Removing corrupted '{pdf_path}' and retrying...")
                try:
                    pdf_path.unlink()
                except FileNotFoundError:
                    pass

        export_url = build_slides_export_pdf_url(p["slides_link"]) or p["slides_link"]
        print(f"Downloading '{p['title']}' to '{pdf_path}'...")

        if fetch_pdf(export_url, pdf_path):
            print(f"Successfully downloaded {p['title']}")
        else:
            print(f"Couldn't download {p['title']}. Please check the link: {p['slides_link']}")