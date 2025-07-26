import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Generate README and download PDFs for talks.")
    parser.add_argument('--json', default="bootstrap/talks.json", help="Path to talks JSON file")
    parser.add_argument('--force-empty', action='store_true', help="Force README generation even if no talks found")
    args = parser.parse_args()

    return args