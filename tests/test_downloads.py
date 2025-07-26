from pathlib import Path
from .pdf_test_utils import make_pdf_bytes, PDF_MAGIC, pdf_path

def test_download_only_creates_pdf_files(tmp_path: Path, write_talks_json, run, make_fetch_stub, talks):
    write_talks_json(tmp_path, talks)
    out_dir = tmp_path / "output_test_file"
    fake_fetch = make_fetch_stub()

    rc = run(tmp_path, ["--download-only", "--out-dir", str(out_dir), "--workers", "3"], stub_fetch=fake_fetch)

    assert rc == 0
    for t in talks:
        pdf = pdf_path(out_dir, t["title"])
        assert pdf.exists()
        assert pdf.read_bytes().startswith(PDF_MAGIC)

    assert not (tmp_path / "README.md").exists()

def test_skip_when_pdf_exists_without_force(tmp_path: Path, write_talks_json, run, make_fetch_stub, talks):
    write_talks_json(tmp_path, talks)
    out_dir = tmp_path / "output_test_file"
    out_dir.mkdir(parents=True, exist_ok=True)

    orig = make_pdf_bytes("ORIG")
    for t in talks:
        pdf = pdf_path(out_dir, t["title"])
        pdf.write_bytes(orig)

    new = make_pdf_bytes("NEW")
    fake_fetch = make_fetch_stub(content=new)

    run(tmp_path, ["--download-only", "--out-dir", str(out_dir)], stub_fetch=fake_fetch)

    for t in talks:
        pdf = pdf_path(out_dir, t["title"])
        assert pdf.exists()
        assert pdf.read_bytes() == orig

def test_force_overwrites_existing_pdf_files(tmp_path: Path, write_talks_json, run, make_fetch_stub, talks):
    write_talks_json(tmp_path, talks)
    out_dir = tmp_path / "output_test_file"
    out_dir.mkdir(parents=True, exist_ok=True)

    orig = make_pdf_bytes("ORIG")
    for task in talks:
        pdf = pdf_path(out_dir, task["title"])
        pdf.write_bytes(orig)

    new = make_pdf_bytes("NEW")
    fake_fetch = make_fetch_stub(content=new)

    run(tmp_path, ["--download-only", "--out-dir", str(out_dir), "--force"], stub_fetch=fake_fetch)

    for task in talks:
        pdf = pdf_path(out_dir, task["title"])
        assert pdf.read_bytes() == new