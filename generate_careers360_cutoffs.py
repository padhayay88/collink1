#!/usr/bin/env python3
import json
from pathlib import Path
from careers360_scraper import generate_comprehensive_cutoffs


def main():
    data_dir = Path("data")
    jee_file = data_dir / "careers360_jee_colleges.json"
    neet_file = data_dir / "careers360_neet_colleges.json"

    if not jee_file.exists() or not neet_file.exists():
        raise SystemExit("Expected colleges JSON files not found in data/. Run careers360_scraper.py first.")

    with open(jee_file, "r", encoding="utf-8") as f:
        jee = json.load(f)
    with open(neet_file, "r", encoding="utf-8") as f:
        neet = json.load(f)

    jee_cutoffs = generate_comprehensive_cutoffs(jee, "jee")
    neet_cutoffs = generate_comprehensive_cutoffs(neet, "neet")

    with open(data_dir / "careers360_jee_cutoffs.json", "w", encoding="utf-8") as f:
        json.dump(jee_cutoffs, f, indent=2, ensure_ascii=False)
    with open(data_dir / "careers360_neet_cutoffs.json", "w", encoding="utf-8") as f:
        json.dump(neet_cutoffs, f, indent=2, ensure_ascii=False)

    summary = {
        "jee_cutoffs": len(jee_cutoffs),
        "neet_cutoffs": len(neet_cutoffs),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
