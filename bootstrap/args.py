import argparse
from .config import DEFAULT_JSON, DEFAULT_OUT_DIR, DEFAULT_N_WORKERS

def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Generate README and download PDF files for talks.")
    parser.add_argument('--json', default=DEFAULT_JSON, help="Path to talks JSON file")

    mx = parser.add_mutually_exclusive_group()
    mx.add_argument('--readme-only', action='store_true', help="Only generate README")
    mx.add_argument('--download-only', action='store_true', help="Only download PDF files")

    parser.add_argument('--out-dir', default=DEFAULT_OUT_DIR,
                        help="Directory to write PDF files and use in README links")
    parser.add_argument('--force', action='store_true',
                        help="Force actions: generate README even if empty; re-download/overwrite existing PDF files")
    parser.add_argument('--workers', type=int, default=DEFAULT_N_WORKERS,
                        help=f"Number of worker threads for downloading PDF files")

    args = parser.parse_args(argv)
    return args