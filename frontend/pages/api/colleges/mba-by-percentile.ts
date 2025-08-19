import type { NextApiRequest, NextApiResponse } from 'next'

// Proxy to backend MBA by CAT percentile endpoint
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
    const url = `${backendBase}/api/v1/db/mba/by-cat-percentile?${params.toString()}`
    console.log('[api/colleges/mba-by-percentile] Proxy ->', url)
    const r = await fetch(url, { cache: 'no-store' })
    const text = await r.text()
    if (!r.ok) {
      res.setHeader('Cache-Control', 'no-store, no-cache, max-age=0, must-revalidate')
      return res.status(r.status).send(text)
    }
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
