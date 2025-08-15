import React, { useEffect, useState } from 'react'
import Head from 'next/head'
import Header from '../components/Header'
import { api } from '../lib/api'

export default function AIChatPage() {
  const [input, setInput] = useState('Suggest government engineering colleges in Gujarat for CS')
  const [history, setHistory] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([])
  const [loading, setLoading] = useState(false)
  const [states, setStates] = useState<string[]>([])

  useEffect(() => {
    (async () => {
      try {
        const s = await api.getSupportedStates('jee')
        setStates(s)
      } catch {}
    })()
  }, [])

  const simpleFallback = async (q: string): Promise<string> => {
    // Very simple heuristic: detect state and ownership, fetch from by-state endpoint
    const lower = q.toLowerCase()
    const ownership = lower.includes('government') ? 'government' : (lower.includes('private') ? 'private' : undefined)

    // Static canonical state map to handle misspellings and synonyms
    const canonicalMap: Record<string, string[]> = {
      'andhra pradesh': ['andhrapradesh', 'ap'],
      'arunachal pradesh': ['arunachalpradesh'],
      'assam': [],
      'bihar': [],
      'chhattisgarh': ['chattisgarh', 'chattisgar'],
      'goa': [],
      'gujarat': ['gj'],
      'haryana': [],
      'himachal pradesh': ['himachalpradesh', 'hp'],
      'jharkhand': [],
      'karnataka': [],
      'kerala': [],
      'madhya pradesh': ['madhyapradesh', 'mp'],
      'maharashtra': ['mh'],
      'manipur': [],
      'meghalaya': [],
      'mizoram': [],
      'nagaland': [],
      'odisha': ['orissa'],
      'punjab': [],
      'rajasthan': [],
      'sikkim': [],
      'tamil nadu': ['tamilnadu', 'tn'],
      'telangana': ['tg', 'telengana'],
      'tripura': [],
      'uttar pradesh': ['uttarpradesh', 'up', 'uttarpardesh', 'uttarpadesh'],
      'uttarakhand': ['uk', 'uttarnkhand', 'uttaranchal'],
      'west bengal': ['westbengal', 'wb'],
      'delhi': ['new delhi', 'ncr'],
      'jammu and kashmir': ['jammu&kashmir', 'j&k', 'jammu and kashmir'],
      'ladakh': []
    }

    const normalize = (s: string) => s.toLowerCase().replace(/[^a-z]/g, '')

    const allStates = new Set<string>([
      ...states,
      ...Object.keys(canonicalMap).map(s => s.replace(/\b\s+\b/g, ' ')),
    ])

    let foundState: string | undefined
    const normalizedQuery = normalize(lower)
    // First try loaded states direct match
    for (const s of Array.from(allStates)) {
      if (lower.includes(s.toLowerCase())) { foundState = s; break }
      if (normalize(s) && normalizedQuery.includes(normalize(s))) { foundState = s; break }
    }
    // Try synonyms map
    if (!foundState) {
      for (const [canon, syns] of Object.entries(canonicalMap)) {
        if (lower.includes(canon)) { foundState = canon; break }
        for (const syn of syns) {
          if (normalizedQuery.includes(normalize(syn))) { foundState = canon; break }
        }
        if (foundState) break
      }
    }

    if (!foundState) return 'Please mention a state (e.g., Gujarat, Maharashtra).'

    try {
      const res = await api.getCollegesByState({ state: foundState, ownership: ownership as any, limit: 50 })
      const wantsCS = /(\bcs\b|computer\s*science|cse)/i.test(q)
      const list = res.colleges.filter(c => !wantsCS || (c.branch || '').toLowerCase().includes('computer'))
      if (list.length === 0) {
        return `No ${ownership || ''} colleges found for your filter in ${foundState}. Try removing branch filter or changing ownership.`.trim()
      }
      const items = list.slice(0, 10).map(c => `• ${c.name} — ${c.location} (${c.type})${c.branch ? `, ${c.branch}` : ''}`)
      return `Top matches in ${foundState}${ownership ? ` (${ownership})` : ''}:
${items.join('\n')}${list.length > 10 ? `\n…and ${list.length - 10} more.` : ''}`
    } catch (e: any) {
      return 'Could not fetch colleges right now. Please try again.'
    }
  }

  const send = async () => {
    if (!input.trim()) return
    const messages = [
      { role: 'system' as const, content: 'You are a helpful Indian college assistant.' },
      ...history.map(m => ({ role: m.role, content: m.content })),
      { role: 'user' as const, content: input.trim() }
    ]
    setLoading(true)
    try {
      const res = await api.aiChat(messages, 'local')
      setHistory([...history, { role: 'user', content: input }, { role: 'assistant', content: res.content || '' }])
      setInput('')
    } catch (e: any) {
      const fallback = await simpleFallback(input)
      setHistory([...history, { role: 'user', content: input }, { role: 'assistant', content: fallback }])
      setInput('')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Head>
        <title>AI Chat - Collink</title>
      </Head>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">AI Chat</h1>
          <div className="bg-white border border-gray-200 rounded-xl p-4">
            <div className="h-80 overflow-auto mb-4 space-y-3">
              {history.length === 0 && (
                <div className="text-gray-500 text-sm">Ask about colleges, states, fees, or ranks…</div>
              )}
              {history.map((m, i) => (
                <div key={i} className={`p-3 rounded-lg ${m.role === 'user' ? 'bg-blue-50 text-blue-800' : 'bg-gray-50 text-gray-800'}`}>{m.content}</div>
              ))}
            </div>
            <div className="flex gap-2">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') send() }}
                placeholder="Type your question…"
                className="flex-1 border border-gray-200 rounded-lg px-3 py-2"
              />
              <button onClick={send} disabled={loading} className="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                {loading ? 'Sending…' : 'Send'}
              </button>
            </div>
          </div>
        </main>
      </div>
    </>
  )
}


