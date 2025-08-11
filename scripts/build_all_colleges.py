import json
import os
from pathlib import Path
from typing import Dict, Any, Iterable


INCLUDE_FILES_EXACT = {
    'college_info.json',
    'college_info_enhanced.json',
    'jee_cutoffs.json',
    'jee_cutoffs_extended.json',
    'jee_cutoffs_extended_v2.json',
    'neet_cutoffs.json',
    'neet_cutoffs_extended.json',
    'diverse_colleges_jee.json',
    'uttar_pradesh_colleges_jee.json',
    'gujarat_colleges_jee.json',
}

# Additionally include any file that contains 'colleges' in its name, but exclude massive/huge cutoffs
EXCLUDE_SUBSTRINGS = {
    'massive_cutoffs',
    '10000_cutoffs',
}


def should_include(filename: str) -> bool:
    name = filename.lower()
    if name in INCLUDE_FILES_EXACT:
        return True
    if 'colleges' in name and not any(x in name for x in EXCLUDE_SUBSTRINGS):
        return True
    return False


def load_rows(path: Path) -> Iterable[Dict[str, Any]]:
    try:
        text = path.read_text(encoding='utf-8')
        data = json.loads(text)
    except Exception:
        return []

    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]

    if isinstance(data, dict):
        for key in ('colleges', 'data', 'items', 'rows'):
            if key in data and isinstance(data[key], list):
                return [row for row in data[key] if isinstance(row, dict)]
        return []

    return []


def merge_info(existing: Dict[str, Any], new_row: Dict[str, Any]) -> Dict[str, Any]:
    # Preserve name case from existing; otherwise set from new row
    if not existing.get('name'):
        existing['name'] = (new_row.get('college') or new_row.get('name') or '').strip()
    # Prefer non-empty location/type if missing
    if not existing.get('location') and new_row.get('location'):
        existing['location'] = new_row.get('location')
    if not existing.get('type') and new_row.get('type'):
        existing['type'] = new_row.get('type')
    # Track exams present
    exams = existing.setdefault('exams', [])
    exam_type = str(new_row.get('exam_type') or '').strip().lower()
    if exam_type and exam_type not in exams:
        exams.append(exam_type)
    return existing


def main() -> None:
    data_dir = Path('data')
    if not data_dir.exists():
        print('data directory not found')
        return

    index: Dict[str, Dict[str, Any]] = {}

    for path in sorted(data_dir.glob('*.json')):
        fname = path.name
        if not should_include(fname):
            continue
        for row in load_rows(path):
            raw_name = (row.get('college') or row.get('name') or '').strip()
            if not raw_name:
                continue
            key = raw_name.lower()
            if key not in index:
                index[key] = {'name': raw_name, 'location': None, 'type': None, 'exams': []}
            index[key] = merge_info(index[key], row)

    # Normalize and sort
    colleges = []
    for item in index.values():
        colleges.append({
            'name': item['name'],
            'location': item.get('location') or None,
            'type': item.get('type') or None,
            'exams': sorted([e for e in item.get('exams', []) if e])
        })
    colleges.sort(key=lambda x: x['name'].lower())

    out_path = data_dir / 'all_colleges.json'
    out = {
        'total': len(colleges),
        'colleges': colleges,
        'note': 'Aggregated from multiple data/*.json sources with deduplication by name (case-insensitive).'
    }
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Saved {len(colleges)} unique colleges to {out_path}')


if __name__ == '__main__':
    main()


