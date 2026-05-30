#!/usr/bin/env python3
"""Convert chart PDFs in this folder to high-DPI PNGs for web embedding.

Why: PDFs embedded via <object type="application/pdf"> render reliably on
desktop browsers but iOS Safari (and many in-app webviews) refuse to render
them inline, falling back to a download prompt. Converting to PNG lets the
same charts display as plain <img> tags everywhere — desktop, mobile, and
search-engine previews.

Usage:
    pip install pymupdf
    python convert_charts.py [--dpi 200] [--no-alpha]

Each *.pdf in the script's folder is written out as a same-name *.png next
to it. Already-existing PNGs are overwritten.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="Render DPI (default: 200; bump to 300 if charts look soft).",
    )
    p.add_argument(
        "--no-alpha",
        action="store_true",
        help="Render onto an opaque white background instead of transparency.",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    try:
        import fitz  # PyMuPDF
    except ImportError:
        print(
            "PyMuPDF is required. Install with:\n    pip install pymupdf",
            file=sys.stderr,
        )
        return 1

    here = Path(__file__).resolve().parent
    pdfs = sorted(here.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {here}")
        return 0

    print(f"Converting {len(pdfs)} PDF(s) at {args.dpi} DPI:")
    for pdf in pdfs:
        png = pdf.with_suffix(".png")
        doc = fitz.open(pdf)
        page = doc[0]
        pix = page.get_pixmap(dpi=args.dpi, alpha=not args.no_alpha)
        pix.save(png)
        doc.close()
        print(f"  {pdf.name} -> {png.name}  ({pix.width}x{pix.height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
