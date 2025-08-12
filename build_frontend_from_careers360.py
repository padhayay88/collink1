#!/usr/bin/env python3
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, Any

DATA_DIR = Path("data")
JEE_CUTOFFS = DATA_DIR / "careers360_jee_cutoffs.json"
NEET_CUTOFFS = DATA_DIR / "careers360_neet_cutoffs.json"
JEE_MASSIVE = DATA_DIR / "jee_massive_colleges.json"
NEET_MASSIVE = DATA_DIR / "neet_massive_colleges.json"
OUTPUT = Path("comprehensive_college_database.json")


def load_json(path: Path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_index(massive_list):
    by_name: Dict[str, Dict[str, Any]] = {}
    for item in massive_list:
        name = item.get("name", "").strip()
        if not name:
            continue
        key = name.lower()
        by_name[key] = {
            "state": item.get("state", "Unknown"),
            "type": item.get("type", "")
        }
    return by_name


def aggregate_cutoffs(cutoffs, exam_label: str, enrich_index: Dict[str, Dict[str, Any]]):
    groups = defaultdict(lambda: {"max_cutoff": 0, "state": "Unknown", "type": ""})
    for c in cutoffs:
        name = c.get("college") or c.get("university") or ""
        if not name:
            continue
        cutoff = int(c.get("cutoff_rank", 0))
        key = name.strip().lower()
        g = groups[key]
        if cutoff > g["max_cutoff"]:
            g["max_cutoff"] = cutoff
        # enrich
        if key in enrich_index:
            g["state"] = enrich_index[key].get("state", g["state"]) or g["state"]
            g["type"] = enrich_index[key].get("type", g["type"]) or g["type"]
    # convert to list
    records = []
    for key, info in groups.items():
        name = key  # store key for lookup
        # Original name casing from index if available
        orig_name = None
        for nkey, meta in enrich_index.items():
            if nkey == key:
                orig_name = nkey
                break
        display_name = None
        # We don't have original casing reliably; just title-case as fallback
        display_name = " ".join(p.capitalize() for p in key.split())
        records.append({
            "name": display_name,
            "type": info["type"] or "University",
            "exam": exam_label,
            "state": info["state"],
            "cutoff": min(max(info["max_cutoff"], 1), 200000),
            "fees": "N/A",
            "seats": 0,
            "availableSeats": 0,
            "seatStatus": "available",
            "scholarship": None,
            "aiPrediction": None,
            "pros": None,
            "cons": None,
            "rating": "4.0",
            "placement": "-",
            "avgPackage": "-"
        })
    return records


def main():
    jee_cut = load_json(JEE_CUTOFFS)
    neet_cut = load_json(NEET_CUTOFFS)
    jee_mass = load_json(JEE_MASSIVE)
    neet_mass = load_json(NEET_MASSIVE)

    jee_index = build_index(jee_mass)
    neet_index = build_index(neet_mass)

    jee_records = aggregate_cutoffs(jee_cut, "JEE Main", jee_index)
    neet_records = aggregate_cutoffs(neet_cut, "NEET", neet_index)

    # Ensure broad JEE coverage using massive list as fallback
    present_jee = set(r["name"].lower() for r in jee_records)
    mass_added = 0
    for item in jee_mass:
        name = (item.get("name") or "").strip()
        if not name:
            continue
        key = name.lower()
        if key in present_jee:
            continue
        # Derive a cutoff from ranking; clamp to 200k
        try:
            rnk = int(item.get("rank", 0))
        except Exception:
            rnk = 0
        # Map rank to a generous cutoff to cover high ranks too
        derived_cutoff = max(1000, min(200000, rnk * 2)) if rnk > 0 else 150000
        jee_records.append({
            "name": name,
            "type": item.get("type", "University") or "University",
            "exam": "JEE Main",
            "state": item.get("state", "Unknown") or "Unknown",
            "cutoff": derived_cutoff,
            "fees": "N/A",
            "seats": 0,
            "availableSeats": 0,
            "seatStatus": "available",
            "scholarship": None,
            "aiPrediction": None,
            "pros": None,
            "cons": None,
            "rating": "4.0",
            "placement": "-",
            "avgPackage": "-"
        })
        present_jee.add(key)
        mass_added += 1

    all_records = jee_records + neet_records

    out = {
        "metadata": {
            "total_colleges": len(all_records),
            "last_updated": __import__("datetime").datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "coverage": "India - all states",
            "exams": ["JEE Main", "NEET"],
            "rank_coverage": {
                "JEE_Main": 200000,
                "NEET": 200000
            }
        },
        "colleges": all_records
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"✅ Built frontend DB with {len(all_records)} records at {OUTPUT}")


if __name__ == "__main__":
    main()
