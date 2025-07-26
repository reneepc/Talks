import re, unicodedata

def _slugify(text: str, sep: str = "-") -> str:
    if not text:
        return "untitled"
    t = unicodedata.normalize("NFKD", text)
    t = t.encode("ascii", "ignore").decode("ascii").lower()
    t = re.sub(r"[^a-z0-9]+", sep, t)
    t = re.sub(rf"{re.escape(sep)}+", sep, t).strip(sep)
    return t or "untitled"

def pdf_filename(title: str) -> str:
    return f"{_slugify(title)}.pdf"