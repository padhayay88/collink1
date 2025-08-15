#!/usr/bin/env python3
import json
import re
from pathlib import Path
from typing import List, Set, Dict, Tuple

import fitz  # PyMuPDF
import pandas as pd
import requests

from bs4 import BeautifulSoup  # type: ignore

PDF_PATH = Path("Consolidated list of All Universities.pdf")
CSV_PATH = Path("universities_list.csv")
JEE_JSON_PATH = Path("data") / "jee_massive_colleges.json"
NEET_JSON_PATH = Path("data") / "neet_massive_colleges.json"
CAREERS360_ENGINEERING_BASE = "https://engineering.careers360.com/colleges/list-of-engineering-colleges-in-india"
MAX_RANK_CAP = 200_000


def normalize_name(name: str) -> str:
    n = name.strip()
    n = re.sub(r"\s+", " ", n)
    return n.lower()


def extract_university_names_from_pdf(pdf_path: Path) -> List[str]:
    if not pdf_path.exists():
        print(f"❌ PDF not found: {pdf_path}")
        return []
    try:
        doc = fitz.open(pdf_path)
        text_parts: List[str] = []
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()
        text = "\n".join(text_parts)
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        names: List[str] = []
        for ln in lines:
            # Remove leading S.No patterns like "123." or "123)"
            clean = re.sub(r"^\s*\d+\s*[\.|\)]\s*", "", ln)
            # Heuristics: treat lines with keywords as potential university names
            if any(k in clean.lower() for k in [
                "university", "institute", "college", "iit", "nit", "aiims"
            ]):
                # Avoid headers
                if len(clean) >= 5 and not clean.lower().startswith(("s.no", "state/ut", "type", "year")):
                    names.append(clean)
        # Deduplicate while preserving order
        seen: Set[str] = set()
        result: List[str] = []
        for n in names:
            key = normalize_name(n)
            if key not in seen:
                seen.add(key)
                result.append(n)
        return result
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return []


def fetch_engineering_page(page: int) -> Tuple[List[Dict[str, str]], bool]:
    url = CAREERS360_ENGINEERING_BASE + (f"?page={page}" if page > 1 else "")
    try:
        resp = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            print(f"HTTP {resp.status_code} at {url}")
            return [], False
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("a[href*='/colleges/']")
        results: List[Dict[str, str]] = []
        for a in cards:
            name = a.get_text(strip=True)
            if not name or len(name) < 3:
                continue
            # Filter out non-college links
            if not any(k in name.lower() for k in ["college", "institute", "iit", "nit", "iiit", "university"]):
                continue
            # Try to find a nearby location/state element
            state = ""
            parent = a.find_parent()
            if parent:
                loc_el = parent.find(string=re.compile(r",\s*[A-Za-z ]+$"))
                if loc_el and isinstance(loc_el, str):
                    m = re.search(r",\s*([A-Za-z ]+)$", loc_el)
                    if m:
                        state = m.group(1).strip()
            results.append({"name": name, "state": state})
        # Heuristic: stop if very few results on page
        return results, len(results) > 5
    except Exception as e:
        print(f"❌ Error fetching page {page}: {e}")
        return [], False


def fetch_all_engineering(max_pages: int = 500) -> List[Dict[str, str]]:
    print("🌐 Fetching engineering colleges from Careers360 (engineering subdomain)...")
    all_rows: List[Dict[str, str]] = []
    for p in range(1, max_pages + 1):
        rows, should_continue = fetch_engineering_page(p)
        if rows:
            all_rows.extend(rows)
            print(f"  Page {p}: +{len(rows)} (total {len(all_rows)})")
        if not should_continue:
            break
    # Deduplicate by name
    seen: Set[str] = set()
    uniq: List[Dict[str, str]] = []
    for r in all_rows:
        k = normalize_name(r["name"])
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    print(f"✅ Careers360 engineering list: {len(uniq)} unique colleges")
    return uniq


