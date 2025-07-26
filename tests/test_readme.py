from pathlib import Path
from .pdf_test_utils import pdf_path

def test_readme_only_generates_readme_with_links(tmp_path: Path, write_talks_json, run, talks):
    out_dir = "test_output_dir"
    write_talks_json(tmp_path, talks)

    run(tmp_path, ["--readme-only", "--out-dir", out_dir])

    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "Talks" in readme
    for t in talks:
        assert t["title"] in readme
        assert pdf_path(out_dir, t["title"]).as_posix() in readme

def test_empty_without_force_exits_and_no_readme(tmp_path: Path, write_talks_json, run):
    write_talks_json(tmp_path, [])
    rc = run(tmp_path, ["--readme-only"])
    assert rc == 0
    assert not (tmp_path / "README.md").exists()

def test_empty_with_force_renders_placeholder(tmp_path: Path, write_talks_json, run):
    write_talks_json(tmp_path, [])
    run(tmp_path, ["--readme-only", "--force"])
    content = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "No talks yet" in content