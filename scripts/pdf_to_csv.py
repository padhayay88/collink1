#!/usr/bin/env python3
"""
Extract tables from a PDF into a single CSV.

Usage:
  python scripts/pdf_to_csv.py --input "<path-to.pdf>" --output "<path-to.csv>"

Notes:
- Uses pdfplumber for table extraction (no Java requirement).
- Adds `page_number` and `table_index` columns to identify origin of each row.
- If a page has multiple detected tables, they are concatenated.
- Rows are padded to the maximum number of columns found in the table to keep a rectangular shape.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

import pdfplumber
import pandas as pd


def _rectangularize(rows: List[List[Optional[str]]]) -> List[List[Optional[str]]]:
    """Pad rows with None so they all have the same length."""
    if not rows:
        return rows
    max_len = max(len(r) for r in rows)
    return [r + [None] * (max_len - len(r)) for r in rows]


def extract_pdf_tables_to_csv(input_pdf: Path, output_csv: Path) -> None:
    if not input_pdf.exists():
        raise FileNotFoundError(f"Input PDF not found: {input_pdf}")

    all_frames = []

    # Some reasonable defaults for table detection; tweak if needed for your file
    table_settings = {
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "snap_tolerance": 3,
        "join_tolerance": 3,
        "edge_min_length": 3,
        "min_words_vertical": 1,
        "min_words_horizontal": 1,
        "keep_blank_chars": False,
        "text_tolerance": 2,
        "intersection_tolerance": 3,
    }

    with pdfplumber.open(str(input_pdf)) as pdf:
        for page_idx, page in enumerate(pdf.pages, start=1):
            try:
                tables = page.extract_tables(table_settings=table_settings)
            except Exception:
                # Fallback to default extraction if custom settings fail
                tables = page.extract_tables()

            if not tables:
                # Try a looser strategy that uses text/lines hybrid
                try:
                    tables = page.find_tables(table_settings=table_settings)
                    tables = [t.extract() for t in tables]
                except Exception:
                    tables = []

            for tbl_idx, table in enumerate(tables or [], start=1):
                if not table:
                    continue
                rect_rows = _rectangularize(table)
                df = pd.DataFrame(rect_rows)

                # Heuristic: if first row has any non-empty header-like values and
                # subsequent rows seem data-like, set it as header
                if df.shape[0] > 1:
                    first_row_nonempty = df.iloc[0].astype(str).str.strip().replace({"None": ""}).astype(bool).sum()
                    second_row_nonempty = df.iloc[1].astype(str).str.strip().replace({"None": ""}).astype(bool).sum()
                    if first_row_nonempty >= second_row_nonempty and first_row_nonempty > 0:
                        df.columns = [str(c) if (c is not None and str(c).strip() != "") else f"col_{i+1}" for i, c in enumerate(df.iloc[0].tolist())]
                        df = df.iloc[1:].reset_index(drop=True)
                    else:
                        df.columns = [f"col_{i+1}" for i in range(df.shape[1])]
                else:
                    df.columns = [f"col_{i+1}" for i in range(df.shape[1])]

                df.insert(0, "page_number", page_idx)
                df.insert(1, "table_index", tbl_idx)
                all_frames.append(df)

    if not all_frames:
        # No tables detected; try extracting text per page as a last resort
        with pdfplumber.open(str(input_pdf)) as pdf:
            rows = []
            for page_idx, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                for line in text.splitlines():
                    rows.append([page_idx, 1, line])
            if not rows:
                raise RuntimeError("No tables or text could be extracted from the PDF.")
            df_text = pd.DataFrame(rows, columns=["page_number", "table_index", "text"])
            df_text.to_csv(output_csv, index=False)
            return

    combined = pd.concat(all_frames, ignore_index=True)
    # Write CSV
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(output_csv, index=False)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Extract tables from a PDF to CSV")
    parser.add_argument("--input", required=True, help="Path to input PDF")
    parser.add_argument("--output", required=True, help="Path to output CSV")
    args = parser.parse_args(argv)

    input_pdf = Path(args.input).expanduser().resolve()
    output_csv = Path(args.output).expanduser().resolve()

    try:
        extract_pdf_tables_to_csv(input_pdf, output_csv)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    print(f"CSV written to: {output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
