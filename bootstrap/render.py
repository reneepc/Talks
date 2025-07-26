from pathlib import Path
import html

DRIVE_FOLDER_LINK = "https://drive.google.com/drive/folders/1R5AOlsUbHGUyDaicyGxKRz03GFLzqg_a?usp=drive_link"

# Flush-left tags so Markdown doesn’t turn them into a code block
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

def generate_talk_row(p, pdf_dir: str = "."):
    pdf_href = (Path(pdf_dir) / f'{p["title"]}.pdf').as_posix()
    return (
        "<tr>\n"
        f'<td><div style="text-align: center;">{html.escape(p["title"])}</div></td>\n'
        f'<td><div style="text-align: center;"><a href="{p["slides_link"]}">View</a></div></td>\n'
        f'<td><div style="text-align: center;"><a href="{pdf_href}">Download</a></div></td>\n'
        "</tr>\n"
    )

def generate_talks_table(talks, pdf_dir: str = "."):
    if not talks:
        return (
            "<tr>\n"
            '<td colspan="3"><div style="text-align: center; opacity: 0.7;">'
            f'No talks yet. Add them to the JSON config file (default path: "bootstrap/talks.json")'
            "</div></td>\n"
            "</tr>\n"
        )
    return "".join(generate_talk_row(p, pdf_dir) for p in talks)

def generate_readme_content(talks, pdf_dir: str = "."):
    readme_content = get_html_header()
    readme_content += generate_talks_table(talks, pdf_dir)
    readme_content += get_html_footer()
    return readme_content

def write_readme_file(talks, pdf_dir: str = "."):
    content = generate_readme_content(talks, pdf_dir)
    Path("README.md").write_text(content, encoding="utf-8")
    print("README.md generated successfully")