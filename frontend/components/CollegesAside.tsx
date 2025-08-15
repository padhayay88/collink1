import React, { useEffect, useMemo, useState, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Landmark, Stethoscope, X, Search, List, Loader2 } from 'lucide-react'
import { api } from '../lib/api'

export default function CollegesAside() {
  const [jeeCount, setJeeCount] = useState<number>(0)
  const [neetCount, setNeetCount] = useState<number>(0)
  const [open, setOpen] = useState<null | 'jee' | 'neet'>(null)
  const [loading, setLoading] = useState(false)
  const [list, setList] = useState<string[]>([])
  const [q, setQ] = useState('')
  const [displayLimit, setDisplayLimit] = useState(50)
  const [isLoadingMore, setIsLoadingMore] = useState(false)
  const [hasMore, setHasMore] = useState(true)
  const observerRef = useRef<IntersectionObserver | null>(null)
  const loadingRef = useRef<HTMLDivElement>(null)

  const filtered = useMemo(() => {
    const term = q.trim().toLowerCase()
    if (!term) return list
    return list.filter(n => n.toLowerCase().includes(term))
  }, [list, q])

  const displayedFiltered = filtered.slice(0, displayLimit)

  // Infinite scroll callback
  const loadMore = useCallback(() => {
    if (isLoadingMore || !hasMore) return
    
    setIsLoadingMore(true)
    setTimeout(() => {
      setDisplayLimit(prev => {
        const newLimit = prev + 50
        if (newLimit >= filtered.length) {
          setHasMore(false)
        }
        return newLimit
      })
      setIsLoadingMore(false)
    }, 300)
  }, [isLoadingMore, hasMore, filtered.length])

  // Intersection observer for infinite scroll
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !isLoadingMore) {
          loadMore()
        }
      },
      { threshold: 0.1 }
    )

    if (loadingRef.current) {
      observer.observe(loadingRef.current)
    }

    observerRef.current = observer

    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect()
      }
    }
  }, [loadMore, hasMore, isLoadingMore])

  useEffect(() => {
    const loadCounts = async () => {
      try {
        const [jee, neet] = await Promise.all([
          api.getAllColleges({ exam: 'jee', limit: 0 }),
          api.getAllColleges({ exam: 'neet', limit: 0 }),
        ])
        setJeeCount(jee?.total || (Array.isArray(jee?.colleges) ? jee.colleges.length : 0))
        setNeetCount(neet?.total || (Array.isArray(neet?.colleges) ? neet.colleges.length : 0))
      } catch {}
    }
    loadCounts()
  }, [])

  const openList = async (exam: 'jee' | 'neet') => {
    setOpen(exam)
    setLoading(true)
    setDisplayLimit(50)
    setHasMore(true)
    try {
      const data = await api.getAllColleges({ exam, limit: 0 })
      const arr = Array.isArray((data as any)?.colleges) ? (data as any).colleges : []
      // Normalize objects to names if needed
      let names = arr.map((c: any) => (typeof c === 'string' ? c : (c?.name || ''))).filter(Boolean)
      // Fallback: use enhanced dataset and filter when exam list is sparse
      if (names.length < 5) {
        const base = await api.getAllColleges({ limit: 0 })
        const baseArr = Array.isArray((base as any)?.colleges) ? (base as any).colleges : []
        const baseNames = baseArr.map((c: any) => (c?.name || '')).filter(Boolean)
        if (exam === 'jee') {
          names = baseNames.filter((n: string) => /\b(IIT|NIT|IIIT|Institute of Technology|National Institute of Technology)\b/i.test(n))
        } else {
          names = baseNames.filter((n: string) => /\b(AIIMS|Medical College|Institute of Medical|Government Medical)\b/i.test(n))
        }
      }
      names.sort((a: string, b: string) => a.localeCompare(b))
      setList(names)
      setQ('')
    } catch {
      setList([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {/* Floating mini-panel with counts */}
      <div className="fixed right-4 top-1/3 z-40 flex flex-col gap-2">
        <motion.button
          whileHover={{ scale: 1.03 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => openList('jee')}
          className="flex items-center gap-2 px-3 py-2 rounded-lg shadow bg-blue-600 text-white"
          title="Show Engineering colleges"
        >
          <Landmark className="w-4 h-4" />
          <span className="text-sm">Engineering</span>
          <span className="ml-2 text-xs bg-white/20 px-2 py-0.5 rounded">{jeeCount}</span>
        </motion.button>
        <motion.button
          whileHover={{ scale: 1.03 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => openList('neet')}
          className="flex items-center gap-2 px-3 py-2 rounded-lg shadow bg-emerald-600 text-white"
          title="Show Medical colleges"
        >
          <Stethoscope className="w-4 h-4" />
          <span className="text-sm">Medical</span>
          <span className="ml-2 text-xs bg-white/20 px-2 py-0.5 rounded">{neetCount}</span>
        </motion.button>
      </div>

      {/* Modal list */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4"
            onClick={() => setOpen(null)}
          >
            <motion.div
              initial={{ scale: 0.97, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.97, opacity: 0 }}
              className="bg-white w-full max-w-3xl rounded-2xl shadow-xl overflow-hidden"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between px-5 py-4 border-b">
                <div className="inline-flex items-center gap-2 font-semibold text-gray-900">
                  <List className="w-4 h-4" /> {open === 'jee' ? 'Engineering Colleges' : 'Medical Colleges'}
                </div>
                <button onClick={() => setOpen(null)} className="p-2 rounded hover:bg-gray-100"><X className="w-5 h-5" /></button>
              </div>
              <div className="p-5 space-y-4">
                <div className="flex items-center gap-2">
                  <Search className="w-4 h-4 text-gray-400" />
                  <input
                    value={q}
                    onChange={(e) => setQ(e.target.value)}
                    placeholder="Search colleges..."
                    className="flex-1 border border-gray-200 rounded-md px-3 py-2"
                  />
                </div>
                {loading ? (
                  <div className="text-sm text-gray-500">Loading...</div>
                ) : (
                  <div className="max-h-[60vh] overflow-auto divide-y border rounded-lg">
                    {displayedFiltered.map((name, i) => (
                      <div key={i} className="px-4 py-2 text-sm text-gray-800">{name}</div>
                    ))}
                    
                    {/* Infinite Scroll Loading Indicator */}
                    {hasMore && filtered.length > 0 && (
                      <div ref={loadingRef} className="flex justify-center py-4">
                        <div className="flex items-center space-x-2 text-gray-600">
                          {isLoadingMore ? (
                            <>
                              <Loader2 className="w-4 h-4 animate-spin" />
                              <span className="text-sm">Loading more colleges...</span>
                            </>
                          ) : (
                            <span className="text-sm">Scroll down to load more colleges</span>
                          )}
                        </div>
                      </div>
                    )}

                    {/* End of Results */}
                    {!hasMore && filtered.length > 0 && (
                      <div className="text-center py-4">
                        <div className="text-sm text-gray-500">
                          You've seen all {filtered.length} colleges
                        </div>
                      </div>
                    )}

                    {filtered.length === 0 && (
                      <div className="px-4 py-6 text-sm text-gray-500 text-center">No colleges found.</div>
                    )}
                  </div>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}


