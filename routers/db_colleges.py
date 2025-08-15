from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / 'colleges.db'

router = APIRouter()

def get_conn():
    if not DB_PATH.exists():
        raise HTTPException(status_code=500, detail=f"Database not found at {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

@router.get('/db/colleges')
async def db_list_colleges(
    q: Optional[str] = Query(None, description='Search by college name (LIKE %q%)'),
    state: Optional[str] = Query(None, description='Filter by state (exact match, case-insensitive)'),
    limit: int = Query(100, ge=0, le=10000),
    offset: int = Query(0, ge=0),
):
    try:
        conn = get_conn()
        cur = conn.cursor()
        where = []
        params: list[Any] = []
        if q:
            where.append('LOWER(name) LIKE ?')
            params.append(f"%{q.lower()}%")
        if state:
            where.append('LOWER(COALESCE(state, "")) = ?')
            params.append(state.lower())
        where_sql = (" WHERE " + " AND ".join(where)) if where else ""

        total = cur.execute(f"SELECT COUNT(*) AS c FROM colleges{where_sql}", params).fetchone()[0]
        sql = f"SELECT id, name, state, type, website, ownership, university, address, city FROM colleges{where_sql} ORDER BY name LIMIT ? OFFSET ?"
        rows = cur.execute(sql, params + [limit if limit > 0 else 10000, offset]).fetchall()
        conn.close()
        return {
            'total': total,
            'count': len(rows),
            'limit': limit,
            'offset': offset,
            'colleges': [dict(r) for r in rows]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/db/colleges/at-rank')
async def db_colleges_at_rank(
    rank: int = Query(..., ge=1, description='Your rank'),
    exam: Optional[str] = Query('jee', description='Exam type, e.g., jee, neet, ielts'),
    category: Optional[str] = Query(None, description='Category filter, e.g., General, OBC, SC, ST'),
    gender: Optional[str] = Query(None, description='Gender filter if present in data'),
    quota: Optional[str] = Query(None, description='Quota filter if present in data'),
    year: Optional[int] = Query(None, description='Filter by year'),
    states: Optional[str] = Query(None, description='Comma-separated list of states to include'),
    ownership: Optional[str] = Query(None, description='government | private'),
    include_no_rank: bool = Query(True, description='Also return colleges without rank data to fill results'),
    tolerance_percent: float = Query(0.0, ge=0.0, le=100.0, description='± tolerance in percent for matching'),
    limit: int = Query(500, ge=1, le=10000),
    offset: int = Query(0, ge=0, description='Offset for pagination')
):
    """Return colleges whose cutoffs match a given rank with optional tolerance and filters.
    Matching logic (per row):
      - let low = rank * (1 - tol), hi = rank * (1 + tol)
      - consider a match if closing_rank between [low, hi] OR
        opening_rank between [low, hi] OR
        (opening_rank <= hi AND closing_rank >= low)
    """
    try:
        conn = get_conn()
        cur = conn.cursor()
        tol = tolerance_percent / 100.0
        low = int(rank * (1 - tol))
        hi = int(rank * (1 + tol))

        where = []
        params: list[Any] = []
        if exam:
            # Tokenized LIKE matching to handle variants like "jee main", "jee advanced"
            tokens = [t for t in exam.lower().split() if t]
            for t in tokens:
                where.append('LOWER(COALESCE(cr.exam_type, "")) LIKE ?')
                params.append(f'%{t}%')

        # Year filter
        if year is not None:
            where.append('cr.year = ?')
            params.append(year)

        # Category filter
        if category:
            where.append('LOWER(COALESCE(cr.category, "")) = ?')
            params.append(category.lower())

        # Gender filter (if present in data schema)
        if gender:
            where.append('LOWER(COALESCE(cr.gender, "")) = ?')
            params.append(gender.lower())

        # Quota filter
        if quota:
            where.append('LOWER(COALESCE(cr.quota, "")) = ?')
            params.append(quota.lower())

        # States filter
        state_list: list[str] = []
        if states:
            state_list = [s.strip().lower() for s in states.split(',') if s.strip()]
            if state_list:
                placeholders = ','.join(['?'] * len(state_list))
                where.append(f'LOWER(COALESCE(c.state, "")) IN ({placeholders})')
                params.extend(state_list)

        # Ownership filter
        if ownership:
            where.append('LOWER(COALESCE(c.ownership, "")) = ?')
            params.append(ownership.lower())

        # Rank matching window
        where.append('( (cr.closing_rank BETWEEN ? AND ?) OR (cr.opening_rank BETWEEN ? AND ?) OR (cr.opening_rank <= ? AND cr.closing_rank >= ?) )')
        params.extend([low, hi, low, hi, hi, low])

        where_sql = ' WHERE ' + ' AND '.join(where)

        def build_sql(with_offset: bool = True):
            return f'''
            SELECT c.id,
                   c.name,
                   c.state,
                   c.ownership,
                   cr.exam_type,
                   cr.year,
                   cr.branch,
                   cr.opening_rank,
                   cr.closing_rank,
                   cr.category,
                   cr.quota,
                   cr.location
            FROM college_ranks cr
            JOIN colleges c ON c.id = cr.college_id
            {where_sql}
            ORDER BY COALESCE(cr.closing_rank, cr.opening_rank) ASC, c.name ASC
            LIMIT ? {('OFFSET ?' if with_offset else '')}
        '''

        sql = build_sql(True)
        rows = cur.execute(sql, params + [limit, offset]).fetchall()

        # If no rows and tolerance is 0, auto-widen tolerance to 20% and retry once
        if len(rows) == 0 and tolerance_percent == 0.0:
            tol = 0.20
            low_retry = int(rank * (1 - tol))
            hi_retry = int(rank * (1 + tol))
            # replace rank window params at the end of params list: [low, hi, low, hi, hi, low]
            params_retry = params[:-6] + [low_retry, hi_retry, low_retry, hi_retry, hi_retry, low_retry]
            rows = cur.execute(build_sql(True), params_retry + [limit, offset]).fetchall()

        results = [dict(r) for r in rows]
        included_ids = {r['id'] for r in rows}

        # If we need to fill with colleges that have no rank data per filters
        if include_no_rank and len(results) < limit:
            remaining = limit - len(results)

            # Build WHERE for colleges without matching rank rows
            no_rank_where = []
            no_rank_params: list[Any] = []

            if state_list:
                placeholders = ','.join(['?'] * len(state_list))
                no_rank_where.append(f'LOWER(COALESCE(c.state, "")) IN ({placeholders})')
                no_rank_params.extend(state_list)

            if ownership:
                no_rank_where.append('LOWER(COALESCE(c.ownership, "")) = ?')
                no_rank_params.append(ownership.lower())

            # Exclude already included ids
            if included_ids:
                placeholders = ','.join(['?'] * len(included_ids))
                no_rank_where.append(f'c.id NOT IN ({placeholders})')
                no_rank_params.extend(list(included_ids))

            # NOT EXISTS rank row for given exam/year (if provided)
            exists_filters = []
            exists_params: list[Any] = []
            if exam:
                exists_filters.append('LOWER(COALESCE(cr.exam_type, "")) = ?')
                exists_params.append(exam.lower())
            if year is not None:
                exists_filters.append('cr.year = ?')
                exists_params.append(year)
            exists_sql = (' AND ' + ' AND '.join(exists_filters)) if exists_filters else ''

            no_rank_where_sql = ('WHERE ' + ' AND '.join(no_rank_where)) if no_rank_where else ''
            no_rank_sql = f'''
                SELECT c.id, c.name, c.state, c.ownership
                FROM colleges c
                {no_rank_where_sql}
                AND NOT EXISTS (
                    SELECT 1 FROM college_ranks cr
                    WHERE cr.college_id = c.id{exists_sql}
                )
                ORDER BY c.name
                LIMIT ?
            ''' if no_rank_where else f'''
                SELECT c.id, c.name, c.state, c.ownership
                FROM colleges c
                WHERE NOT EXISTS (
                    SELECT 1 FROM college_ranks cr
                    WHERE cr.college_id = c.id{exists_sql}
                )
                ORDER BY c.name
                LIMIT ?
            '''

            fill_rows = cur.execute(no_rank_sql, no_rank_params + exists_params + [remaining]).fetchall()
            for r in fill_rows:
                d = dict(r)
                d.update({
                    'exam_type': exam,
                    'year': year,
                    'branch': None,
                    'opening_rank': None,
                    'closing_rank': None,
                    'category': category,
                    'quota': quota,
                    'location': None,
                    'has_rank': False
                })
                results.append(d)

        # Final fallback: fill with any colleges (regardless of having rank rows) to always reach limit
        if len(results) < limit:
            remaining = limit - len(results)
            any_where = []
            any_params: list[Any] = []
            if state_list:
                placeholders = ','.join(['?'] * len(state_list))
                any_where.append(f'LOWER(COALESCE(c.state, "")) IN ({placeholders})')
                any_params.extend(state_list)
            if ownership:
                any_where.append('LOWER(COALESCE(c.ownership, "")) = ?')
                any_params.append(ownership.lower())
            if included_ids:
                placeholders = ','.join(['?'] * len(included_ids))
                any_where.append(f'c.id NOT IN ({placeholders})')
                any_params.extend(list(included_ids))
            any_where_sql = ('WHERE ' + ' AND '.join(any_where)) if any_where else ''
            # Order by best available cutoff (lower is better), then by name
            any_sql_base = f'''
                SELECT c.id, c.name, c.state, c.ownership,
                       MIN(COALESCE(cr.closing_rank, cr.opening_rank)) AS best_cutoff
                FROM colleges c
                LEFT JOIN college_ranks cr ON cr.college_id = c.id
                {any_where_sql}
                GROUP BY c.id, c.name, c.state, c.ownership
                ORDER BY (best_cutoff IS NULL) ASC, best_cutoff ASC, c.name ASC
                LIMIT ? OFFSET ?
            '''

            any_offset = 0
            safety = 0
            while remaining > 0 and safety < 20:
                batch = cur.execute(any_sql_base, any_params + [remaining, any_offset]).fetchall()
                if not batch:
                    break
                for r in batch:
                    d = dict(r)
                    d.update({
                        'exam_type': exam,
                        'year': year,
                        'branch': None,
                        'opening_rank': None,
                        'closing_rank': None,
                        'category': category,
                        'quota': quota,
                        'location': None,
                        'has_rank': False
                    })
                    results.append(d)
                remaining = limit - len(results)
                any_offset += len(batch)
                safety += 1

        conn.close()
        return {
            'exam': exam,
            'rank': rank,
            'category': category,
            'tolerance_percent': tolerance_percent,
            'year': year,
            'states': state_list,
            'ownership': ownership,
            'include_no_rank': include_no_rank,
            'total': len(results),
            'colleges': results,
            'offset': offset
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/db/top')
async def db_top_colleges(
    exam: Optional[str] = Query(None, description='Filter by exam type: JEE | NEET | IELTS'),
    year: Optional[int] = Query(None, description='Filter by year for ranks'),
    limit: int = Query(100, ge=1, le=1000)
):
    """Return colleges ordered by best (lowest) available cutoff rank.
    If exam is provided, only consider ranks for that exam. If year is provided, only that year.
    """
    try:
        conn = get_conn()
        cur = conn.cursor()
        where = []
        params: list[Any] = []
        if exam:
            where.append('LOWER(COALESCE(cr.exam_type, "")) = ?')
            params.append(exam.lower())
        if year:
            where.append('cr.year = ?')
            params.append(year)
        where_sql = ('WHERE ' + ' AND '.join(where)) if where else ''

        sql = f'''
            SELECT c.id,
                   c.name,
                   c.state,
                   MIN(COALESCE(cr.closing_rank, cr.opening_rank)) AS best_rank,
                   MAX(cr.year) AS latest_year
            FROM college_ranks cr
            JOIN colleges c ON c.id = cr.college_id
            {where_sql}
            GROUP BY c.id, c.name, c.state
            ORDER BY (best_rank IS NULL) ASC, best_rank ASC
            LIMIT ?
        '''
        rows = cur.execute(sql, params + [limit]).fetchall()
        conn.close()
        return {
            'filters': {'exam': exam, 'year': year},
            'total': len(rows),
            'colleges': [
                {
                    'name': r['name'],
                    'state': r['state'],
                    'best_rank': r['best_rank'],
                    'latest_year': r['latest_year']
                } for r in rows
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/db/college/{name}')
async def db_get_college(name: str):
    try:
        conn = get_conn()
        cur = conn.cursor()
        row = cur.execute(
            'SELECT id, name, state, type, website, ownership, university, address, city FROM colleges WHERE LOWER(name) = ? LIMIT 1',
            (name.lower(),)
        ).fetchone()
        if not row:
            # fallback partial match
            row = cur.execute(
                'SELECT id, name, state, type, website, ownership, university, address, city FROM colleges WHERE LOWER(name) LIKE ? ORDER BY LENGTH(name) LIMIT 1',
                (f"%{name.lower()}%",)
            ).fetchone()
        if not row:
            conn.close()
            raise HTTPException(status_code=404, detail=f"College '{name}' not found")
        college = dict(row)
        # attach limited ranks summary
        rank_rows = cur.execute(
            'SELECT exam_type, year, branch, opening_rank, closing_rank, category, quota, location FROM college_ranks WHERE college_id = ? ORDER BY year DESC LIMIT 200',
            (college['id'],)
        ).fetchall()
        college['ranks'] = [dict(r) for r in rank_rows]
        conn.close()
        return college
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/db/colleges/by-state')
async def db_colleges_by_state(
    state: str = Query(..., description='State to filter by (case-insensitive exact match)'),
    limit: int = Query(500, ge=0, le=10000)
):
    try:
        conn = get_conn()
        cur = conn.cursor()
        rows = cur.execute(
            'SELECT id, name, state, type, website, ownership, university, address, city FROM colleges WHERE LOWER(COALESCE(state, "")) = ? ORDER BY name LIMIT ?',
            (state.lower(), limit if limit > 0 else 10000)
        ).fetchall()
        conn.close()
        return {
            'state': state,
            'total': len(rows),
            'colleges': [dict(r) for r in rows]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/db/college/{name}/ranks')
async def db_college_ranks(
    name: str,
    exam: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    limit: int = Query(1000, ge=0, le=20000)
):
    try:
        conn = get_conn()
        cur = conn.cursor()
        c_row = cur.execute('SELECT id FROM colleges WHERE LOWER(name) = ? LIMIT 1', (name.lower(),)).fetchone()
        if not c_row:
            c_row = cur.execute('SELECT id FROM colleges WHERE LOWER(name) LIKE ? ORDER BY LENGTH(name) LIMIT 1', (f"%{name.lower()}%",)).fetchone()
        if not c_row:
            conn.close()
            raise HTTPException(status_code=404, detail=f"College '{name}' not found")
        college_id = c_row[0]
        where = ['college_id = ?']
        params: list[Any] = [college_id]
        if exam:
            where.append('LOWER(COALESCE(exam_type, "")) = ?')
            params.append(exam.lower())
        if year:
            where.append('year = ?')
            params.append(year)
        where_sql = ' WHERE ' + ' AND '.join(where)
        rows = cur.execute(
            f'SELECT exam_type, year, branch, opening_rank, closing_rank, category, quota, location FROM college_ranks{where_sql} ORDER BY year DESC, exam_type LIMIT ?',
            params + [limit if limit > 0 else 20000]
        ).fetchall()
        conn.close()
        return {
            'college': name,
            'total': len(rows),
            'ranks': [dict(r) for r in rows]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
