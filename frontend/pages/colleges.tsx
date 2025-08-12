import React, { useEffect, useMemo, useState } from 'react'
import Head from 'next/head'
import Header from '../components/Header'
import { motion } from 'framer-motion'
import { MapPin, Star, Building } from 'lucide-react'

export default function Colleges() {
  const [query, setQuery] = useState('')
  const [exam, setExam] = useState('All Exams')
  const [type, setType] = useState('All Types')
  const [stateFilter, setStateFilter] = useState('All States')
  const [allColleges, setAllColleges] = useState<any[]>([])
  const [visible, setVisible] = useState(30)

  useEffect(() => {
    // Try multiple sources to maximize compatibility
    const tryPaths = [
      '/data/all_colleges.json', // preferred if present in public/data
      '/comprehensive_college_database.json'
    ]
    ;(async () => {
      for (const p of tryPaths) {
        try {
          const r = await fetch(p)
          if (!r.ok) continue
          const data = await r.json()
          const list = Array.isArray(data?.colleges) ? data.colleges : data
          if (Array.isArray(list) && list.length) {
            setAllColleges(list)
            return
          }
        } catch {}
      }
    })()
  }, [])

  const filteredColleges = useMemo(() => {
    const q = query.trim().toLowerCase()
    return allColleges.filter((c: any) => {
      const examOk = exam === 'All Exams' || c.exam === exam
      const typeOk = type === 'All Types' || String(c.type || '').toLowerCase() === type.toLowerCase()
      const stateOk = stateFilter === 'All States' || (c.state || '') === stateFilter
      const searchOk = !q || String(c.name || '').toLowerCase().includes(q)
      return examOk && typeOk && stateOk && searchOk
    })
  }, [allColleges, exam, type, stateFilter, query])

  useEffect(() => {
    setVisible(30)
    const onScroll = () => {
      if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 200) {
        setVisible(v => Math.min(v + 30, filteredColleges.length))
      }
    }
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [filteredColleges.length])

  const uniqueStates = useMemo(
    () => Array.from(new Set(allColleges.map((c: any) => c.state).filter(Boolean))).sort(),
    [allColleges]
  )

  return (
    <>
      <Head>
        <title>Search Colleges - Collink</title>
        <meta name="description" content="Search and browse colleges with authentic names and state tags." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <Header />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Page Header */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-2">Search Colleges</h1>
            <p className="text-gray-600">{filteredColleges.length.toLocaleString()} colleges found</p>
          </motion.div>

          {/* Search & Filters */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="bg-white rounded-2xl shadow-xl p-6 mb-8">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <input
                placeholder="Search colleges, locations..."
                value={query}
                onChange={e => setQuery(e.target.value)}
                className="px-4 py-3 border rounded-lg w-full"
              />
              <select className="px-4 py-3 border rounded-lg" value={exam} onChange={e => setExam(e.target.value)}>
                <option>All Exams</option>
                <option>JEE Main</option>
                <option>JEE Advanced</option>
                <option>NEET</option>
              </select>
              <select className="px-4 py-3 border rounded-lg" value={type} onChange={e => setType(e.target.value)}>
                <option>All Types</option>
                <option>IIT</option>
                <option>NIT</option>
                <option>AIIMS</option>
                <option>Government</option>
                <option>Private</option>
                <option>University</option>
              </select>
              <select className="px-4 py-3 border rounded-lg" value={stateFilter} onChange={e => setStateFilter(e.target.value)}>
                <option>All States</option>
                {uniqueStates.map((s: any) => (
                  <option key={s}>{s}</option>
                ))}
              </select>
            </div>
          </motion.div>

          {/* Colleges List */}
          <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="grid grid-cols-1 gap-6">
            {filteredColleges.slice(0, visible).map((college: any, index: number) => (
              <motion.div key={`${college.name}-${index}`} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: index * 0.02 }} className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden">
                <div className="p-6 border-b border-gray-100">
                  <div className="flex flex-col lg:flex-row gap-6">
                    <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold text-2xl flex-shrink-0">
                      {String(college.name || '').split(' ').map((w: string) => w[0]).join('').slice(0, 3)}
                    </div>
                    <div className="flex-1">
                      <h2 className="text-2xl font-bold text-gray-900 mb-2">{college.name}</h2>
                      <div className="flex flex-wrap items-center gap-4 text-gray-600 mb-4">
                        <div className="flex items-center"><MapPin className="w-4 h-4 mr-2" /><span>{college.state || '—'}</span></div>
                        <div className="flex items-center"><Building className="w-4 h-4 mr-2" /><span>{college.type || '—'}</span></div>
                      </div>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="text-center p-3 bg-gray-50 rounded-lg">
                          <div className="flex items-center justify-center mb-1">
                            <Star className="w-4 h-4 text-yellow-500 mr-1" />
                            <span className="font-bold">{college.rating || '4.0'}</span>
                          </div>
                          <span className="text-sm text-gray-600">Rating</span>
                        </div>
                        <div className="text-center p-3 bg-gray-50 rounded-lg">
                          <div className="font-bold">{college.exam || '—'}</div>
                          <span className="text-sm text-gray-600">Exam</span>
                        </div>
                        <div className="text-center p-3 bg-gray-50 rounded-lg">
                          <div className="font-bold">{college.fees || '—'}</div>
                          <span className="text-sm text-gray-600">Fees</span>
                        </div>
                        <div className="text-center p-3 bg-gray-50 rounded-lg">
                          <div className="font-bold">{Number(college.cutoff || 0).toLocaleString()}</div>
                          <span className="text-sm text-gray-600">Cutoff</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="p-4 text-xs text-gray-500">Source: Careers360 / PDF / Generated</div>
              </motion.div>
            ))}
            {visible < filteredColleges.length && (
              <div className="text-center text-gray-500 py-6">Scroll to load more…</div>
            )}
          </motion.div>
        </div>
      </div>
    </>
  )
}
