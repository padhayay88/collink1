import type { NextApiRequest, NextApiResponse } from 'next'

export const config = {
  api: {
    bodyParser: true,
  },
}

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

    const systemMsg = messages.find((m) => m.role === 'system')?.content
    const contents = messages
      .filter((m) => m.role !== 'system')
      .map((m) => ({ role: m.role === 'assistant' ? 'model' : 'user', parts: [{ text: m.content }] }))

    // Prepare SSE headers
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache, no-transform',
      Connection: 'keep-alive',
      'Access-Control-Allow-Origin': '*',
    })

    const call = (model: string) =>
      fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:streamGenerateContent?key=${apiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          systemInstruction: systemMsg ? { role: 'system', parts: [{ text: systemMsg }] } : undefined,
          contents,
          generationConfig: { temperature: 0.2 },
        }),
      })

    let response = await call(primaryModel)

    if (!response.ok || !response.body) {
      let details: any
      try { details = await response.json() } catch { details = await response.text() }
      const is429 = response.status === 429 || (details && typeof details === 'object' && details.error?.status === 'RESOURCE_EXHAUSTED')
      if (is429 && primaryModel !== fallbackModel) {
        response = await call(fallbackModel)
      }
      if (!response.ok || !response.body) {
        const errTxt = typeof details === 'string' ? details : JSON.stringify(details)
        res.write(`data: ${JSON.stringify({ error: 'Gemini API error', details: errTxt })}\n\n`)
        res.write('data: [DONE]\n\n')
        return res.end()
      }
    }

    const reader = (response as any).body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      const chunk = decoder.decode(value)
      const lines = chunk.split('\n').map((l) => l.trim()).filter(Boolean)
      for (const line of lines) {
        // Ensure SSE formatting with data: prefix
        if (line.startsWith('data:')) {
          res.write(line + '\n')
        } else {
          res.write(`data: ${line}\n`)
        }
      }
    }

    res.write('data: [DONE]\n\n')
    res.end()
  } catch (e: any) {
    res.write(`data: ${JSON.stringify({ error: e?.message || 'Unknown server error' })}\n\n`)
    res.write('data: [DONE]\n\n')
    res.end()
  }
}
