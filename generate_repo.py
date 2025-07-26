from bootstrap import parse_args, load_talks, write_readme_file, download_pdf_files
import sys

if __name__ == "__main__":
    args = parse_args()

    talks = load_talks(args.json)

    if not talks:
        print(f"No talks found in {args.json}")
        if not args.force_empty:
            print("Exiting without generating README.md")
            sys.exit(0)

    write_readme_file(talks)
    download_pdf_files(talks)