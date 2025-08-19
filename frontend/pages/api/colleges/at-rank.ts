import type { NextApiRequest, NextApiResponse } from 'next'

// This route proxies to the backend SQL-powered endpoint for at-rank queries.
// It avoids CORS issues and keeps the frontend URL stable at /api/colleges/at-rank.
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

    const backendUrl = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/db/colleges/at-rank?${params.toString()}`
    // Debug log
    console.log('[api/colleges/at-rank] Proxy ->', backendUrl)
    const r = await fetch(backendUrl, { cache: 'no-store' })
    const text = await r.text()
    if (!r.ok) {
      res.setHeader('Cache-Control', 'no-store, no-cache, max-age=0, must-revalidate')
      return res.status(r.status).send(text)
    }
    // Try JSON parse, fallback to text
    try {
      const data = JSON.parse(text)
      res.setHeader('Cache-Control', 'no-store, no-cache, max-age=0, must-revalidate')
      return res.status(200).json(data)
    } catch {
      res.setHeader('Cache-Control', 'no-store, no-cache, max-age=0, must-revalidate')
      return res.status(200).send(text)
    }
  } catch (e: any) {
    res.setHeader('Cache-Control', 'no-store, no-cache, max-age=0, must-revalidate')
    return res.status(500).json({ error: e?.message || 'proxy_failed' })
  }
}
