import React, { useEffect, useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import { Layers, ChevronDown, ChevronUp, Search } from 'lucide-react'
import { api } from '../lib/api'

interface BranchBrowserProps {
  rank: number
  exam: string
}

export default function BranchBrowser({ rank, exam }: BranchBrowserProps) {
  const [open, setOpen] = useState(true)
  const [loading, setLoading] = useState(false)
  const [branches, setBranches] = useState<string[]>([])
  const [query, setQuery] = useState('')
  const [selected, setSelected] = useState<string>('')
  const [results, setResults] = useState<Array<{ college: string; branch: string; opening_rank?: number; closing_rank?: number; location?: string }>>([])
  const [loadingResults, setLoadingResults] = useState(false)
  const isJEE = useMemo(() => (exam || '').toLowerCase() === 'jee', [exam])

  const filteredBranches = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return branches
    return branches.filter(b => b.toLowerCase().includes(q))
  }, [branches, query])

  const loadBranches = async () => {
    if (!isJEE || branches.length > 0) return
    setLoading(true)
    try {
      const data = await api.listJEEBranches()
      let list = Array.isArray(data?.branches) ? data.branches : []
      // Fallback to a default comprehensive list if API returns empty
      if (list.length === 0) {
        list = [
          'Computer Science and Engineering',
          'Information Technology',
          'Electronics and Communication Engineering',
          'Electrical Engineering',
          'Mechanical Engineering',
          'Civil Engineering',
          'Chemical Engineering',
          'Aerospace Engineering',
          'Metallurgical and Materials Engineering',
          'Biotechnology',
          'Instrumentation Engineering',
          'Production and Industrial Engineering',
          'Mechatronics Engineering',
          'Automobile Engineering',
          'Mining Engineering',
          'Petroleum Engineering',
          'Data Science',
          'Artificial Intelligence and Machine Learning',
          'Electronics and Instrumentation Engineering',
          'Electronics and Electrical Engineering',
        ]
      }
      // Unique + sorted
      const uniq = Array.from(new Set(list)).sort((a, b) => a.localeCompare(b))
      setBranches(uniq)
    } catch (e) {
      // Load defaults on error
      const uniq = Array.from(new Set([
        'Computer Science and Engineering',
        'Information Technology',
        'Electronics and Communication Engineering',
        'Electrical Engineering',
        'Mechanical Engineering',
        'Civil Engineering',
        'Chemical Engineering',
      ])).sort((a, b) => a.localeCompare(b))
      setBranches(uniq)
    } finally {
      setLoading(false)
    }
  }

  const loadResults = async (branch: string) => {
    setLoadingResults(true)
    try {
      const data = await api.getCollegesByBranch({ branch, rank, limit: 100 })
      setResults(data.colleges)
    } catch (e) {
      setResults([])
    } finally {
      setLoadingResults(false)
    }
  }

  useEffect(() => {
    loadBranches()
  }, [])

  if (!isJEE) return null

  return (
    <div className="mt-10">
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 py-3 rounded-lg border border-gray-200 bg-white text-gray-800 mb-4"
      >
        <span className="inline-flex items-center gap-2 font-medium"><Layers className="w-4 h-4" /> Browse Branches (JEE)</span>
        {open ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
      </motion.button>

      {open && (
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <div className="flex items-center gap-2 mb-3">
            <Search className="w-4 h-4 text-gray-400" />
            <input
              placeholder="Filter branches (e.g., Computer Science)"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="flex-1 border border-gray-200 rounded-md px-3 py-2"
            />
          </div>
          {loading ? (
            <div className="text-sm text-gray-500">Loading branches…</div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 max-h-56 overflow-auto">
              {filteredBranches.map((b) => (
                <button
                  key={b}
                  onClick={() => { setSelected(b); loadResults(b) }}
                  className={`text-left px-3 py-2 rounded-md border ${selected === b ? 'border-blue-400 bg-blue-50' : 'border-gray-200 hover:bg-gray-50'}`}
                  title={b}
                >
                  {b}
                </button>
              ))}
              {filteredBranches.length === 0 && (
                <div className="text-sm text-gray-500">No branches match your filter.</div>
              )}
            </div>
          )}

          {/* Results */}
          {selected && (
            <div className="mt-5">
              <div className="text-sm text-gray-700 mb-2">Colleges for <span className="font-semibold">{selected}</span> near rank <span className="font-semibold">{rank.toLocaleString()}</span></div>
              {loadingResults ? (
                <div className="text-sm text-gray-500">Loading colleges…</div>
              ) : (
                <div className="space-y-2">
                  {results.map((r, idx) => (
                    <div key={idx} className="p-3 rounded-lg border border-gray-200 bg-white flex items-center justify-between">
                      <div>
                        <div className="font-medium text-gray-900">{r.college}</div>
                        <div className="text-sm text-gray-600">{r.location || 'India'}</div>
                      </div>
                      <div className="text-right text-sm">
                        <div className="text-gray-800">{(r.opening_rank || '-')}-{(r.closing_rank || '-')}</div>
                        <div className="text-gray-500">Opening–Closing</div>
                      </div>
                    </div>
                  ))}
                  {results.length === 0 && (
                    <div className="text-sm text-gray-500">No colleges found.</div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}


