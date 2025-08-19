import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const base = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'
    const url = `${base}/api/v1/stats`
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
