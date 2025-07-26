from pathlib import Path
import re
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict
from .naming import pdf_filename
from .config import DEFAULT_REQUEST_TIMEOUT

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

def fetch_pdf(url: str, out_path: Path, timeout: int = DEFAULT_REQUEST_TIMEOUT) -> bool:
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
    if not pdf_path.exists(): return True
    if force: return True
    return not is_pdf_file(pdf_path)

def remove_existing(pdf_path: Path) -> None:
    if pdf_path.exists():
        print("Removing existing file:", pdf_path)
        pdf_path.unlink(missing_ok=True)

def _ensure_out_dir_exists(out_dir: str) -> Path:
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    return out_path

def _download_one(title: str, export_url: str, pdf_path: Path) -> bool:
    print(f"Downloading '{title}' to '{pdf_path}'...")
    return fetch_pdf(export_url, pdf_path)

def _submit_downloads(executor: ThreadPoolExecutor, talks: list, out_path: Path, force: bool) -> Dict:
    futures_map: Dict = {}
    for talk in talks:
        title = talk["title"]
        link = talk["slides_link"]
        pdf_path = out_path / pdf_filename(title)

        if not should_download(pdf_path, force):
            print(f"Skipping '{pdf_path}' (already exists and is a valid PDF)")
            continue
        remove_existing(pdf_path)

        export_url = build_slides_export_pdf_url(link) or link
        fut = executor.submit(_download_one, title, export_url, pdf_path)
        futures_map[fut] = (title, pdf_path, link)
    return futures_map

def _report_results(futures_map: Dict) -> None:
    for fut in as_completed(futures_map):
        title, pdf_path, link = futures_map[fut]
        try:
            ok = fut.result()
        except Exception as e:
            print(f"Failed to download {title}: {e}")
            continue
        if not ok:
            print(f"Couldn't download {title}. Please check the link: {link}")
            continue
        print(f"Successfully downloaded {title}: {pdf_path}")

def download_pdf_files(talks: list, out_dir: str, force, workers: int) -> None:
    if not talks:
        print("No talks to download")
        return
    out_path = _ensure_out_dir_exists(out_dir)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures_map = _submit_downloads(executor, talks, out_path, force)
        _report_results(futures_map)