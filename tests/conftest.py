import json
import sys
import importlib
from pathlib import Path
from .pdf_test_utils import make_pdf_bytes
import pytest

def _clear_project_modules() -> None:
    for name in list(sys.modules):
        if name == "bootstrap" or name.startswith("bootstrap.") or name == "generate_repo":
            del sys.modules[name]
    importlib.invalidate_caches()

@pytest.fixture()
def write_talks_json():
    def _write(dst_root: Path, talks: list) -> Path:
        p = dst_root / "bootstrap" / "talks.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(talks, indent=2), encoding="utf-8")
        return p
    return _write

@pytest.fixture()
def make_fetch_stub():
    def _factory(content: bytes | None = None, tag: str = "FAKE"):
        def _fake_fetch(url: str, out_path: Path, timeout: int = 60) -> bool:
            data = content if content is not None else make_pdf_bytes(tag)
            out_path.write_bytes(data)
            return True
        return _fake_fetch
    return _factory

@pytest.fixture()
def run(monkeypatch):
    def _run(workdir: Path, argv: list[str], stub_fetch=None):
        repo = Path(__file__).resolve().parents[1]
        monkeypatch.chdir(workdir)

        _clear_project_modules()

        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))
        if stub_fetch is not None:
            dl = importlib.import_module("bootstrap.pdf_downloader")
            monkeypatch.setattr(dl, "fetch_pdf", stub_fetch, raising=True)

        gr = importlib.import_module("generate_repo")
        importlib.reload(gr)
        return gr.main(argv)

    return _run

@pytest.fixture()
def talks():
    return [
        {"title": "Go Memory Internals", "slides_link": "https://docs.google.com/presentation/d/ID1/edit"},
        {"title": "Embeddings", "slides_link": "https://docs.google.com/presentation/d/ID2/edit"},
    ]