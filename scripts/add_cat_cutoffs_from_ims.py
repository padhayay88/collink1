import json
import math
import re
from pathlib import Path
from typing import List, Dict, Any

import requests
from bs4 import BeautifulSoup

IMS_URL = "https://www.imsindia.com/blog/cat/cat-cutoff/"
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = DATA_DIR / "cat_cutoffs.json"

# Assumption: approximate total candidates to convert percentile to rank
TOTAL_CANDIDATES = 300_000

# Basic normalization for college names
NORMALIZE = {
    "iim a": "Indian Institute of Management Ahmedabad (IIMA)",
    "iim b": "Indian Institute of Management Bangalore (IIMB)",
    "iim c": "Indian Institute of Management Calcutta (IIMC)",
    "iim l": "Indian Institute of Management Lucknow (IIML)",
}


def percentile_to_rank(percentile: float) -> int:
    percentile = max(0.0, min(100.0, percentile))
    # rank ~ (100 - p)% of total
    rank = ((100.0 - percentile) / 100.0) * TOTAL_CANDIDATES
    return max(1, int(math.ceil(rank)))


def normalize_name(name: str) -> str:
    key = re.sub(r"\s+", " ", name.strip()).lower()
    for k, v in NORMALIZE.items():
        if key.startswith(k):
            return v
    return name.strip()


def extract_percentile_number(text: str) -> float:
    # Examples: "99+", "99.5", ">=99", "95-97" -> take lower bound
    txt = text.strip().replace("%", "")
    m = re.search(r"(\d{2,3}(?:\.\d+)?)", txt)
    if not m:
        return -1.0
    val = float(m.group(1))
    # If it's a range like 95-97, lower bound
    range_m = re.search(r"^(\d{2,3}(?:\.\d+)?)\s*[-–]", txt)
    if range_m:
        val = float(range_m.group(1))
    # If it's 99+, keep as 99
    return min(val, 100.0)


def parse_ims_page(html: str) -> List[Dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")

    cutoffs: List[Dict[str, Any]] = []

    # Strategy 1: Parse tables with college and cutoff/percentile columns
    for table in soup.find_all("table"):
        headers = [th.get_text(strip=True).lower() for th in table.find_all("th")]
        rows = table.find_all("tr")
        for tr in rows[1:]:
            cols = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
            if not cols or len(cols) < 2:
                continue
            text_row = " | ".join(cols).lower()
            # Identify likely college and percentile fields
            college = cols[0]
            percentile_text = None
            # Try to find the first column that looks like percentile
            for c in cols[1:]:
                if re.search(r"\d{2}(?:\.\d+)?\s*%?|\d{2}\+", c):
                    percentile_text = c
                    break
            if not percentile_text:
                continue

            p = extract_percentile_number(percentile_text)
            if p < 0:
                continue

            college_name = normalize_name(college)
            closing_rank = percentile_to_rank(p)

            cutoffs.append({
                "college": college_name,
                "branch": "MBA",
                "opening_rank": max(1, int(closing_rank * 0.5)),  # rough band
                "closing_rank": closing_rank,
                "category": "General",
                "quota": "All India",
                "location": "",
                "exam_type": "cat"
            })

    # Strategy 2: Parse list items/paragraphs with patterns like "IIM A - 99+ percentile"
    for li in soup.find_all(["li", "p"]):
        text = li.get_text(" ", strip=True)
        if not text:
            continue
        m = re.search(r"(iim\s*[a-z]+|[A-Z][A-Za-z &()]+)\s*[-:–]\s*(\d{2,3}(?:\.\d+)?\+?|\d{2,3}\s*%|\d{2,3}\s*-\s*\d{2,3})\s*percentile", text, re.IGNORECASE)
        if not m:
            continue
        college_raw = m.group(1)
        pct_txt = m.group(2)
        p = extract_percentile_number(pct_txt)
        if p < 0:
            continue
        college_name = normalize_name(college_raw)
        closing_rank = percentile_to_rank(p)
        cutoffs.append({
            "college": college_name,
            "branch": "MBA",
            "opening_rank": max(1, int(closing_rank * 0.5)),
            "closing_rank": closing_rank,
            "category": "General",
            "quota": "All India",
            "location": "",
            "exam_type": "cat"
        })

    # Deduplicate by college+branch, keep best (lowest) closing_rank
    dedup: Dict[str, Dict[str, Any]] = {}
    for c in cutoffs:
        key = (c["college"].lower(), c["branch"].lower())
        k = "|".join(key)
        if k not in dedup or c["closing_rank"] < dedup[k]["closing_rank"]:
            dedup[k] = c

    return list(dedup.values())


def main():
    print(f"Fetching IMS CAT cutoff page: {IMS_URL}")
    resp = requests.get(IMS_URL, timeout=30)
    resp.raise_for_status()

    data = parse_ims_page(resp.text)
    print(f"Parsed {len(data)} CAT cutoff entries")

    if not data:
        print("Warning: No data parsed. The page structure may have changed.")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved CAT cutoffs to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
