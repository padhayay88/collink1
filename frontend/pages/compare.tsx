import React, { useEffect, useMemo, useState } from 'react'
import Head from 'next/head'
import { useRouter } from 'next/router'
import api from '../lib/api'
import Header from '../components/Header'
import { toast } from 'react-hot-toast'
import { Trophy, ArrowUpRight, Share2, Copy, Award } from 'lucide-react'

interface ComparedCollege {
  name: string
  location?: string
  nirf_rank?: number
  fees?: number
  average_package?: number
  overall_rating?: number
}

export default function ComparePage() {
  const router = useRouter()
  const [colleges, setColleges] = useState<string[]>([])
  const [data, setData] = useState<ComparedCollege[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Parse query once router is ready
  useEffect(() => {
    if (!router.isReady) return
    const raw = (router.query.colleges as string) || ''
    if (!raw) return
    try {
      // raw may be comma separated (already encoded by caller)
      const decoded = decodeURIComponent(raw)
      const list = decoded.split(',').map(s => s.trim()).filter(Boolean).slice(0, 4)
      setColleges(list)
    } catch (e) {
      // fallback: try simple split
      const list = raw.split(',').map(s => s.trim()).filter(Boolean).slice(0, 4)
      setColleges(list)
    }
  }, [router.isReady, router.query.colleges])

  // Fetch compare
  useEffect(() => {
    const run = async () => {
      if (!colleges.length) return
      setLoading(true)
      setError(null)
      try {
        const res = await api.compareColleges(colleges)
        setData(res.colleges || [])
      } catch (e: any) {
        setError(e?.message || 'Failed to compare colleges')
        setData([])
      } finally {
        setLoading(false)
      }
    }
    run()
  }, [colleges.join('|')])

  const headers = useMemo(() => [
    { key: 'name', label: 'College' },
    { key: 'location', label: 'Location' },
    { key: 'nirf_rank', label: 'NIRF Rank' },
    { key: 'fees', label: 'Annual Fees (₹)' },
    { key: 'average_package', label: 'Avg Package (₹ LPA)' },
    { key: 'overall_rating', label: 'Rating/10' },
  ] as const, [])

  // Determine best-in-class for highlighting
  const best = useMemo(() => {
    if (!data.length) return {}
    const ranks = data.map(d => d.nirf_rank ?? Number.POSITIVE_INFINITY)
    const fees = data.map(d => d.fees ?? Number.POSITIVE_INFINITY)
    const pkgs = data.map(d => d.average_package ?? Number.NEGATIVE_INFINITY)
    const ratings = data.map(d => d.overall_rating ?? Number.NEGATIVE_INFINITY)
    return {
      nirf_rank: Math.min(...ranks),
      fees: Math.min(...fees),
      average_package: Math.max(...pkgs),
      overall_rating: Math.max(...ratings),
    }
  }, [data]) as any

  const isBest = (key: keyof ComparedCollege, val: any) => {
    if (val === undefined || val === null) return false
    return best && best[key as any] === val
  }

  return (
    <>
      <Head>
        <title>Compare Colleges - Collink</title>
      </Head>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 relative overflow-hidden">
        <div className="relative z-10">
          <Header />
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <div className="mb-6 flex items-start justify-between gap-4">
              <div>
                <h1 className="text-3xl md:text-4xl font-bold text-gray-900">Compare Colleges</h1>
                <p className="text-gray-600">{colleges.length ? `Comparing: ${colleges.join(' vs ')}` : 'Select colleges to compare from predictions page.'}</p>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={async () => {
                    try {
                      const url = typeof window !== 'undefined' ? window.location.href : ''
                      await navigator.clipboard.writeText(url)
                      toast.success('Share link copied')
                    } catch {
                      toast.error('Failed to copy link')
                    }
                  }}
                  className="inline-flex items-center px-3 py-2 rounded-lg bg-white shadow border hover:bg-gray-50 text-sm text-gray-700"
                >
                  <Share2 className="w-4 h-4 mr-2" /> Share
                </button>
              </div>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 mb-6">
                {error}
              </div>
            )}

            {loading ? (
              <div className="bg-white rounded-2xl shadow p-6 animate-pulse">
                <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
                <div className="space-y-3">
                  {Array.from({ length: 5 }).map((_, i) => (
                    <div key={i} className="grid grid-cols-6 gap-4">
                      {Array.from({ length: 6 }).map((__, j) => (
                        <div key={j} className="h-5 bg-gray-200 rounded"></div>
                      ))}
                    </div>
                  ))}
                </div>
              </div>
            ) : data.length ? (
              <div className="bg-white rounded-2xl shadow overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50 sticky top-0 z-10">
                    <tr>
                      {headers.map(h => (
                        <th key={h.key} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          {h.label}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-100">
                    {data.map((c, idx) => (
                      <tr key={`${c.name}-${idx}`} className="hover:bg-gray-50">
                        <td className="px-6 py-4 text-sm font-semibold text-gray-900">
                          <div className="flex items-center gap-2">
                            <span>{c.name}</span>
                            {isBest('overall_rating', c.overall_rating) && (
                              <span className="inline-flex items-center text-[10px] px-2 py-0.5 rounded-full bg-green-100 text-green-700 border border-green-200"><Trophy className="w-3 h-3 mr-1"/>Best Rated</span>
                            )}
                            {isBest('nirf_rank', c.nirf_rank) && (
                              <span className="inline-flex items-center text-[10px] px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-700 border border-indigo-200"><Award className="w-3 h-3 mr-1"/>Top NIRF</span>
                            )}
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-700">{c.location || '—'}</td>
                        <td className={`px-6 py-4 text-sm ${isBest('nirf_rank', c.nirf_rank) ? 'text-indigo-700 font-semibold' : 'text-gray-700'}`}>{c.nirf_rank ?? '—'}</td>
                        <td className={`px-6 py-4 text-sm ${isBest('fees', c.fees) ? 'text-green-700 font-semibold' : 'text-gray-700'}`}>{c.fees ? `₹${c.fees.toLocaleString()}` : '—'}</td>
                        <td className={`px-6 py-4 text-sm ${isBest('average_package', c.average_package) ? 'text-blue-700 font-semibold' : 'text-gray-700'}`}>{c.average_package ? `${c.average_package}` : '—'}</td>
                        <td className={`px-6 py-4 text-sm ${isBest('overall_rating', c.overall_rating) ? 'text-emerald-700 font-semibold' : 'text-gray-700'}`}>{c.overall_rating ?? '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="bg-white rounded-2xl shadow p-10 text-center text-gray-600">
                No comparison data. Go back and select at least two colleges to compare.
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