def fetch_collegedunia_neet_colleges(max_pages: int = 50) -> List[Dict[str, str]]:
    """Fetch NEET colleges from Collegedunia.

    Strategy:
      1) Try to extract college anchors from predictor landing page
         https://collegedunia.com/neet-college-predictor (may have some static links)
      2) Fallback to MBBS college listings: https://collegedunia.com/medical/mbbs-colleges
         and iterate paginated results for broader coverage.
    Returns list of {name, state} (state best-effort; may be empty).
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    results: List[Dict[str, str]] = []

    def add_name(n: str, state: str = ""):
        n = n.strip()
        if len(n) < 3:
            return
        if not any(k in n.lower() for k in ["college", "institute", "medical", "aiims", "jipmer", "hospital"]):
            return
        results.append({"name": n, "state": state})

    # 1) Predictor landing page (best-effort)
    try:
        url = "https://collegedunia.com/neet-college-predictor"
        r = requests.get(url, timeout=20, headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a"):
                text = a.get_text(strip=True)
                add_name(text)
    except Exception:
        pass

    # 2) MBBS colleges listing with pagination
    try:
        base = "https://collegedunia.com/medical/mbbs-colleges"
        for p in range(1, max_pages + 1):
            page_url = base + (f"?page={p}" if p > 1 else "")
            try:
                resp = requests.get(page_url, timeout=20, headers=headers)
                if resp.status_code != 200:
                    break
                soup = BeautifulSoup(resp.text, "html.parser")
                cards = soup.select("a[href*='/college/'], a.cd__clg__name, a.cd__card__image")
                found = 0
                for a in cards:
                    name = a.get_text(strip=True)
                    if name:
                        add_name(name)
                        found += 1
                # Heuristic: stop if page returns very few new items
                if found < 5:
                    break
            except Exception:
                break
    except Exception:
        pass

    # Deduplicate while preserving order
    seen: Set[str] = set()
    uniq: List[Dict[str, str]] = []
    for r in results:
        k = normalize_name(r["name"])
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    print(f"✅ Collegedunia NEET colleges discovered: {len(uniq)}")
    return uniq


def merge_into_csv(csv_path: Path, extracted_names: List[str]) -> int:
    if not csv_path.exists():
        print(f"❌ CSV not found: {csv_path}")
        return 0
    df = pd.read_csv(csv_path)
    if "University Name" not in df.columns:
        raise ValueError("CSV must have a 'University Name' column")
    existing_norm = set(df["University Name"].fillna("").map(normalize_name))

    to_add: List[Dict[str, str]] = []
    max_sno = int(df["S.No"].max()) if "S.No" in df.columns and pd.api.types.is_numeric_dtype(df["S.No"]) else len(df)

    for name in extracted_names:
        if normalize_name(name) not in existing_norm:
            max_sno += 1
            to_add.append({
                "S.No": max_sno,
                "University Name": name,
                "State/UT": "Unknown",
                "Type": "Unknown",
                "Year Established": ""
            })

    if to_add:
        df_new = pd.DataFrame(to_add)
        df = pd.concat([df, df_new], ignore_index=True)
        df.to_csv(csv_path, index=False)
        print(f"✅ Appended {len(to_add)} new rows to {csv_path}")
    else:
        print("ℹ️ No new universities to add to CSV")
    return len(to_add)


def merge_careers360_into_csv(csv_path: Path, careers_rows: List[Dict[str, str]]) -> int:
    names = [r["name"] for r in careers_rows]
    return merge_into_csv(csv_path, names)


def ensure_in_jee_dataset(jee_path: Path, names_states: List[Dict[str, str]], max_rank_cap: int = MAX_RANK_CAP) -> Tuple[int, int]:
    if not jee_path.exists():
        print(f"❌ JEE dataset not found: {jee_path}")
        return 0, 0
    with open(jee_path, "r", encoding="utf-8") as f:
        jee = json.load(f)

    existing_norm = set(normalize_name(item.get("name", "")) for item in jee)
    current_max_rank = max((int(item.get("rank", 0)) for item in jee), default=0)

    missing = [r for r in names_states if normalize_name(r["name"]) not in existing_norm]

    appended = 0
    replaced = 0

    # If we have headroom to append
    for r in list(missing):
        if current_max_rank < max_rank_cap:
            current_max_rank += 1
            jee.append({
                "name": r["name"],
                "type": "University",
                "state": r.get("state", "Unknown") or "Unknown",
                "rank": current_max_rank,
                "category": "jee",
                "source": "Careers360"
            })
            existing_norm.add(normalize_name(r["name"]))
            appended += 1
        else:
            break

    # If still missing and at cap, replace from the tail (prefer non-Careers360 sources)
    remaining_missing = [r for r in names_states if normalize_name(r["name"]) not in existing_norm]
    if remaining_missing:
        # Build list of candidate indices to replace (from end, prefer source CSV/PDF)
        replace_indices = []
        for idx in range(len(jee) - 1, -1, -1):
            src = str(jee[idx].get("source", ""))
            if src in ("CSV/PDF", ""):
                replace_indices.append(idx)
            if len(replace_indices) >= len(remaining_missing):
                break
        # If not enough, just take from tail
        while len(replace_indices) < len(remaining_missing) and len(replace_indices) < len(jee):
            replace_indices.append(len(jee) - 1 - len(replace_indices))

        for r, idx in zip(remaining_missing, replace_indices):
            rank_num = int(jee[idx].get("rank", max_rank_cap))
            jee[idx] = {
                "name": r["name"],
                "type": "University",
                "state": r.get("state", "Unknown") or "Unknown",
                "rank": rank_num,
                "category": "jee",
                "source": "Careers360"
            }
            replaced += 1

    with open(jee_path, "w", encoding="utf-8") as f:
        json.dump(jee, f, ensure_ascii=False, indent=2)

    return appended, replaced


def ensure_in_neet_dataset(neet_path: Path, names_states: List[Dict[str, str]], max_rank_cap: int = MAX_RANK_CAP) -> Tuple[int, int]:
    if not neet_path.exists():
        print(f"❌ NEET dataset not found: {neet_path}")
        return 0, 0
    with open(neet_path, "r", encoding="utf-8") as f:
        neet = json.load(f)

    existing_norm = set(normalize_name(item.get("name", "")) for item in neet)
    current_max_rank = max((int(item.get("rank", 0)) for item in neet), default=0)

    missing = [r for r in names_states if normalize_name(r["name"]) not in existing_norm]

    appended = 0
    replaced = 0

    for r in list(missing):
        if current_max_rank < max_rank_cap:
            current_max_rank += 1
            neet.append({
                "name": r["name"],
                "type": "Medical College",
                "state": r.get("state", "Unknown") or "Unknown",
                "rank": current_max_rank,
                "category": "neet",
                "source": "Collegedunia"
            })
            existing_norm.add(normalize_name(r["name"]))
            appended += 1
        else:
            break

    remaining_missing = [r for r in names_states if normalize_name(r["name"]) not in existing_norm]
    if remaining_missing:
        replace_indices = []
        for idx in range(len(neet) - 1, -1, -1):
            src = str(neet[idx].get("source", ""))
            if src in ("CSV/PDF", ""):
                replace_indices.append(idx)
            if len(replace_indices) >= len(remaining_missing):
                break
        while len(replace_indices) < len(remaining_missing) and len(replace_indices) < len(neet):
            replace_indices.append(len(neet) - 1 - len(replace_indices))

        for r, idx in zip(remaining_missing, replace_indices):
            rank_num = int(neet[idx].get("rank", max_rank_cap))
            neet[idx] = {
                "name": r["name"],
                "type": "Medical College",
                "state": r.get("state", "Unknown") or "Unknown",
                "rank": rank_num,
                "category": "neet",
                "source": "Collegedunia"
            }
            replaced += 1

    with open(neet_path, "w", encoding="utf-8") as f:
        json.dump(neet, f, ensure_ascii=False, indent=2)

    return appended, replaced


def main():
    print("🚀 Updating universities and JEE dataset from PDF + Careers360 → CSV → JSON")

    # 1) PDF → CSV
    names_pdf = extract_university_names_from_pdf(PDF_PATH)
    print(f"📄 Extracted {len(names_pdf)} names from PDF")
    added_csv_pdf = merge_into_csv(CSV_PATH, names_pdf)

    # 2) Careers360 engineering list → CSV
    rows_c360 = fetch_all_engineering()
    added_csv_c360 = merge_careers360_into_csv(CSV_PATH, rows_c360)

    # 3) Ensure all Careers360 engineering colleges are present in JEE dataset (append or replace tail)
    appended, replaced = ensure_in_jee_dataset(JEE_JSON_PATH, rows_c360, max_rank_cap=MAX_RANK_CAP)

    # 4) Collegedunia → NEET dataset (append or replace tail)
    print("\n🌐 Fetching NEET colleges from Collegedunia...")
    rows_cd_neet = fetch_collegedunia_neet_colleges()
    added_csv_cd = merge_into_csv(CSV_PATH, [r["name"] for r in rows_cd_neet])
    appended_neet, replaced_neet = ensure_in_neet_dataset(NEET_JSON_PATH, rows_cd_neet, max_rank_cap=MAX_RANK_CAP)

    print(f"\nSummary:")
    print(f"  +{added_csv_pdf} from PDF into CSV")
    print(f"  +{added_csv_c360} from Careers360 into CSV")
    print(f"  +{added_csv_cd} from Collegedunia into CSV")
    print(f"  +{appended} appended to JEE, {replaced} replaced (cap {MAX_RANK_CAP})")
    print(f"  +{appended_neet} appended to NEET, {replaced_neet} replaced (cap {MAX_RANK_CAP})")


if __name__ == "__main__":
    main()
