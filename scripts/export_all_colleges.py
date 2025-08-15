import json
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / 'colleges.db'
ROOT_DATA = Path(__file__).resolve().parents[1] / 'data'
FRONTEND_PUBLIC_DATA = Path(__file__).resolve().parents[1] / 'frontend' / 'public' / 'data'

ROOT_DATA.mkdir(parents=True, exist_ok=True)
FRONTEND_PUBLIC_DATA.mkdir(parents=True, exist_ok=True)

OUT_FILENAME = 'all_colleges.json'


def export_all():
    if not DB_PATH.exists():
        raise SystemExit(f"DB not found at {DB_PATH}")

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    rows = cur.execute(
        """
        SELECT id, name, state, ownership, city, website, phone, email
        FROM colleges
        ORDER BY name COLLATE NOCASE
        """
    ).fetchall()

    data = [dict(r) for r in rows]

    for target in [ROOT_DATA / OUT_FILENAME, FRONTEND_PUBLIC_DATA / OUT_FILENAME]:
        with open(target, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Wrote {len(data)} colleges to {target}")

    conn.close()


if __name__ == '__main__':
    export_all()
