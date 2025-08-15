import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST')
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const apiKey = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY
  if (!apiKey) {
    return res.status(500).json({ error: 'GEMINI_API_KEY (or GOOGLE_API_KEY) not configured on server' })
  }

  try {
    const { messages } = req.body as { messages: Array<{ role: 'user' | 'assistant' | 'system', content: string }> }
    if (!messages || !Array.isArray(messages)) {
      return res.status(400).json({ error: 'Invalid request body. Expected { messages: [...] }' })
    }

    const primaryModel = process.env.GEMINI_MODEL || 'gemini-1.5-pro-latest'
    const fallbackModel = 'gemini-1.5-flash-latest'

    // Build Gemini payload
    const systemMsg = messages.find((m) => m.role === 'system')?.content
    const contents = messages
      .filter((m) => m.role !== 'system')
      .map((m) => ({ role: m.role === 'assistant' ? 'model' : 'user', parts: [{ text: m.content }] }))

    const call = (model: string) =>
      fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          systemInstruction: systemMsg ? { role: 'system', parts: [{ text: systemMsg }] } : undefined,
          contents,
          generationConfig: { temperature: 0.2 },
        }),
      })

    let response = await call(primaryModel)

    if (!response.ok) {
      let details: any
      try { details = await response.json() } catch { details = await response.text() }
      const is429 = response.status === 429 || (details && typeof details === 'object' && details.error?.status === 'RESOURCE_EXHAUSTED')
      if (is429 && primaryModel !== fallbackModel) {
        // retry with fallback model
        response = await call(fallbackModel)
        if (!response.ok) {
          try { details = await response.json() } catch { details = await response.text() }
          return res.status(response.status).json({ error: 'Upstream API error (fallback failed)', details })
        }
      } else {
        return res.status(response.status).json({ error: 'Upstream API error', details })
      }
    }

    const data = await response.json() as any
    const reply = data?.candidates?.[0]?.content?.parts?.map((p: any) => p?.text || '').join('')?.trim() || 'Sorry, I could not generate a response.'
    const usedModel = response.headers.get('x-goog-model') || (response.url.includes(fallbackModel) ? fallbackModel : primaryModel)

    return res.status(200).json({ reply, model: usedModel })
  } catch (e: any) {
    return res.status(500).json({ error: e?.message || 'Unknown server error' })
  }
}
