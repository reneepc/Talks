import argparse
import os
from .config import DEFAULT_JSON, DEFAULT_OUT_DIR, DEFAULT_N_WORKERS

CUSTOM_DIRS_ALLOWED = {"pdf", "readme"}

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
                        help="Number of worker threads for downloading PDF files")

    return parser.parse_args(argv)

def parse_out_dir(s: str | None) -> dict[str, str]:
    """
      "dir"                      -> {'pdf': 'dir', 'readme': 'dir'}
      "pdf=dir readme=/assets"   -> {'pdf': 'dir', 'readme': '/assets'}
      "pdf=dir,readme=/assets"   -> same as above
    """
    output_dir = s.strip()

    # Single value → apply to both
    if "=" not in output_dir:
        v = _expand_path_string(output_dir)
        return {"pdf": v, "readme": v}

    # Keyed pairs with defaults for unspecified keys
    kv = _parse_keyed(output_dir)
    return {
        "pdf": kv.get("pdf"),
        "readme": kv.get("readme"),
    }


def _expand_path_string(path_str: str) -> str:
    original_path = path_str
    path_str = path_str.strip()
    path_str = os.path.expandvars(path_str)
    path_str = os.path.expanduser(path_str)
    if not path_str:
        return original_path
    return path_str


def _parse_keyed(path_string: str) -> dict[str, str]:
    tokens = path_string.replace(",", " ").split()
    out: dict[str, str] = {}
    for token in tokens:
        if "=" not in token:
            raise ValueError(f"Invalid token {token!r}. Use 'pdf=...' or 'readme=...'.")

        key, path_value = token.split("=", 1)
        key = key.strip().lower()

        if key not in CUSTOM_DIRS_ALLOWED:
            raise ValueError(f"Unknown key {key!r}. Allowed keys: {sorted(CUSTOM_DIRS_ALLOWED)}")
        path_value = _expand_path_string(path_value)

        if not path_value:
            raise ValueError(f"Empty value for {key!r}.")
        out[key] = path_value
    return out

