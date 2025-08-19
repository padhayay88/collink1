import type { NextApiRequest, NextApiResponse } from 'next'
import fs from 'fs'
import path from 'path'

function loadColleges() {
  const candidates = [
    path.resolve(process.cwd(), '..', 'comprehensive_college_database.json'),
    path.resolve(process.cwd(), 'comprehensive_college_database.json'),
    path.resolve(process.cwd(), 'public', 'comprehensive_college_database.json'),
  ]
  for (const p of candidates) {
    try {
      if (!fs.existsSync(p)) continue
      const raw = fs.readFileSync(p, 'utf-8')
      const data = JSON.parse(raw)
      const list = Array.isArray(data?.colleges) ? data.colleges : (Array.isArray(data) ? data : [])
      if (Array.isArray(list) && list.length) return list
    } catch {}
  }
  return []
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const colleges = loadColleges()
  // Group by rough rank buckets if present; else put under 'Unranked'
  const by_rank: Record<string, any[]> = {}
  for (const c of colleges) {
    const r = Number(c.rank || c.nirf_rank || c.closing_rank || c.opening_rank)
    let bucket = 'Unranked'
    if (!Number.isNaN(r) && r > 0) {
      if (r <= 100) bucket = '1-100'
      else if (r <= 500) bucket = '101-500'
      else if (r <= 1000) bucket = '501-1000'
      else if (r <= 5000) bucket = '1001-5000'
      else bucket = '5001+'
    }
    ;(by_rank[bucket] ||= []).push(c)
  }
  res.status(200).json(by_rank)
}

