import React, { useEffect, useMemo, useState } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import Header from '../components/Header'
import { api } from '../lib/api'
import { MapPin, Search } from 'lucide-react'

export default function StatesDirectoryPage() {
  const [states, setStates] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [q, setQ] = useState('')

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      try {
        const res = await api.getSupportedStates('jee')
        setStates(res)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const filtered = useMemo(() => {
    return states.filter(s => s.toLowerCase().includes(q.toLowerCase()))
  }, [states, q])

  return (
    <>
      <Head>
        <title>Browse States - Collink</title>
      </Head>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2"><MapPin className="w-5 h-5 text-blue-600" /> Browse States</h1>
            <p className="text-gray-600 mt-1">Select a state to view Government and Private colleges.</p>
          </div>
          <div className="relative mb-6">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Search state..."
              className="w-full pl-10 pr-3 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
          {loading ? (
            <div className="text-center text-gray-500 py-10">Loading states...</div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
              {filtered.map((st) => (
                <Link
                  key={st}
                  href={{ pathname: '/state', query: { name: st } }}
                  className="px-4 py-3 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 text-gray-800"
                >
                  {st}
                </Link>
              ))}
              {!loading && filtered.length === 0 && (
                <div className="col-span-full text-center text-gray-500 py-10">No states found</div>
              )}
            </div>
          )}
        </main>
      </div>
    </>
  )
}


