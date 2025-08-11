#!/usr/bin/env python3
import json
from pathlib import Path

DATA = Path('data')

def load_many(paths):
    rows = []
    for p in paths:
        fp = DATA / p
        if fp.exists():
            try:
                rows.extend(json.loads(fp.read_text(encoding='utf-8')))
            except Exception:
                pass
    return rows

def summarize(label, rows):
    uniq_colleges = set()
    uniq_pairs = set()
    for r in rows:
        c = (r.get('college') or r.get('college_name') or '').strip().lower()
        b = (r.get('branch') or r.get('program') or r.get('course') or '').strip().lower()
        if c:
            uniq_colleges.add(c)
        if c and b:
            uniq_pairs.add((c, b))
    return {
        'label': label,
        'total_rows': len(rows),
        'unique_colleges': len(uniq_colleges),
        'unique_college_branch_pairs': len(uniq_pairs),
    }

def main():
    jee_files = [
        'jee_1000_cutoffs.json',
        'jee_massive_cutoffs.json',
        'jee_cutoffs_extended.json',
        'jee_cutoffs_extended_v2.json',
        'diverse_colleges_jee.json',
        'gujarat_colleges_jee.json',
        'uttar_pradesh_colleges_jee.json',
    ]
    neet_files = [
        'neet_1000_cutoffs.json',
        'neet_massive_cutoffs.json',
        'neet_cutoffs.json',
        'neet_cutoffs_extended.json',
    ]

    jee_rows = load_many(jee_files)
    neet_rows = load_many(neet_files)

    out = {
        'jee': summarize('jee', jee_rows),
        'neet': summarize('neet', neet_rows),
    }
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()


