#!/usr/bin/env python3
from bootstrap import parse_args, load_talks, write_readme_file, download_pdf_files
import sys

if __name__ == "__main__":
    args = parse_args()

    talks = load_talks(args.json)

    if not talks:
        print(f"No talks found in {args.json}")
        if not args.force:
            if args.download_only:
                print("Exiting without downloading PDFs.")
            else:
                print("Exiting without generating README.md")
            sys.exit(0)

    if args.readme_only:
        write_readme_file(talks, pdf_dir=args.out_dir)
    elif args.download_only:
        download_pdf_files(talks, out_dir=args.out_dir, force=args.force)
    else:
        write_readme_file(talks, pdf_dir=args.out_dir)
        download_pdf_files(talks, out_dir=args.out_dir, force=args.force)