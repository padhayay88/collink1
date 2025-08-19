import os
import json
import csv
import sqlite3
from pathlib import Path


def create_database(db_path: str = 'colleges.db'):
    """Create SQLite database with appropriate tables and indexes."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Core entities
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS colleges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        state TEXT,
        type TEXT,
        website TEXT,
        established_year INTEGER,
        ownership TEXT,
        university TEXT,
        address TEXT,
        city TEXT,
        pincode TEXT,
        phone TEXT,
        email TEXT,
        fax TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(name, state) ON CONFLICT IGNORE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS college_ranks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        college_id INTEGER NOT NULL,
        exam_type TEXT,
        year INTEGER,
        branch TEXT,
        opening_rank INTEGER,
        closing_rank INTEGER,
        category TEXT,
        quota TEXT,
        location TEXT,
        FOREIGN KEY (college_id) REFERENCES colleges(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS college_courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        college_id INTEGER NOT NULL,
        course_name TEXT,
        duration_years INTEGER,
        degree_awarded TEXT,
        intake_capacity INTEGER,
        FOREIGN KEY (college_id) REFERENCES colleges(id)
    )
    ''')

    # Helpful indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_colleges_name ON colleges(name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_colleges_state ON colleges(state)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ranks_college ON college_ranks(college_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ranks_exam_year ON college_ranks(exam_type, year)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ranks_branch ON college_ranks(branch)')

    conn.commit()
    return conn


def _ensure_college(cursor: sqlite3.Cursor, item: dict) -> int | None:
    """Insert or fetch a college and return its id."""
    name = item.get('college') or item.get('college_name') or item.get('name')
    if not name:
        return None

    state = item.get('state') or _extract_state(item)

    cursor.execute(
        '''INSERT OR IGNORE INTO colleges (name, state, website, type, ownership, university, address, city, pincode, phone, email, fax)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (
            name,
            state,
            item.get('website') or item.get('url'),
            item.get('type') or item.get('institute_type'),
            item.get('ownership') or item.get('type_of_college'),
            item.get('university') or item.get('affiliation'),
            item.get('address'),
            item.get('city') or _extract_city(item),
            item.get('pincode') or item.get('pin') or item.get('zip'),
            item.get('phone') or item.get('contact') or item.get('mobile'),
            item.get('email'),
            item.get('fax')
        ),
    )

    cursor.execute('SELECT id FROM colleges WHERE name = ? AND IFNULL(state, "") = IFNULL(?, "")', (name, state))
    row = cursor.fetchone()
    return row[0] if row else None


def _extract_state(item: dict) -> str | None:
    loc = item.get('location') or item.get('address') or ''
    parts = [p.strip() for p in str(loc).split(',') if p]
    if len(parts) >= 2:
        return parts[-1]
    return parts[0] if parts else None


def _extract_city(item: dict) -> str | None:
    loc = item.get('location') or item.get('address') or ''
    parts = [p.strip() for p in str(loc).split(',') if p]
    if len(parts) >= 2:
        return parts[-2]
    return None


def import_json_data(conn: sqlite3.Connection, file_path: str, exam_type: str | None = None):
    """Import data from JSON file to database."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, list):
            data = [data]

        cursor = conn.cursor()
        inserted = 0
        ranks_inserted = 0

        for item in data:
            try:
                college_id = _ensure_college(cursor, item)
                if not college_id:
                    continue

                # Insert rich rank/cutoff info if present
                open_rank = item.get('opening_rank')
                close_rank = item.get('closing_rank') or item.get('rank')
                if open_rank or close_rank:
                    try:
                        cursor.execute(
                            '''INSERT INTO college_ranks (college_id, exam_type, year, branch, opening_rank, closing_rank, category, quota, location)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (
                                college_id,
                                exam_type or item.get('exam_type') or _infer_exam_from_filename(file_path),
                                int(item.get('year') or 2024),
                                item.get('branch') or item.get('course'),
                                _safe_int(open_rank),
                                _safe_int(close_rank),
                                item.get('category') or 'General',
                                item.get('quota') or item.get('pool') or 'All India',
                                item.get('location')
                            ),
                        )
                        ranks_inserted += 1
                    except Exception as e:
                        print(f"  Skipped rank row for college_id={college_id}: {e}")

                inserted += 1
            except Exception as e:
                print(f"  Error processing record in {os.path.basename(file_path)}: {e}")

        conn.commit()
        print(f"Imported JSON: {os.path.basename(file_path)} | colleges touched: {inserted}, ranks: {ranks_inserted}")
    except Exception as e:
        print(f"Error processing JSON {file_path}: {e}")


def import_csv_data(conn: sqlite3.Connection, file_path: str, exam_type: str | None = None):
    """Import data from CSV file with flexible headers."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            cursor = conn.cursor()
            inserted = 0
            ranks_inserted = 0

            for row in reader:
                try:
                    # Normalize keys to lower_case
                    item = {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}

                    # Map common variants
                    normalized = {
                        'name': item.get('name') or item.get('college') or item.get('college_name') or item.get('university') or item.get('institute'),
                        'state': item.get('state') or item.get('province'),
                        'website': item.get('website') or item.get('url'),
                        'type': item.get('type') or item.get('institute_type'),
                        'ownership': item.get('ownership') or item.get('type_of_college'),
                        'university': item.get('university') or item.get('affiliation'),
                        'address': item.get('address') or item.get('location'),
                        'city': item.get('city'),
                        'pincode': item.get('pincode') or item.get('pin') or item.get('zip'),
                        'phone': item.get('phone') or item.get('contact') or item.get('mobile'),
                        'email': item.get('email'),
                        'fax': item.get('fax'),
                        'branch': item.get('branch') or item.get('course'),
                        'opening_rank': item.get('opening_rank') or item.get('openingrank'),
                        'closing_rank': item.get('closing_rank') or item.get('closingrank') or item.get('rank'),
                        'category': item.get('category'),
                        'quota': item.get('quota') or item.get('pool'),
                        'year': item.get('year'),
                        'location': item.get('location')
                    }

                    college_id = _ensure_college(cursor, normalized)
                    if not college_id:
                        continue

                    if normalized.get('opening_rank') or normalized.get('closing_rank'):
                        try:
                            cursor.execute(
                                '''INSERT INTO college_ranks (college_id, exam_type, year, branch, opening_rank, closing_rank, category, quota, location)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                (
                                    college_id,
                                    exam_type or _infer_exam_from_filename(file_path),
                                    _safe_int(normalized.get('year')) or 2024,
                                    normalized.get('branch'),
                                    _safe_int(normalized.get('opening_rank')),
                                    _safe_int(normalized.get('closing_rank')),
                                    normalized.get('category') or 'General',
                                    normalized.get('quota') or 'All India',
                                    normalized.get('location')
                                ),
                            )
                            ranks_inserted += 1
                        except Exception as e:
                            print(f"  Skipped CSV rank row for college_id={college_id}: {e}")

                    inserted += 1
                except Exception as e:
                    print(f"  Error processing CSV row in {os.path.basename(file_path)}: {e}")

            conn.commit()
            print(f"Imported CSV: {os.path.basename(file_path)} | colleges touched: {inserted}, ranks: {ranks_inserted}")
    except Exception as e:
        print(f"Error processing CSV {file_path}: {e}")


