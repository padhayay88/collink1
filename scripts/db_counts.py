import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parents[1] / 'colleges.db'
if not db_path.exists():
    print('DB not found at', db_path)
    raise SystemExit(1)

conn = sqlite3.connect(str(db_path))
cur = conn.cursor()

def one(q):
    cur.execute(q)
    return cur.fetchone()[0]

print('DB:', db_path)
print('colleges:', one('SELECT COUNT(*) FROM colleges'))
print('college_ranks:', one('SELECT COUNT(*) FROM college_ranks'))
print('distinct_states:', one('SELECT COUNT(DISTINCT COALESCE(state, "")) FROM colleges'))
conn.close()
