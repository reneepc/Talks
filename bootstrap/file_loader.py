from pathlib import Path
import json

json_template = [
    {
        "title": "Example - Replace me",
        "slides_link": "https://docs.google.com/presentation/d/EXAMPLE/edit"
    }
]

def load_talks(path: str) -> list:
    p = Path(path)

    # If not in the current directory, also try the parent directory
    if not p.exists():
        try:
            candidate = Path(__file__).resolve().parents[1] / p.name
            if candidate.exists():
                p = candidate
        except Exception:
            pass

    if not p.exists():
        # Create a template in current directory so it's easy to discover/edit
        try:
            Path(path).write_text(
                json.dumps(json_template, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8"
            )
            print(f"Couldn't locate file {path}.\nCreated a template at '{Path(path).resolve()}'")
        except OSError as e:
            print(f"Failed to create template file {path}: {e}")
        return []

    data = fetch_talks(p)
    return sanitize_talks(data)

def fetch_talks(path: Path) -> list:
    try:
        text = path.read_text(encoding="utf-8")
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {path}: line {e.lineno}, col {e.colno}: {e.msg}")
        return []
    except OSError as e:
        print(f"Failed to read {path}: {e}")
        return []

    if not isinstance(data, list):
        print(f"Expecting a JSON array of this format: {json.dumps(json_template, indent=2)}")
        return []

    return data

def sanitize_talks(data: list) -> list:
    out = []
    for i, item in enumerate(data):
        err = (
            f"Failed to parse item {i}. It should be formatted like:\n"
            f"{json.dumps(json_template[0], indent=2)}"
        )
        if not isinstance(item, dict):
            print(err); continue
        title = item.get("title")
        link  = item.get("slides_link")
        if not title or not link:
            print(err); continue
        out.append({"title": str(title), "slides_link": str(link)})

    if not out:
        print("No valid talks found. Please check your JSON file.")
    return out