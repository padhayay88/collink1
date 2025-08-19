import csv
import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup

NIRF_ENGINEERING_URL = "https://www.nirfindia.org/Rankings/2024/EngineeringRanking.html"
OUTPUT_DIR = Path(__file__).resolve().parents[2] / 'data'
OUTPUT_CSV = OUTPUT_DIR / 'engineering_nirf_2024.csv'

# Columns we will try to capture from NIRF table
COLUMNS = [
    'rank',
    'institute',
    'location',
    'state',
    'nirf_score'
]


def extract_text(el):
    if not el:
        return ''
    return ' '.join(el.get_text(strip=True).split())


def parse_page(html: str):
    soup = BeautifulSoup(html, 'html.parser')

    # NIRF pages often render a table of rankings; try common selectors
    table = soup.find('table')
    if not table:
        # Try any table with headers that contain Rank or Institute
        for t in soup.find_all('table'):
            headers = [extract_text(th).lower() for th in t.find_all(['th', 'td'], recursive=False)]
            if any('rank' in h for h in headers) or any('institute' in h for h in headers):
                table = t
                break

    if not table:
        raise RuntimeError('Could not find rankings table on the page')

    rows_out = []

    # Try to detect header row
    header_cells = table.find('tr')
    if header_cells:
        header_cells = [extract_text(c).lower() for c in header_cells.find_all(['th', 'td'])]
    else:
        header_cells = []

    for tr in table.find_all('tr'):
        cells = tr.find_all(['td', 'th'])
        if len(cells) < 2:
            continue
        texts = [extract_text(c) for c in cells]

        # Heuristic: first numeric column is rank; institute usually second
        rank_val = ''
        institute = ''
        location = ''
        state = ''
        score = ''

        # map based on common patterns
        for i, val in enumerate(texts):
            low = val.lower()
            if rank_val == '' and val.replace('.', '', 1).isdigit():
                rank_val = val
                continue
            if institute == '' and i <= 2 and len(val) > 2:
                institute = val
                continue
            # score often appears as last numeric/float value
            if score == '' and any(ch.isdigit() for ch in val) and ('score' in low or i == len(texts) - 1):
                # keep raw; parse as float where possible downstream
                score = val

        # Some tables include location/state in separate columns
        # Try to infer from remaining cells
        if not location and len(texts) >= 3:
            # Often the third cell is location
            location = texts[2]
        # Split state if location contains comma
        if location and ',' in location and not state:
            parts = [p.strip() for p in location.split(',') if p.strip()]
            if len(parts) >= 2:
                state = parts[-1]
                location = ', '.join(parts[:-1])

        rows_out.append({
            'rank': rank_val,
            'institute': institute,
            'location': location,
            'state': state,
            'nirf_score': score,
        })

    # Filter out rows without a rank or institute
    rows_out = [r for r in rows_out if r['institute'] and r['rank']]
    return rows_out


def save_csv(rows):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                'rank': r.get('rank', ''),
                'institute': r.get('institute', ''),
                'location': r.get('location', ''),
                'state': r.get('state', ''),
                'nirf_score': r.get('nirf_score', ''),
            })


def main():
    print(f"Fetching NIRF Engineering page: {NIRF_ENGINEERING_URL}")
    resp = requests.get(NIRF_ENGINEERING_URL, timeout=30)
    resp.raise_for_status()
    rows = parse_page(resp.text)
    if not rows:
        raise RuntimeError('No rows parsed from NIRF page')
    save_csv(rows)
    print(f"Saved {len(rows)} rows to {OUTPUT_CSV}")


if __name__ == '__main__':
    main()
