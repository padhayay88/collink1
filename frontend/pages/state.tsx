import React, { useEffect, useMemo, useState } from 'react'
import Head from 'next/head'
import { useRouter } from 'next/router'
import Header from '../components/Header'
import { api } from '../lib/api'
import { Building2, ChevronLeft, MapPin, Shield } from 'lucide-react'

export default function StateCollegesPage() {
  const router = useRouter()
  const stateName = useMemo(() => {
    const raw = (router.query.name as string) || ''
    return raw
  }, [router.query.name])

  const [loading, setLoading] = useState(false)
  const [loadingMore, setLoadingMore] = useState(false)
  const [data, setData] = useState<{
    state: string
    ownership_filter?: string
    exam: string
    counts: { government: number; private: number; unknown: number }
    colleges: Array<{ name: string; location: string; type: string; exam_type?: string; branch?: string; opening_rank?: number; closing_rank?: number }>
    total: number
  } | null>(null)
  const [ownership, setOwnership] = useState<'all' | 'government' | 'private'>('all')
  const [limit, setLimit] = useState<number>(200)

  useEffect(() => {
    if (!stateName) return
    const load = async () => {
      setLoading(true)
      try {
        const res = await api.getCollegesByState({ state: stateName, limit })
        setData(res)
      } catch (e) {
        console.error(e)
        setData(null)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [stateName, limit])

  const filtered = useMemo(() => {
    if (!data) return []
    if (ownership === 'all') return data.colleges
    const ownLabel = ownership === 'government' ? 'Government' : 'Private'
    return data.colleges.filter(c => c.type === ownLabel)
  }, [data, ownership])

  return (
    <>
      <Head>
        <title>{stateName ? `${stateName} Colleges` : 'State Colleges'} - Collink</title>
      </Head>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <button onClick={() => router.back()} className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4">
            <ChevronLeft className="w-5 h-5" /> Back
          </button>
          <div className="flex items-center gap-2 mb-4">
            <MapPin className="w-5 h-5 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">{stateName || 'Choose State'}</h1>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-4 mb-6 flex flex-wrap items-center gap-3">
            <span className="text-gray-600">Ownership:</span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setOwnership('all')}
                className={`px-3 py-1.5 rounded-lg border ${ownership === 'all' ? 'border-blue-600 text-blue-700 bg-blue-50' : 'border-gray-200 text-gray-700 hover:bg-gray-50'}`}
              >All</button>
              <button
                onClick={() => setOwnership('government')}
                className={`px-3 py-1.5 rounded-lg border ${ownership === 'government' ? 'border-blue-600 text-blue-700 bg-blue-50' : 'border-gray-200 text-gray-700 hover:bg-gray-50'}`}
              >Government</button>
              <button
                onClick={() => setOwnership('private')}
                className={`px-3 py-1.5 rounded-lg border ${ownership === 'private' ? 'border-blue-600 text-blue-700 bg-blue-50' : 'border-gray-200 text-gray-700 hover:bg-gray-50'}`}
              >Private</button>
            </div>
            {data && (
              <div className="ml-auto text-sm text-gray-500 flex gap-4">
                <span>Total: {data.total}</span>
                <span>Gov: {data.counts.government}</span>
                <span>Priv: {data.counts.private}</span>
                <span>Unknown: {data.counts.unknown}</span>
              </div>
            )}
          </div>

          {loading ? (
            <div className="text-center text-gray-500 py-10">Loading colleges...</div>
          ) : filtered.length === 0 ? (
            <div className="text-center text-gray-500 py-10">No colleges found</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filtered.map((c) => (
                <CollegeCard key={`${c.name}-${c.branch || ''}`} c={c} />
              ))}
            </div>
          )}

          {/* Load more for performance: request next batch */}
          {!loading && data && data.colleges && data.colleges.length >= limit && (
            <div className="flex justify-center mt-6">
              <button
                onClick={async () => {
                  try {
                    setLoadingMore(true)
                    setLimit((prev) => prev + 200)
                  } finally {
                    setTimeout(() => setLoadingMore(false), 200)
                  }
                }}
                className="px-4 py-2 rounded-lg border border-gray-300 bg-white text-gray-800 hover:bg-gray-50"
                disabled={loadingMore}
              >
                {loadingMore ? 'Loading…' : 'Load more'}
              </button>
            </div>
          )}
        </main>
      </div>
    </>
  )
}

// Memoized college card to reduce re-renders
const CollegeCard = React.memo(function CollegeCard({ c }: { c: { name: string; location?: string; type?: string; exam_type?: string; branch?: string; opening_rank?: number; closing_rank?: number } }) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4">
      <div className="flex items-center justify-between mb-2">
        <div className="font-semibold text-gray-900">{c.name}</div>
        <span className={`text-xs px-2 py-1 rounded-full border ${c.type === 'Government' ? 'text-green-700 border-green-200 bg-green-50' : c.type === 'Private' ? 'text-purple-700 border-purple-200 bg-purple-50' : 'text-gray-600 border-gray-200 bg-gray-50'}`}>{c.type || 'Unknown'}</span>
      </div>
      <div className="text-sm text-gray-600 flex items-center gap-1"><MapPin className="w-4 h-4" /> {c.location || 'N/A'}</div>
      {(c.branch || c.opening_rank || c.closing_rank) && (
        <div className="mt-3 text-xs text-gray-700 grid grid-cols-2 gap-2">
          {c.branch && <div className="flex items-center gap-2"><Building2 className="w-4 h-4" /> <span className="truncate" title={c.branch}>{c.branch}</span></div>}
          {typeof c.opening_rank === 'number' && <div>Open Rank: <span className="font-medium">{c.opening_rank}</span></div>}
          {typeof c.closing_rank === 'number' && <div>Close Rank: <span className="font-medium">{c.closing_rank}</span></div>}
          {c.exam_type && <div className="col-span-2 flex items-center gap-2"><Shield className="w-4 h-4" /> Exam: {c.exam_type.toUpperCase()}</div>}
        </div>
      )}
    </div>
  )
})

