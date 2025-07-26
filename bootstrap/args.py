import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Generate README and download PDFs for talks.")
    parser.add_argument('--json', default="bootstrap/talks.json", help="Path to talks JSON file")

    mx = parser.add_mutually_exclusive_group()
    mx.add_argument('--readme-only', action='store_true', help="Only generate README")
    mx.add_argument('--download-only', action='store_true', help="Only download PDFs")

    parser.add_argument('--out-dir', default=".", help="Directory to write PDFs and use in README links (default: current directory)")

    parser.add_argument('--force', action='store_true',
                        help="Force actions: generate README even if empty; re-download/overwrite existing PDFs")

    args = parser.parse_args()
    return args