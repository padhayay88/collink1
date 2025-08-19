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
  const by_state: Record<string, any[]> = {}
  for (const c of colleges) {
    const state = String(c.state || 'Unknown')
    ;(by_state[state] ||= []).push(c)
  }
  res.status(200).json(by_state)
}
