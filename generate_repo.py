#!/usr/bin/env python3
from bootstrap import parse_args, load_talks, write_readme_file, download_pdf_files
import sys

def main(argv=None) -> int:
    args = parse_args(argv)
    talks = load_talks(args.json)

    if not talks:
        print(f"No talks found in {args.json}")
        if not args.force:
            if args.download_only:
                print("Exiting without downloading PDF files.")
            else:
                print("Exiting without generating README.md")
            return 0

    if args.readme_only:
        write_readme_file(talks, pdf_dir=args.out_dir)
    elif args.download_only:
        download_pdf_files(talks, out_dir=args.out_dir, force=args.force, workers=args.workers)
    else:
        write_readme_file(talks, pdf_dir=args.out_dir)
        download_pdf_files(talks, out_dir=args.out_dir, force=args.force, workers=args.workers)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
