#!/usr/bin/env python3
"""
Extract MBA colleges from NIRF 2024 PDF and export to CSV.

Input:  MBA_Colleges_India_NIRF_2024.pdf (project root)
Output: data/mba_nirf_2024.csv

Strategy:
- Try pdfplumber table extraction (best for tabular PDFs)
- Fallback to text parsing with regex if tables not detected
- Derive percentile from N (count of colleges): percentile = round(100 * (1 - (rank-1)/(N-1)), 4)

Columns:
rank, institute, location, nirf_score, percentile

Requires: pdfplumber (pip install pdfplumber)
"""
from __future__ import annotations
import csv
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

PDF_NAME = "MBA_Colleges_India_NIRF_2024.pdf"
OUTPUT_CSV = Path("data") / "mba_nirf_2024.csv"

@dataclass
class Row:
    rank: int
    institute: str
    location: Optional[str] = None
    nirf_score: Optional[float] = None

    def to_list(self, percentile: Optional[float] = None) -> List[str]:
        return [
            str(self.rank),
            self.institute.strip(),
            (self.location or "").strip(),
            ("" if self.nirf_score is None else f"{self.nirf_score}"),
            ("" if percentile is None else f"{percentile}")
        ]

def try_extract_with_pdfplumber(pdf_path: Path) -> List[Row]:
    try:
        import pdfplumber  # type: ignore
    except Exception as e:
        return []

    rows: List[Row] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            # Try tables first
            try:
                tables = page.extract_tables() or []
            except Exception:
                tables = []
            for table in tables:
                # Normalize table rows (strip cells)
                for raw in table:
                    cells = [(c or "").strip() for c in raw]
                    if not cells:
                        continue
                    # Identify rows where first cell is rank
                    first = cells[0]
                    if re.fullmatch(r"\d{1,3}", first):
                        rank = int(first)
                        # Heuristics: next cells may include name, location, score columns
                        institute = None
                        location = None
                        nirf_score = None
                        # Try common patterns
                        # Pattern A: [rank, institute, city/state, score]
                        if len(cells) >= 3:
                            institute = cells[1]
                            # Find a score-like cell among the tail
                            score_idx = None
                            for idx in range(2, len(cells)):
                                if re.fullmatch(r"\d{1,2}\.\d{1,3}", cells[idx]) or re.fullmatch(r"\d{1,3}(?:\.\d+)?", cells[idx]):
                                    score_idx = idx
                                    break
                            if score_idx is not None:
                                try:
                                    nirf_score = float(cells[score_idx])
                                except Exception:
                                    nirf_score = None
                                # location likely between institute and score
                                if score_idx - 1 >= 2:
                                    location = cells[score_idx - 1]
                                elif len(cells) >= 3:
                                    location = cells[2]
                            else:
                                # No score detected; assume [rank, institute, location]
                                location = cells[2] if len(cells) > 2 else None
                        # Fallback: join all non-empty cells except rank as institute
                        if not institute:
                            institute = " ".join([c for c in cells[1:] if c]).strip()
                        if institute:
                            rows.append(Row(rank=rank, institute=institute, location=location, nirf_score=nirf_score))
            # Fallback: parse text lines on this page if no tables found anything
            # We'll do text fallback after all pages if still empty
    return rows

def extract_from_text(pdf_path: Path) -> List[Row]:
    # Use PyMuPDF if available; else pdfplumber text
    text = None
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(str(pdf_path))
        parts = []
        for page in doc:
            parts.append(page.get_text())
        doc.close()
        text = "\n".join(parts)
    except Exception:
        try:
            import pdfplumber  # type: ignore
            parts = []
            with pdfplumber.open(str(pdf_path)) as pdf:
                for page in pdf.pages:
                    parts.append(page.extract_text() or "")
            text = "\n".join(parts)
        except Exception:
            text = None

    if not text:
        return []

    rows: List[Row] = []
    # Regex for lines starting with rank
    line_re = re.compile(r"^(?P<rank>\d{1,3})\.?\s+(?P<rest>.+)$")
    score_re = re.compile(r"(\d{1,2}\.\d{1,3})$")  # trailing score like 83.48

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        m = line_re.match(line)
        if not m:
            continue
        try:
            rank = int(m.group("rank"))
        except Exception:
            continue
        rest = m.group("rest").strip()
        # Try split by score at end
        score = None
        sm = score_re.search(rest)
        if sm:
            try:
                score = float(sm.group(1))
            except Exception:
                score = None
            rest = rest[: sm.start()].strip()
        # Try to separate location at the end after a comma
        institute = rest
        location = None
        # Heuristic: if rest contains ", <City/State>" at end
        if "," in rest:
            parts = [p.strip() for p in rest.split(",")]
            if len(parts) >= 2 and all(parts):
                # Assume last token(s) form location
                location = parts[-1]
                institute = ", ".join(parts[:-1])
        rows.append(Row(rank=rank, institute=institute, location=location, nirf_score=score))

    # Deduplicate by rank and keep first occurrence
    seen = set()
    unique: List[Row] = []
    for r in rows:
        if r.rank not in seen:
            seen.add(r.rank)
            unique.append(r)
    unique.sort(key=lambda r: r.rank)
    return unique

def compute_percentiles(rows: List[Row]) -> List[Tuple[Row, float]]:
    if not rows:
        return []
    n = len(rows)
    if n == 1:
        return [(rows[0], 100.0)]
    out: List[Tuple[Row, float]] = []
    for r in rows:
        pct = 100.0 * (1.0 - (r.rank - 1) / (n - 1))
        out.append((r, round(pct, 4)))
    return out

def write_csv(rows_with_pct: List[Tuple[Row, float]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rank", "institute", "location", "nirf_score", "percentile"])  # header
        for r, pct in rows_with_pct:
            w.writerow(r.to_list(percentile=pct))


def main() -> None:
    pdf_path = Path(PDF_NAME)
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return

    print("🔎 Trying table extraction (pdfplumber)...")
    rows = try_extract_with_pdfplumber(pdf_path)

    if not rows:
        print("⚠️  Table extraction failed or produced no rows. Falling back to text parsing...")
        rows = extract_from_text(pdf_path)

    if not rows:
        print("❌ Could not extract any rows from the PDF.")
        print("Tip: Install pdfplumber or PyMuPDF: pip install pdfplumber PyMuPDF")
        return

    print(f"✓ Extracted {len(rows)} rows. Computing percentiles and writing CSV...")
    rows_with_pct = compute_percentiles(rows)
    write_csv(rows_with_pct, OUTPUT_CSV)
    print(f"✅ Wrote {len(rows_with_pct)} rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
