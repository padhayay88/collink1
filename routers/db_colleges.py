from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
import sqlite3
from pathlib import Path
import csv

DB_PATH = Path(__file__).resolve().parents[1] / 'colleges.db'

router = APIRouter()

def get_conn():
    if not DB_PATH.exists():
        raise HTTPException(status_code=500, detail=f"Database not found at {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

# Approximate total candidates to convert CAT percentile to rank (aligned with scripts/add_cat_cutoffs_from_ims.py)
CAT_TOTAL_CANDIDATES = 300_000

def cat_percentile_to_rank(percentile: float) -> int:
    p = max(0.0, min(100.0, float(percentile)))
    rank = ((100.0 - p) / 100.0) * CAT_TOTAL_CANDIDATES
    return max(1, int(rank))

@router.get('/db/colleges')
async def db_list_colleges(
    q: Optional[str] = Query(None, description='Search by college name (LIKE %q%)'),
    state: Optional[str] = Query(None, description='Filter by state (exact match, case-insensitive)'),
    limit: int = Query(100, ge=0, le=100000),
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
        rows = cur.execute(sql, params + [limit if limit > 0 else 100000, offset]).fetchall()
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

@router.get('/db/engineering/nirf')
async def db_engineering_by_nirf(
    limit: int = Query(200, ge=1, le=5000),
    min_score: Optional[float] = Query(None, description='Optional minimum NIRF score filter'),
):
    """Return Engineering colleges from NIRF 2024 list.

    Data source: data/engineering_nirf_2024.csv with columns: rank,institute,location,state,nirf_score
    Generate using scripts/data_extraction/extract_engineering_nirf_2024.py
    """
    try:
        csv_path = Path(__file__).resolve().parents[1] / 'data' / 'engineering_nirf_2024.csv'
        if not csv_path.exists():
            raise HTTPException(status_code=500, detail=f"Engineering NIRF CSV not found at {csv_path}. Generate it via scripts/data_extraction/extract_engineering_nirf_2024.py")

        rows: list[dict[str, Any]] = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                try:
                    rank_val = int((r.get('rank') or '0').strip().replace(',', ''))
                except Exception:
                    rank_val = 0
                raw_score = (r.get('nirf_score') or '').strip()
                score_val = None
                if raw_score:
                    try:
                        score_val = float(raw_score)
                    except Exception:
                        score_val = None
                if min_score is not None and (score_val is None or score_val < min_score):
                    continue
                rows.append({
                    'name': (r.get('institute') or '').strip(),
                    'location': (r.get('location') or '').strip(),
                    'state': (r.get('state') or '').strip(),
                    'nirf_rank': rank_val,
                    'nirf_score': score_val,
                })

        # Sort best first by nirf_rank ascending, fallback by score desc
        rows.sort(key=lambda x: (x.get('nirf_rank') or 10**9, -(x.get('nirf_score') or -1)))
        rows = rows[:limit]

        return {
            'source': 'nirf_2024_engineering',
            'limit': limit,
            'min_score': min_score,
            'total': len(rows),
            'colleges': rows,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/db/mba/nirf')
async def db_mba_by_nirf_percentile(
    percentile: float = Query(..., ge=0.0, le=100.0, description='Show MBA colleges at or above this NIRF-derived percentile'),
    limit: int = Query(200, ge=1, le=5000),
    min_score: Optional[float] = Query(None, description='Optional minimum NIRF score filter'),
):
    """Return MBA colleges from NIRF 2024 list filtered by percentile.

    Data source: data/mba_nirf_2024.csv with columns: rank,institute,location,nirf_score,percentile
    """
    try:
        csv_path = Path(__file__).resolve().parents[1] / 'data' / 'mba_nirf_2024.csv'
        if not csv_path.exists():
            raise HTTPException(status_code=500, detail=f"NIRF CSV not found at {csv_path}. Generate it via scripts/data_extraction/extract_mba_nirf_2024.py")

        rows: list[dict[str, Any]] = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                try:
                    pct = float(r.get('percentile') or 0.0)
                except Exception:
                    pct = 0.0
                if pct < percentile:
                    continue
                score_val = None
                raw_score = (r.get('nirf_score') or '').strip()
                if raw_score:
                    try:
                        score_val = float(raw_score)
                    except Exception:
                        score_val = None
                if min_score is not None and (score_val is None or score_val < min_score):
                    continue
                try:
                    rank_val = int((r.get('rank') or '0').strip())
                except Exception:
                    rank_val = 0
                rows.append({
                    'name': (r.get('institute') or '').strip(),
                    'location': (r.get('location') or '').strip(),
                    'nirf_rank': rank_val,
                    'nirf_score': score_val,
                    'nirf_percentile': pct
                })

        # Sort best first by nirf_rank (ascending), fallback by score desc
        rows.sort(key=lambda x: (x.get('nirf_rank') or 10**9, -(x.get('nirf_score') or -1)))
        rows = rows[:limit]

        return {
            'exam': 'cat',
            'source': 'nirf_2024',
            'percentile': percentile,
            'limit': limit,
            'min_score': min_score,
            'total': len(rows),
            'colleges': rows,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/db/ba/colleges')
async def db_ba_colleges(
    states: Optional[str] = Query(None, description='Comma-separated list of states to include'),
    ownership: Optional[str] = Query(None, description='government | private'),
    year: Optional[int] = Query(None, description='Optional year for ranks table filtering'),
    limit: int = Query(200, ge=1, le=10000),
    offset: int = Query(0, ge=0)
):
    """List BA colleges.
    Primary source: colleges having any rank rows with branch LIKE '%BA%'.
    Fallback (if none): any colleges with type/name indicating arts.
    """
    try:
        conn = get_conn()
        cur = conn.cursor()

        where = []
        params: list[Any] = []

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

        # Year filter for ranks
        rank_year = ''
        year_params: list[Any] = []
        if year is not None:
            rank_year = ' AND cr.year = ?'
            year_params.append(year)

        where_sql = (' WHERE ' + ' AND '.join(where)) if where else ''

        sql = f'''
            SELECT DISTINCT c.id, c.name, c.state, c.ownership
            FROM colleges c
            JOIN college_ranks cr ON cr.college_id = c.id
            {where_sql}
            AND LOWER(COALESCE(cr.branch, "")) LIKE '%ba%'
            {rank_year}
            ORDER BY c.name
            LIMIT ? OFFSET ?
        '''

        rows = cur.execute(sql, params + year_params + [limit, offset]).fetchall()
        results = [dict(r) for r in rows]

        # Fallback if none from ranks
        if not results:
            fb_where = []
            fb_params: list[Any] = []
            if state_list:
                placeholders = ','.join(['?'] * len(state_list))
                fb_where.append(f'LOWER(COALESCE(state, "")) IN ({placeholders})')
                fb_params.extend(state_list)
            if ownership:
                fb_where.append('LOWER(COALESCE(ownership, "")) = ?')
                fb_params.append(ownership.lower())
            fb_where_sql = (' WHERE ' + ' AND '.join(fb_where)) if fb_where else ''
            # Try type/name includes arts or BA
            fb_like = "(LOWER(COALESCE(type, '')) LIKE '%arts%' OR LOWER(COALESCE(name, '')) LIKE '%arts%' OR LOWER(COALESCE(name, '')) LIKE '%ba %')"
            fb_where_sql = (fb_where_sql + (' AND ' if fb_where_sql else ' WHERE ') + fb_like)
            fb_sql = f'''SELECT id, name, state, ownership FROM colleges{fb_where_sql} ORDER BY name LIMIT ? OFFSET ?'''
            rows = cur.execute(fb_sql, fb_params + [limit, offset]).fetchall()
            results = [dict(r) for r in rows]

        conn.close()
        return {
            'track': 'ba',
            'total': len(results),
            'colleges': results,
            'limit': limit,
            'offset': offset,
            'states': state_list,
            'ownership': ownership,
            'year': year
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/db/mba/by-cat-percentile')
async def db_mba_by_cat_percentile(
    percentile: float = Query(..., ge=0.0, le=100.0, description='Your CAT percentile (0-100)'),
    year: Optional[int] = Query(None, description='Filter by year for ranks'),
    states: Optional[str] = Query(None, description='Comma-separated list of states to include'),
    ownership: Optional[str] = Query(None, description='government | private'),
    include_no_rank: bool = Query(False, description='Also return colleges without rank data to fill results'),
    tolerance_percent: float = Query(0.0, ge=0.0, le=100.0, description='± tolerance in percent for matching after converting percentile to rank'),
    limit: int = Query(200, ge=1, le=10000),
    offset: int = Query(0, ge=0)
):
    """Return MBA colleges for CAT exam based on CAT percentile.
    Internally converts percentile to an approximate equivalent rank and reuses the rank-window matching logic.
    Filters to CAT exam and tries to restrict to MBA-related branches (branch LIKE '%MBA%').
    """
    try:
        # Convert percentile to a target rank and matching window
        base_rank = cat_percentile_to_rank(percentile)
        tol = tolerance_percent / 100.0
        low = int(base_rank * (1 - tol))
        hi = int(base_rank * (1 + tol))

        conn = get_conn()
        cur = conn.cursor()

        where: list[str] = []
        params: list[Any] = []

        # Exam filter to CAT
        where.append('LOWER(COALESCE(cr.exam_type, "")) LIKE ?')
        params.append('%cat%')

        # Year filter
        if year is not None:
            where.append('cr.year = ?')
            params.append(year)

        # MBA branch filter (match common variants)
        where.append('LOWER(COALESCE(cr.branch, "")) LIKE ?')
        params.append('%mba%')

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

        # Rank matching: if min_rank/max_rank provided, use range filters
        # Centered rank window based on approx rank from percentile
        where.append('( (cr.closing_rank BETWEEN ? AND ?) OR (cr.opening_rank BETWEEN ? AND ?) OR (cr.opening_rank <= ? AND cr.closing_rank >= ?) )')
        params.extend([low, hi, low, hi, hi, low])

        where_sql = ' WHERE ' + ' AND '.join(where)

        base_sql = f'''
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
            LIMIT ? OFFSET ?
        '''

        rows = cur.execute(base_sql, params + [limit, offset]).fetchall()
        results = [dict(r) for r in rows]

        included_ids = {r['id'] for r in rows}

        # Fill with colleges that have no CAT-MBA rank rows if requested
        if include_no_rank and len(results) < limit:
            remaining = limit - len(results)
            no_rank_where = []
            no_rank_params: list[Any] = []

            if state_list:
                placeholders = ','.join(['?'] * len(state_list))
                no_rank_where.append(f'LOWER(COALESCE(c.state, "")) IN ({placeholders})')
                no_rank_params.extend(state_list)
            if ownership:
                no_rank_where.append('LOWER(COALESCE(c.ownership, "")) = ?')
                no_rank_params.append(ownership.lower())
            if included_ids:
                placeholders = ','.join(['?'] * len(included_ids))
                no_rank_where.append(f'c.id NOT IN ({placeholders})')
                no_rank_params.extend(list(included_ids))

            # Require NOT EXISTS a CAT rank row (optionally for the given year)
            exists_filters = ['LOWER(COALESCE(cr.exam_type, "")) LIKE ?']
            exists_params: list[Any] = ['%cat%']
            if year is not None:
                exists_filters.append('cr.year = ?')
                exists_params.append(year)
            exists_sql = ' AND '.join(exists_filters)

            no_rank_where_sql = ('WHERE ' + ' AND '.join(no_rank_where)) if no_rank_where else ''
            no_rank_sql = f'''
                SELECT c.id, c.name, c.state, c.ownership
                FROM colleges c
                {no_rank_where_sql}
                AND NOT EXISTS (
                    SELECT 1 FROM college_ranks cr
                    WHERE cr.college_id = c.id AND {exists_sql}
                )
                ORDER BY c.name
                LIMIT ?
            ''' if no_rank_where else f'''
                SELECT c.id, c.name, c.state, c.ownership
                FROM colleges c
                WHERE NOT EXISTS (
                    SELECT 1 FROM college_ranks cr
                    WHERE cr.college_id = c.id AND {exists_sql}
                )
                ORDER BY c.name
                LIMIT ?
            '''

            fill_rows = cur.execute(no_rank_sql, no_rank_params + exists_params + [remaining]).fetchall()
            for r in fill_rows:
                d = dict(r)
                d.update({
                    'exam_type': 'cat',
                    'year': year,
                    'branch': 'MBA',
                    'opening_rank': None,
                    'closing_rank': None,
                    'category': None,
                    'quota': None,
                    'location': None,
                    'has_rank': False
                })
                results.append(d)

        conn.close()
        return {
            'exam': 'cat',
            'percentile': percentile,
            'approx_rank': base_rank,
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
    include_no_rank: bool = Query(False, description='Also return colleges without rank data to fill results'),
    tolerance_percent: float = Query(0.0, ge=0.0, le=100.0, description='± tolerance in percent for matching'),
    min_rank: Optional[int] = Query(None, ge=1, description='Return rows with cutoff >= min_rank'),
    max_rank: Optional[int] = Query(None, ge=1, description='Return rows with cutoff <= max_rank'),
    limit: int = Query(500, ge=1, le=100000),
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
            if tokens:
                # Match if ANY token is present to be inclusive across data variants
                or_clauses = []
                for t in tokens:
                    or_clauses.append('LOWER(COALESCE(cr.exam_type, "")) LIKE ?')
                    params.append(f'%{t}%')
                where.append('( ' + ' OR '.join(or_clauses) + ' )')

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

        # Rank matching: if min_rank/max_rank provided, use range filters; else use centered window
        if min_rank is not None or max_rank is not None:
            # Consider a row matching if either opening_rank or closing_rank satisfies the bounds
            # Use COALESCE to handle NULLs (treat as very large number)
            if min_rank is not None and max_rank is not None:
                # Include rows where either bound falls in range OR the range overlaps [min,max]
                where.append('(' 
                             ' (COALESCE(cr.closing_rank, 2147483647) BETWEEN ? AND ?)' 
                             ' OR (COALESCE(cr.opening_rank, 2147483647) BETWEEN ? AND ?)' 
                             ' OR (COALESCE(cr.opening_rank, 2147483647) <= ? AND COALESCE(cr.closing_rank, 2147483647) >= ?)' 
                             ')')
                params.extend([min_rank, max_rank, min_rank, max_rank, max_rank, min_rank])
            elif min_rank is not None:
                where.append('( COALESCE(cr.closing_rank, 2147483647) >= ? OR COALESCE(cr.opening_rank, 2147483647) >= ? )')
                params.extend([min_rank, min_rank])
            elif max_rank is not None:
                where.append('( COALESCE(cr.closing_rank, 2147483647) <= ? OR COALESCE(cr.opening_rank, 2147483647) <= ? )')
                params.extend([max_rank, max_rank])
        else:
            # Centered rank window
            where.append('( (cr.closing_rank BETWEEN ? AND ?) OR (cr.opening_rank BETWEEN ? AND ?) OR (cr.opening_rank <= ? AND cr.closing_rank >= ?) )')
            params.extend([low, hi, low, hi, hi, low])

        where_sql = ' WHERE ' + ' AND '.join(where)

        def build_sql(with_offset: bool = True):
            # Select distinct colleges by grouping rank rows, computing a deterministic best match per college.
            # This avoids returning multiple rows per college for different branches/categories which can lead to
            # client-side de-dup showing fewer items and inconsistent counts.
            return f'''
            SELECT 
                g.id,
                g.name,
                g.state,
                g.ownership,
                g.exam_type,
                g.year,
                g.branch,
                g.opening_rank,
                g.closing_rank,
                g.category,
                g.quota,
                g.location
            FROM (
                SELECT 
                    c.id AS id,
                    c.name AS name,
                    c.state AS state,
                    c.ownership AS ownership,
                    -- Choose the best matching row per college by minimum of COALESCE(closing, opening)
                    MIN(COALESCE(cr.closing_rank, cr.opening_rank)) AS match_rank,
                    -- Also surface some representative fields using MIN/MAX on textual cols to keep SQLite happy
                    MIN(COALESCE(cr.opening_rank, cr.closing_rank)) AS opening_rank,
                    MIN(COALESCE(cr.closing_rank, cr.opening_rank)) AS closing_rank,
                    MIN(COALESCE(cr.exam_type, '')) AS exam_type,
                    MAX(COALESCE(cr.year, 0)) AS year,
                    MIN(COALESCE(cr.branch, '')) AS branch,
                    MIN(COALESCE(cr.category, '')) AS category,
                    MIN(COALESCE(cr.quota, '')) AS quota,
                    MIN(COALESCE(cr.location, '')) AS location
                FROM college_ranks cr
                JOIN colleges c ON c.id = cr.college_id
                {where_sql}
                GROUP BY c.id, c.name, c.state, c.ownership
            ) AS g
            ORDER BY (g.match_rank IS NULL) ASC, g.match_rank ASC, g.name ASC
            LIMIT ? {('OFFSET ?' if with_offset else '')}
        '''

        sql = build_sql(True)
        rows = cur.execute(sql, params + [limit, offset]).fetchall()

        # Strict behavior: do not auto-widen tolerance; return exact matches only per provided filters

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

        # Removed final fallback that filled with any colleges to avoid identical results across ranks

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
