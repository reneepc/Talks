from pathlib import Path
import html
from .naming import pdf_filename
from .config import DRIVE_FOLDER_LINK

def get_html_header():
    return (
        '<div align="center">\n'
        '  <h1>Talks</h1>\n'
        '</div>\n'
        '\n'
        '<p align="center">Here is a collection of my public talks</p>\n'
        '\n'
        '<table align="center">\n'
        '<thead>\n'
        '<tr>\n'
        '<th style="text-align: center;">Title</th>\n'
        '<th style="text-align: center;">Google Slides</th>\n'
        '<th style="text-align: center;">PDF Download</th>\n'
        '</tr>\n'
        '</thead>\n'
        '<tbody>\n'
    )

def get_html_footer():
    return (
        '</tbody>\n'
        '</table>\n'
        '<hr>\n'
        f'<p align="center">\n'
        f'  <a href="{html.escape(DRIVE_FOLDER_LINK, quote=True)}">\n'
        '    Google Drive Folder - Contains all talks\n'
        '  </a>\n'
        '</p>\n'
    )

def generate_talk_row(talk, pdf_base: str) -> str:
    pdf_href = (Path(pdf_base) / pdf_filename(talk["title"])).as_posix()
    return (
        "<tr>\n"
        f'<td><div style="text-align: center;">{html.escape(talk["title"])}</div></td>\n'
        f'<td><div style="text-align: center;"><a href="{html.escape(talk["slides_link"], quote=True)}">View</a></div></td>\n'
        f'<td><div style="text-align: center;"><a href="{pdf_href}">Download</a></div></td>\n'
        "</tr>\n"
    )

def generate_talks_table(talks, pdf_base: str) -> str:
    if not talks:
        return (
            "<tr>\n"
            '<td colspan="3"><div style="text-align: center; opacity: 0.7;">'
            'No talks yet. Add them to the JSON config file (default path: "bootstrap/talks.json")'
            "</div></td>\n"
            "</tr>\n"
        )
    return "".join(generate_talk_row(p, pdf_base) for p in talks)

def generate_readme_content(talks, pdf_base: str) -> str:
    readme_content = get_html_header()
    readme_content += generate_talks_table(talks, pdf_base)
    readme_content += get_html_footer()
    return readme_content

def write_readme_file(talks, out_dir: str, pdf_base: str) -> None:
    out_dir_path = Path(out_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)

    content = generate_readme_content(talks, pdf_base)
    Path(out_dir, "README.md").write_text(content, encoding="utf-8")
    print("README.md generated successfully")