def _infer_exam_from_filename(path: str) -> str | None:
    lower = os.path.basename(path).lower()
    if 'neet' in lower:
        return 'NEET'
    if 'jee' in lower:
        return 'JEE'
    if 'ielts' in lower:
        return 'IELTS'
    return None


def _safe_int(val):
    try:
        if val is None or val == '':
            return None
        return int(float(str(val).replace(',', '').strip()))
    except Exception:
        return None


def main():
    db_path = 'colleges.db'
    data_dir = 'data'

    print('Creating/connecting to database...')
    conn = create_database(db_path)

    try:
        json_count = 0
        csv_count = 0

        for root, _, files in os.walk(data_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if file.lower().endswith('.json'):
                    print(f"\nProcessing JSON {file}...")
                    import_json_data(conn, file_path, _infer_exam_from_filename(file_path))
                    json_count += 1
                elif file.lower().endswith('.csv'):
                    print(f"\nProcessing CSV {file}...")
                    import_csv_data(conn, file_path, _infer_exam_from_filename(file_path))
                    csv_count += 1

        # Summary
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM colleges')
        total_colleges = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM college_ranks')
        total_ranks = cursor.fetchone()[0]

        print('\n==== Import Summary ====')
        print(f'JSON files processed: {json_count}')
        print(f'CSV files processed:  {csv_count}')
        print(f'Total colleges:       {total_colleges}')
        print(f'Total rank records:   {total_ranks}')
        print('========================')
    finally:
        conn.close()


if __name__ == '__main__':
    main()
