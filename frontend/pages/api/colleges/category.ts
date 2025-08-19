import type { NextApiRequest, NextApiResponse } from 'next'
import fs from 'fs'
import path from 'path'

function loadColleges() {
  // Try multiple potential locations so this works in dev and prod builds
  const candidates = [
    path.resolve(process.cwd(), '..', 'comprehensive_college_database.json'), // repo root (when cwd=frontend)
    path.resolve(process.cwd(), 'comprehensive_college_database.json'),       // same dir (if copied inside frontend)
    path.resolve(process.cwd(), 'public', 'comprehensive_college_database.json'), // served via public/
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
  const by_category: Record<string, any[]> = {}
  for (const c of colleges) {
    const category = String(c.category || c.type || 'Uncategorized')
    ;(by_category[category] ||= []).push(c)
  }
  res.status(200).json(by_category)
}
