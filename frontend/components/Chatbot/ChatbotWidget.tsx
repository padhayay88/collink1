"use client"

import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, X, MessageCircle } from 'lucide-react'
import AnimatedAvatar from './AnimatedAvatar'

interface Msg {
  id: string
  role: 'user' | 'bot'
  text: string
}

export default function ChatbotWidget() {
  const [open, setOpen] = useState(false)
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<Msg[]>([
    { id: 'm1', role: 'bot', text: 'Hi! I\'m Collink Assistant. Ask me about colleges, exams, or predictions.' }
  ])
  const listRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, open])

  async function sendMessage() {
    const text = input.trim()
    if (!text) return
    const userMsg: Msg = { id: crypto.randomUUID(), role: 'user', text }
    setMessages((m) => [...m, userMsg])
    setInput('')

    // Show typing indicator
    const thinking: Msg = { id: crypto.randomUUID(), role: 'bot', text: '...' }
    setMessages((m) => [...m, thinking])

    try {
      // Build chat history for API
      const history = [
        { role: 'system', content: 'You are Collink Assistant. Help users with college search, exam info (JEE/NEET/IELTS), and using the predictor. Be concise.' },
        ...messages
          .filter((m) => m.text !== '...')
          .map((m) => ({ role: m.role === 'user' ? 'user' : 'assistant', content: m.text })),
        { role: 'user', content: text },
      ]

      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: history }),
      })

      const data = await res.json()
      const replyText = data?.reply || 'Sorry, I could not generate a response.'

      setMessages((m) => m.filter((x) => x.id !== thinking.id))
      setMessages((m) => [...m, { id: crypto.randomUUID(), role: 'bot', text: replyText }])
    } catch (err: any) {
      setMessages((m) => m.filter((x) => x.id !== thinking.id))
      setMessages((m) => [...m, { id: crypto.randomUUID(), role: 'bot', text: 'Network error. Please try again.' }])
    }
  }

  async function sendMessageStream() {
    const text = input.trim()
    if (!text) return
    const userMsg: Msg = { id: crypto.randomUUID(), role: 'user', text }
    setMessages((m) => [...m, userMsg])
    setInput('')

    // Streaming placeholder
    const streamId = crypto.randomUUID()
    const botMsg: Msg = { id: streamId, role: 'bot', text: '' }
    setMessages((m) => [...m, botMsg])

    try {
      const history = [
        { role: 'system', content: 'You are Collink Assistant. Help users with college search, exam info (JEE/NEET/IELTS), and using the predictor. Be concise.' },
        ...messages.map((m) => ({ role: m.role === 'user' ? 'user' : 'assistant', content: m.text })),
        { role: 'user', content: text },
      ]

      const response = await fetch('/api/chat-stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: history }),
      })

      if (!response.ok) {
        const txt = await response.text()
        console.error('Stream API non-OK:', response.status, txt)
        // Fallback to non-streaming
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ messages: history }),
        })
        const data = await res.json().catch(() => ({}))
        const upstream = typeof data?.details === 'string' ? data.details : JSON.stringify(data?.details || '')
        const errText = data?.error ? `${data.error}${upstream ? `: ${upstream}` : ''}` : ''
        const replyText = data?.reply || errText || 'Sorry, I could not generate a response.'
        setMessages((m) => m.map((msg) => (msg.id === streamId ? { ...msg, text: replyText } : msg)))
        return
      }

      let gotToken = false
      const timeout = setTimeout(async () => {
        if (!gotToken) {
          try {
            const res = await fetch('/api/chat', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ messages: history }),
            })
            const data = await res.json().catch(() => ({}))
            const upstream = typeof data?.details === 'string' ? data.details : JSON.stringify(data?.details || '')
            const errText = data?.error ? `${data.error}${upstream ? `: ${upstream}` : ''}` : ''
            const replyText = data?.reply || errText || 'Sorry, I could not generate a response.'
            setMessages((m) => m.map((msg) => (msg.id === streamId ? { ...msg, text: replyText } : msg)))
          } catch (e) {
            setMessages((m) => m.map((msg) => (msg.id === streamId ? { ...msg, text: 'Network error. Please try again.' } : msg)))
          }
        }
      }, 6000)

      await readOpenAIStream(response, (token) => {
        gotToken = true
        setMessages((m) => m.map((msg) => (msg.id === streamId ? { ...msg, text: (msg.text || '') + token } : msg)))
      })
      clearTimeout(timeout)

      // If stream returned OK but no content accumulated, fallback once
      const currentBot = messages.find((m) => m.id === streamId)
      const finalText = (currentBot as any)?.text || ''
      if (!finalText) {
        try {
          const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: history }),
          })
          const data = await res.json().catch(() => ({}))
          const upstream = typeof data?.details === 'string' ? data.details : JSON.stringify(data?.details || '')
          const errText = data?.error ? `${data.error}${upstream ? `: ${upstream}` : ''}` : ''
          const replyText = data?.reply || errText || 'Sorry, I could not generate a response.'
          setMessages((m) => m.map((msg) => (msg.id === streamId ? { ...msg, text: replyText } : msg)))
        } catch (e) {
          setMessages((m) => m.map((msg) => (msg.id === streamId ? { ...msg, text: 'Network error. Please try again.' } : msg)))
        }
      }
    } catch (e: any) {
      console.error('Stream error:', e)
      // Final fallback to non-stream
      try {
        const history = [
          { role: 'system', content: 'You are Collink Assistant. Help users with college search, exam info (JEE/NEET/IELTS), and using the predictor. Be concise.' },
          ...messages.map((m) => ({ role: m.role === 'user' ? 'user' : 'assistant', content: m.text })),
          { role: 'user', content: text },
        ]
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ messages: history }),
        })
        const data = await res.json().catch(() => ({}))
        const upstream = typeof data?.details === 'string' ? data.details : JSON.stringify(data?.details || '')
        const errText = data?.error ? `${data.error}${upstream ? `: ${upstream}` : ''}` : ''
        const replyText = data?.reply || errText || 'Sorry, I could not generate a response.'
        setMessages((m) => m.map((msg) => (msg.id === streamId ? { ...msg, text: replyText } : msg)))
      } catch (err) {
        console.error('Fallback error:', err)
        setMessages((m) => m.map((msg) => (msg.id === streamId ? { ...msg, text: 'Network error. Please try again.' } : msg)))
      }
    }
  }


  return (
    <>
      {/* Floating button */}
      <motion.button
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 z-40 rounded-full p-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{
          scale: 1,
          opacity: 1,
          y: [0, -4, 0, 4, 0],
          x: [0, 2, 0, -2, 0],
          boxShadow: [
            '0 10px 15px -3px rgba(59,130,246,0.2), 0 4px 6px -4px rgba(59,130,246,0.2)',
            '0 10px 18px -3px rgba(147,51,234,0.25), 0 4px 8px -4px rgba(147,51,234,0.25)',
            '0 10px 15px -3px rgba(59,130,246,0.2), 0 4px 6px -4px rgba(59,130,246,0.2)'
          ]
        }}
        transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
        whileHover={{ scale: 1.06, rotate: -2 }}
        aria-label="Open Chatbot"
      >
        <div className="relative flex items-center justify-center">
          {/* Show the actual chatbot avatar without needing to open */}
          <div className="scale-110">
            <AnimatedAvatar src="/chatbot.png" />
          </div>
          <motion.span
            className="absolute -top-1 -right-1 inline-block w-2 h-2 rounded-full bg-pink-400"
            animate={{ scale: [1, 1.4, 1] }}
            transition={{ repeat: Infinity, duration: 1.6 }}
          />
        </div>
      </motion.button>

      {/* Panel */}
      <AnimatePresence>
        {open && (
          <motion.div
            className="fixed bottom-6 right-6 z-50 w-[360px] max-w-[92vw]"
            initial={{ opacity: 0, y: 20, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.96 }}
            drag
            dragMomentum={false}
            dragElastic={0.2}
            dragConstraints={{ left: -300, right: 0, top: -300, bottom: 0 }}
          >
            <div className="rounded-2xl overflow-hidden shadow-2xl border border-gray-200 bg-white">
              {/* Header */}
              <div className="flex items-center justify-between p-3 border-b bg-slate-50">
                <div className="flex items-center gap-3">
                  <AnimatedAvatar src="/chatbot.png" />
                  <div>
                    <div className="font-semibold text-slate-900">Collink Assistant</div>
                    <div className="text-xs text-slate-500">Online • helpful</div>
                  </div>
                </div>
                <button onClick={() => setOpen(false)} className="p-2 text-slate-500 hover:text-slate-700" aria-label="Close">
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Messages */}
              <div ref={listRef} className="h-80 overflow-y-auto p-4 space-y-3 bg-white">
                {messages.map((m) => (
                  <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <motion.div
                      initial={{ opacity: 0, y: 6 }}
                      animate={{ opacity: 1, y: 0 }}
                      className={`${m.role === 'user' ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white' : 'bg-slate-100 text-slate-800'} px-3 py-2 rounded-xl max-w-[80%] text-sm`}
                    >
                      {m.text === '...' ? (
                        <div className="flex items-center gap-1">
                          <span className="typing-dot" />
                          <span className="typing-dot" />
                          <span className="typing-dot" />
                        </div>
                      ) : (
                        m.text
                      )}
                    </motion.div>
                  </div>
                ))}
              </div>

              {/* Input */}
              <form
                className="flex items-center gap-2 p-3 border-t bg-white"
                onSubmit={(e) => {
                  e.preventDefault()
                  sendMessageStream()
                }}
              >
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask about colleges, exams, or predictions..."
                  className="flex-1 rounded-xl border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button type="submit" className="rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 text-white p-2 shadow hover:shadow-md" aria-label="Send">
                  <Send className="w-5 h-5" />
                </button>
              </form>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      {/* Typing dots animation */}
      <style jsx>{`
        .typing-dot {
          width: 6px;
          height: 6px;
          border-radius: 9999px;
          background: #94a3b8; /* slate-400 */
          display: inline-block;
          animation: blink 1.4s infinite ease-in-out both;
        }
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        @keyframes blink {
          0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
          40% { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </>
  )
}

async function readOpenAIStream(response: Response, onToken: (t: string) => void) {
  const reader = (response as any).body?.getReader?.()
  if (!reader) return
  const decoder = new TextDecoder('utf-8')
  let done = false
  while (!done) {
    const { value, done: d } = await reader.read()
    done = d
    const chunk = decoder.decode(value, { stream: true })
    const lines = chunk.split('\n')
    for (const line of lines) {
      const trimmed = line.trim()
      if (!trimmed.startsWith('data:')) continue
      const data = trimmed.replace(/^data:\s*/, '')
      if (data === '[DONE]') return
      try {
        const json = JSON.parse(data)
        // OpenAI-style
        const delta = json?.choices?.[0]?.delta?.content
        if (typeof delta === 'string' && delta.length) {
          onToken(delta)
          continue
        }
        // Gemini-style: candidates[].content.parts[].text
        const parts = json?.candidates?.[0]?.content?.parts
        if (Array.isArray(parts)) {
          for (const p of parts) {
            const t = typeof p?.text === 'string' ? p.text : ''
            if (t) onToken(t)
          }
        }
      } catch (_) {
        // ignore
      }
    }
  }
}

