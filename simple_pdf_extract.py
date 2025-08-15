#!/usr/bin/env python3
"""
Simple PDF extraction script for college data
"""
import json
import re
from pathlib import Path

# PyMuPDF is imported as 'fitz'
try:
    import fitz  # PyMuPDF
except Exception as e:
    fitz = None
    print("PyMuPDF (fitz) not installed. Please install with: pip install PyMuPDF")

def extract_colleges_from_pdf(pdf_path: str | None = None):
    """Extract colleges from PDF with error handling"""
    if not fitz:
        return []

    # Default to project-root PDF name if not provided
    pdf_path = pdf_path or "Consolidated list of All Universities.pdf"
    pdf_file = Path(pdf_path)

    # If a relative path was given but file lives in the project root, try that
    if not pdf_file.exists():
        # Try absolute path from current file's directory up to project root
        project_root_pdf = Path(__file__).resolve().parent / pdf_file.name
        if project_root_pdf.exists():
            pdf_file = project_root_pdf

    if not pdf_file.exists():
        print(f"Error: PDF not found at {pdf_file}")
        return []

    try:
        print(f"Opening PDF: {pdf_file}")
        doc = fitz.open(pdf_file)
        print(f"PDF has {doc.page_count} pages")

        all_text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            page_text = page.get_text()
            all_text += page_text + "\n"
            print(f"Extracted page {page_num + 1}")

        doc.close()

        # Ensure data directory exists
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)

        # Save raw text for inspection
        with open("pdf_raw_text.txt", "w", encoding="utf-8") as f:
            f.write(all_text)
        print("Saved raw text to pdf_raw_text.txt")

        # Parse colleges
        colleges = []
        lines = all_text.split('\n')

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # Look for numbered entries (potential rankings)
            if re.match(r'^\d+\.?\s+', line):
                rank_match = re.match(r'^(\d+)\.?\s+(.*)', line)
                if rank_match:
                    try:
                        rank = int(rank_match.group(1))
                    except ValueError:
                        continue
                    name = rank_match.group(2).strip()

                    college = {
                        "rank": rank,
                        "college_name": name,
                        "university_name": name,
                        "type": "University",
                        "category": "General",
                        "source": "PDF_Ranking_List"
                    }
                    colleges.append(college)

        print(f"Found {len(colleges)} colleges")

        # Save colleges
        colleges_file = data_dir / "pdf_ranking_colleges.json"

        with open(colleges_file, "w", encoding="utf-8") as f:
            json.dump(colleges, f, indent=2, ensure_ascii=False)

        print(f"Saved colleges to {colleges_file}")

        # Show preview
        print("\nFirst 10 colleges:")
        for college in colleges[:10]:
            print(f"Rank {college['rank']}: {college['college_name']}")

        return colleges

    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    import sys
    pdf_arg = sys.argv[1] if len(sys.argv) > 1 else None
    colleges = extract_colleges_from_pdf(pdf_arg)
    print(f"\nTotal colleges extracted: {len(colleges)}")
