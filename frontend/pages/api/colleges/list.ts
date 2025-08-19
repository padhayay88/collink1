import type { NextApiRequest, NextApiResponse } from 'next'

// Proxy to backend DB list colleges endpoint to avoid CORS and keep stable frontend path
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const params = new URLSearchParams()
    for (const [k, v] of Object.entries(req.query)) {
      if (Array.isArray(v)) {
        for (const vv of v) params.append(k, String(vv))
      } else if (v !== undefined) {
        params.set(k, String(v))
      }
    }

    const backendBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const url = `${backendBase}/api/v1/db/colleges?${params.toString()}`
    const r = await fetch(url)
    const text = await r.text()
    if (!r.ok) return res.status(r.status).send(text)
    try {
      const data = JSON.parse(text)
      return res.status(200).json(data)
    } catch {
      return res.status(200).send(text)
    }
  } catch (e: any) {
    return res.status(500).json({ error: e?.message || 'proxy_failed' })
  }
}
