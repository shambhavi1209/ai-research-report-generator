"""
generate.py — Headless CLI for batch/report generation.

Real extraction:  python generate.py --file input.pdf --company "X Ltd" --out report.pdf
Demo (no key):    python generate.py --demo --company "Meridian Auto Components Ltd" --out demo.pdf
"""
from __future__ import annotations

import argparse
import os
import pathlib

from charts.builders import build_charts
from demo_data import DEMO_REPORTS, meridian_auto
from render import render_pdf


def main() -> None:
    p = argparse.ArgumentParser(description="Generate a Geojit-style research report PDF")
    p.add_argument("--file", help="Path to context document (pdf/csv/txt)")
    p.add_argument("--company", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--demo", action="store_true", help="Use built-in demo data (no API key needed)")
    args = p.parse_args()

    if args.demo:
        report = DEMO_REPORTS.get(args.company, meridian_auto)()
        report.company_name = args.company
    else:
        if not args.file:
            p.error("--file is required unless --demo is set")
        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            p.error("Set GEMINI_API_KEY for real extraction, or use --demo")
        from extractors import extract_text
        from llm.extract import extract_report
        data = pathlib.Path(args.file).read_bytes()
        text = extract_text(data, args.file)
        report = extract_report(text, args.company, key)

    pdf = render_pdf(report, build_charts(report))
    pathlib.Path(args.out).write_bytes(pdf)
    print(f"Wrote {args.out} ({len(pdf):,} bytes)")


if __name__ == "__main__":
    main()
