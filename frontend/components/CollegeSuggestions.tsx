import React, { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { toast } from 'react-hot-toast'

import { CheckCircle, AlertTriangle, XCircle, MapPin, TrendingUp, ExternalLink, GraduationCap, BarChart2, Save, Bell, Heart, Share2, Copy, Eye, Globe, BookOpen, UserCheck, FileText, ChevronDown, ChevronUp, Info, Star, Bookmark, Award, Home, Building2, Phone, MessageCircle, IndianRupee, Gift, Loader2 } from 'lucide-react'
import TrendChart from './TrendChart'
import api, { Prediction } from '../lib/api'

// Use shared Prediction type from lib/api

interface CollegeSuggestionsProps {
  predictions: Prediction[]
  exam: string
  rank: number
  category: string
  enableCompare?: boolean
}

export default function CollegeSuggestions({ predictions, exam, rank, category, enableCompare = true }: CollegeSuggestionsProps) {
  const [displayLimit, setDisplayLimit] = useState(20) // Start with fewer items
  const [isLoading, setIsLoading] = useState(false)
  const [hasMore, setHasMore] = useState(true)
  const observerRef = useRef<IntersectionObserver | null>(null)
  const loadingRef = useRef<HTMLDivElement>(null)
  const [selectedCompare, setSelectedCompare] = useState<Set<string>>(new Set())
  const pageScrollRef = useRef<number>(0)
  const highRef = useRef<HTMLDivElement>(null)
  const medRef = useRef<HTMLDivElement>(null)
  const lowRef = useRef<HTMLDivElement>(null)
  const [highStart, setHighStart] = useState(0)
  const [medStart, setMedStart] = useState(0)
  const [lowStart, setLowStart] = useState(0)

  const APPROX_ROW = 220 // px, approximate card height including gap
  const WINDOW_COUNT = 30 // how many items to render per section
  const BUFFER = 6

  // Persist compare selections in localStorage
  useEffect(() => {
    try {
      const saved = localStorage.getItem('compare.selection')
      if (saved) {
        const arr: string[] = JSON.parse(saved)
        setSelectedCompare(new Set(arr))
      }
    } catch {}
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    try {
      const arr = Array.from(selectedCompare)
      localStorage.setItem('compare.selection', JSON.stringify(arr))
    } catch {}
  }, [selectedCompare])

  const isSelected = useCallback((name: string) => selectedCompare.has(name), [selectedCompare])
  const toggleSelected = useCallback((name: string) => {
    setSelectedCompare(prev => {
      const next = new Set(prev)
      if (next.has(name)) next.delete(name)
      else next.add(name)
      return next
    })
  }, [])

  const getConfidenceColor = (confidence?: string, level?: string) => {
    const val = (confidence || level || '').toLowerCase()
    switch (val) {
      case 'high':
        return 'text-green-700 bg-green-100 border-green-200'
      case 'medium':
        return 'text-yellow-700 bg-yellow-100 border-yellow-200'
      case 'low':
        return 'text-red-700 bg-red-100 border-red-200'
      default:
        return 'text-gray-700 bg-gray-100 border-gray-200'
    }
  }

  const getConfidenceIcon = (confidence?: string, level?: string) => {
    const val = (confidence || level || '').toLowerCase()
    switch (val) {
      case 'high':
        return CheckCircle
      case 'medium':
        return AlertTriangle
      case 'low':
        return XCircle
      default:
        return AlertTriangle
    }
  }

  const formatRankRange = (opening?: number, closing?: number) => {
    if (opening && closing) {
      return `${opening.toLocaleString()} - ${closing.toLocaleString()}`
    }
    return 'N/A'
  }

  const formatIELTSScore = (min?: number, preferred?: number) => {
    if (min && preferred) {
      return `${min} - ${preferred}`
    } else if (min) {
      return `${min}+`
    }
    return 'N/A'
  }

  const highConfidenceColleges = predictions.filter(p => (p.confidence || p.confidence_level || '').toLowerCase() === 'high')
  const mediumConfidenceColleges = predictions.filter(p => (p.confidence || p.confidence_level || '').toLowerCase() === 'medium')
  const lowConfidenceColleges = predictions.filter(p => (p.confidence || p.confidence_level || '').toLowerCase() === 'low')
  
  // Performance: Limit initial display with infinite scroll
  const displayedHigh = highConfidenceColleges.slice(0, displayLimit)
  const displayedMedium = mediumConfidenceColleges.slice(0, displayLimit)
  const displayedLow = lowConfidenceColleges.slice(0, displayLimit)

  // Infinite scroll callback
  const loadMore = useCallback(() => {
    if (isLoading || !hasMore) return
    
    setIsLoading(true)
    setTimeout(() => {
      setDisplayLimit(prev => {
        const newLimit = prev + 20
        const totalColleges = highConfidenceColleges.length + mediumConfidenceColleges.length + lowConfidenceColleges.length
        if (newLimit >= totalColleges) {
          setHasMore(false)
        }
        return newLimit
      })
      setIsLoading(false)
    }, 500) // Simulate loading delay
  }, [isLoading, hasMore, highConfidenceColleges.length, mediumConfidenceColleges.length, lowConfidenceColleges.length])

  // Intersection observer for infinite scroll
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !isLoading) {
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
  }, [loadMore, hasMore, isLoading])

  // Reset display limit when predictions change
  useEffect(() => {
    setDisplayLimit(20)
    setHasMore(true)
    setIsLoading(false)
  }, [predictions])

  // Lightweight virtualization: compute start index per section based on scroll
  useEffect(() => {
    const onScroll = () => {
      const y = window.scrollY
      pageScrollRef.current = y
      const updateFor = (el: HTMLElement | null, total: number, setFn: (n: number) => void) => {
        if (!el || total === 0) return
        const rect = el.getBoundingClientRect()
        const top = rect.top + window.scrollY
        const rel = Math.max(0, y - top)
        const idx = Math.floor(rel / APPROX_ROW)
        const start = Math.max(0, Math.min(total - 1, idx - BUFFER))
        setFn(start)
      }
      updateFor(highRef.current, displayedHigh.length, setHighStart)
      updateFor(medRef.current, displayedMedium.length, setMedStart)
      updateFor(lowRef.current, displayedLow.length, setLowStart)
    }
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [displayedHigh.length, displayedMedium.length, displayedLow.length])

  if (predictions.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-2xl shadow-xl p-12 text-center"
      >
        <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <TrendingUp className="w-10 h-10 text-gray-400" />
        </div>
        <h3 className="text-2xl font-bold text-gray-900 mb-4">No Predictions Found</h3>
        <p className="text-gray-600 mb-8 max-w-md mx-auto">
          No colleges found for your rank. Try adjusting your rank or category to get better predictions.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:shadow-lg transition-all duration-200">
            Try Different Rank
          </button>
          <button className="bg-gray-100 text-gray-700 px-6 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-all duration-200">
            Search Colleges
          </button>
        </div>
      </motion.div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl shadow-xl p-8 text-white"
      >
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-3xl font-bold mb-2">College Predictions</h2>
            <p className="text-blue-100">Based on your {(exam || 'exam').toUpperCase()} performance</p>
          </div>
          <div className="w-16 h-16 bg-white bg-opacity-20 rounded-2xl flex items-center justify-center">
            <GraduationCap className="w-8 h-8 text-white" />
          </div>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold">{predictions.length}</div>
            <div className="text-sm text-blue-100">Total Matches</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">{highConfidenceColleges.length}</div>
            <div className="text-sm text-blue-100">High Confidence</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">{rank.toLocaleString()}</div>
            <div className="text-sm text-blue-100">Your {(exam || 'exam') === 'ielts' ? 'Score' : 'Rank'}</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold">{category}</div>
            <div className="text-sm text-blue-100">Category</div>
          </div>
        </div>
      </motion.div>

      {/* High Confidence Colleges */}
      {displayedHigh.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          ref={highRef}
        >
          <div className="flex items-center mb-6">
            <div className="w-3 h-8 bg-green-500 rounded-full mr-3"></div>
            <h3 className="text-2xl font-bold text-gray-900">High Confidence Matches</h3>
            <div className="ml-3 bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
              {displayedHigh.length} of {highConfidenceColleges.length} colleges
            </div>
          </div>
          <div className="grid gap-6">
            <AnimatePresence initial={false}>
              {(() => {
                const start = highStart
                const end = Math.min(displayedHigh.length, start + WINDOW_COUNT)
                const topSpace = start * APPROX_ROW
                const bottomSpace = Math.max(0, (displayedHigh.length - end) * APPROX_ROW)
                const slice = displayedHigh.slice(start, end)
                return (
                  <>
                    {topSpace > 0 && <div style={{ height: topSpace }} />}
                    {slice.map((prediction, i) => (
                      <motion.div
                        key={`high-${start + i}`}
                        initial={{ opacity: 0, y: 12 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -8 }}
                        transition={{ duration: 0.25, delay: (start + i) * 0.035 }}
                        layout
                      >
                        <CollegeCard 
                          prediction={prediction} 
                          exam={exam}
                          compareEnabled={enableCompare}
                          selectedForCompare={isSelected(prediction.college)}
                          onToggleCompare={() => toggleSelected(prediction.college)}
                        />
                      </motion.div>
                    ))}
                    {bottomSpace > 0 && <div style={{ height: bottomSpace }} />}
                  </>
                )
              })()}
            </AnimatePresence>
          </div>
        </motion.div>
      )}

      {/* Medium Confidence Colleges */}
      {displayedMedium.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          ref={medRef}
        >
          <div className="flex items-center mb-6">
            <div className="w-3 h-8 bg-yellow-500 rounded-full mr-3"></div>
            <h3 className="text-2xl font-bold text-gray-900">Medium Confidence Matches</h3>
            <div className="ml-3 bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium">
              {displayedMedium.length} of {mediumConfidenceColleges.length} colleges
            </div>
          </div>
          <div className="grid gap-6">
            <AnimatePresence initial={false}>
              {(() => {
                const start = medStart
                const end = Math.min(displayedMedium.length, start + WINDOW_COUNT)
                const topSpace = start * APPROX_ROW
                const bottomSpace = Math.max(0, (displayedMedium.length - end) * APPROX_ROW)
                const slice = displayedMedium.slice(start, end)
                return (
                  <>
                    {topSpace > 0 && <div style={{ height: topSpace }} />}
                    {slice.map((prediction, i) => (
                      <motion.div
                        key={`medium-${start + i}`}
                        initial={{ opacity: 0, y: 12 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -8 }}
                        transition={{ duration: 0.25, delay: (start + i) * 0.035 }}
                        layout
                      >
                        <CollegeCard prediction={prediction} exam={exam} />
                      </motion.div>
                    ))}
                    {bottomSpace > 0 && <div style={{ height: bottomSpace }} />}
                  </>
                )
              })()}
            </AnimatePresence>
          </div>
        </motion.div>
      )}

      {/* Low Confidence Colleges */}
      {displayedLow.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          ref={lowRef}
        >
          <div className="flex items-center mb-6">
            <div className="w-3 h-8 bg-red-500 rounded-full mr-3"></div>
            <h3 className="text-2xl font-bold text-gray-900">Reach Colleges</h3>
            <div className="ml-3 bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium">
              {displayedLow.length} of {lowConfidenceColleges.length} colleges
            </div>
          </div>
          <div className="grid gap-6">
            <AnimatePresence initial={false}>
              {(() => {
                const start = lowStart
                const end = Math.min(displayedLow.length, start + WINDOW_COUNT)
                const topSpace = start * APPROX_ROW
                const bottomSpace = Math.max(0, (displayedLow.length - end) * APPROX_ROW)
                const slice = displayedLow.slice(start, end)
                return (
                  <>
                    {topSpace > 0 && <div style={{ height: topSpace }} />}
                    {slice.map((prediction, i) => (
                      <motion.div
                        key={`low-${start + i}`}
                        initial={{ opacity: 0, y: 12 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -8 }}
                        transition={{ duration: 0.25, delay: (start + i) * 0.035 }}
                        layout
                      >
                        <CollegeCard prediction={prediction} exam={exam} />
                      </motion.div>
                    ))}
                    {bottomSpace > 0 && <div style={{ height: bottomSpace }} />}
                  </>
                )
              })()}
            </AnimatePresence>
          </div>
        </motion.div>
      )}

      {/* Infinite Scroll Loading Indicator */}
      {hasMore && (
        <div ref={loadingRef} className="flex justify-center py-8">
          <div className="flex items-center space-x-2 text-gray-600">
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Loading more colleges...</span>
              </>
            ) : (
              <span>Scroll down to load more colleges</span>
            )}
          </div>
        </div>
      )}

      {/* End of Results */}
      {!hasMore && predictions.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-8"
        >
          <div className="bg-gray-50 rounded-lg p-6">
            <CheckCircle className="w-8 h-8 text-green-500 mx-auto mb-2" />
            <p className="text-gray-600">You've seen all {predictions.length} college predictions</p>
            <p className="text-sm text-gray-500 mt-1">Use the filters above to refine your search</p>
          </div>
        </motion.div>
      )}

      {/* Compare Action Bar */}
      {enableCompare && selectedCompare.size >= 1 && (
        <div className="fixed bottom-20 left-1/2 -translate-x-1/2 z-40">
          <div className="bg-white shadow-2xl rounded-full px-4 py-2 border border-gray-200 flex items-center gap-3">
            <span className="text-sm text-gray-700">Selected: {selectedCompare.size}</span>
            <button
              className={`text-sm px-3 py-1.5 rounded-full ${selectedCompare.size >= 2 ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-500'}`}
              disabled={selectedCompare.size < 2}
              onClick={() => {
                const names = Array.from(selectedCompare).slice(0, 4)
                const q = encodeURIComponent(names.join(','))
                const url = `/compare?colleges=${q}`
                window.open(url, '_blank')
                toast.success('Opened compare in a new tab')
              }}
            >
              Compare
            </button>
            <button
              className="text-sm px-3 py-1.5 rounded-full bg-purple-600 text-white"
              onClick={async () => {
                try {
                  const uid = 'local-user'
                  const names = Array.from(selectedCompare)
                  for (const n of names) {
                    await api.saveCollege(uid, n)
                  }
                  toast.success(`Saved ${names.length} colleges`)
                  // update localStorage to persist and sync across tabs
                  try {
                    const cached = localStorage.getItem('saved.colleges')
                    const list: string[] = cached ? JSON.parse(cached) : []
                    const merged = Array.from(new Set([...list, ...names]))
                    localStorage.setItem('saved.colleges', JSON.stringify(merged))
                  } catch {}
                } catch (e) {
                  console.error('Save selected failed', e)
                  toast.error('Failed to save some colleges')
                }
              }}
            >
              Save Selected
            </button>
            <button
              className="text-sm px-3 py-1.5 rounded-full bg-gray-100 hover:bg-gray-200"
              onClick={() => {
                const id = toast.custom((t) => (
                  <div className="bg-white border border-gray-200 shadow-lg rounded-lg p-3 flex items-center gap-3">
                    <span className="text-sm text-gray-700">Clear all selections?</span>
                    <button
                      className="text-sm px-2 py-1 rounded bg-gray-100 hover:bg-gray-200"
                      onClick={() => toast.dismiss(t.id)}
                    >
                      Cancel
                    </button>
                    <button
                      className="text-sm px-2 py-1 rounded bg-red-600 text-white hover:bg-red-700"
                      onClick={() => {
                        setSelectedCompare(new Set())
                        toast.dismiss(t.id)
                        toast.success('Cleared selections')
                      }}
                    >
                      Clear
                    </button>
                  </div>
                ))
              }}
            >
              Clear
            </button>
          </div>
        </div>
      )}

      {/* Summary Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-white rounded-2xl shadow-xl p-8"
      >
        <h3 className="text-xl font-bold text-gray-900 mb-4">Summary & Next Steps</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <CheckCircle className="w-5 h-5 text-green-600" />
              <span className="text-gray-700">{highConfidenceColleges.length} safe college options</span>
            </div>
            <div className="flex items-center space-x-3">
              <AlertTriangle className="w-5 h-5 text-yellow-600" />
              <span className="text-gray-700">{mediumConfidenceColleges.length} moderate reach colleges</span>
            </div>
            <div className="flex items-center space-x-3">
              <XCircle className="w-5 h-5 text-red-600" />
              <span className="text-gray-700">{lowConfidenceColleges.length} ambitious reach colleges</span>
            </div>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-sm text-blue-800">
              <strong>💡 Tip:</strong> Apply to a mix of colleges across all confidence levels. 
              High confidence colleges are your safety options, while medium and low confidence 
              colleges are worth pursuing for better opportunities.
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

// Advanced Interactive College Card Component
function CollegeCard({ prediction, exam, compareEnabled, selectedForCompare, onToggleCompare }: { prediction: Prediction; exam: string; compareEnabled?: boolean; selectedForCompare?: boolean; onToggleCompare?: () => void }) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [isFavorited, setIsFavorited] = useState(false)
  const isComparing = !!selectedForCompare
  const [showShareMenu, setShowShareMenu] = useState(false)
  const [copied, setCopied] = useState(false)
  const [aiLoading, setAiLoading] = useState(false)
  const [aiSummary, setAiSummary] = useState<{ overview: string; pros: string[]; cons: string[]; summary: string } | null>(null)

  const confVal = (prediction.confidence || (prediction as any).confidence_level || '').toLowerCase()
  const ConfidenceIcon = confVal === 'high' ? CheckCircle : confVal === 'medium' ? AlertTriangle : XCircle

  const confidenceColor = confVal === 'high' ? 'text-green-700 bg-green-100 border-green-200' :
                          confVal === 'medium' ? 'text-yellow-700 bg-yellow-100 border-yellow-200' :
                          'text-red-700 bg-red-100 border-red-200'

  // Type assertion to access additional properties
  const extendedPrediction = prediction as any
  const collegeName = prediction.college || prediction.university || 'Unknown College'
  const courseName = prediction.branch || prediction.course || 'Course not specified'

  const buildResourceLinks = (name: string) => {
    const q = encodeURIComponent(name)
    
    // Check if we have enriched data with official URLs
    const extendedData = prediction as any
    const officialInfo = extendedData?.official_info || {}
    const officialLinks = extendedData?.official_links || {}
    const searchQueries = extendedData?.search_queries || {}
    const contactQueries = extendedData?.contact_queries || {}
    
    return {
      official: [
        { 
          label: 'Official Website', 
          url: officialInfo.official_website || (officialLinks.website_patterns && officialLinks.website_patterns[0]) || `https://www.google.com/search?q=${q}+official+site`,
          isOfficial: !!(officialInfo.official_website || (officialLinks.website_patterns && officialLinks.website_patterns[0]))
        },
        { 
          label: 'Brochure', 
          url: officialInfo.brochure || searchQueries.google_brochure || `https://www.google.com/search?q=${q}+brochure`,
          isOfficial: !!officialInfo.brochure
        },
        { 
          label: 'Apply Now', 
          url: officialInfo.apply_now || searchQueries.google_admissions || `https://www.google.com/search?q=${q}+admissions+apply`,
          isOfficial: !!officialInfo.apply_now
        },
      ],
      academic: [
        { 
          label: 'NIRF Ranking', 
          url: searchQueries.google_nirf || `https://www.google.com/search?q=${q}+NIRF+ranking+site%3Anirfindia.org`,
          isOfficial: false,
          extraInfo: officialInfo.nirf_rank ? `Rank: ${officialInfo.nirf_rank}` : undefined
        },
        { 
          label: 'Placement Info', 
          url: searchQueries.google_placements || `https://www.google.com/search?q=${q}+placements`,
          isOfficial: false
        },
        { 
          label: 'Facilities', 
          url: `https://www.google.com/search?q=${q}+facilities`,
          isOfficial: false
        },
      ],
      studentLife: [
        { 
          label: 'Hostel Info', 
          url: `https://www.google.com/search?q=${q}+hostel+fees+rules`,
          isOfficial: false
        },
        { 
          label: 'Location (Maps)', 
          url: searchQueries.maps || `https://www.google.com/maps/search/${q}`,
          isOfficial: false
        },
        { 
          label: 'Contact', 
          url: contactQueries.phone || `https://www.google.com/search?q=${q}+contact+email+phone`,
          isOfficial: false,
          extraInfo: officialInfo.contact ? `${officialInfo.contact.phone || ''} ${officialInfo.contact.email || ''}`.trim() : undefined
        },
      ],
      financial: [
        { 
          label: 'Fee Structure', 
          url: searchQueries.google_fees || `https://www.google.com/search?q=${q}+fee+structure`,
          isOfficial: false,
          extraInfo: officialInfo.fee_range ? `₹${officialInfo.fee_range}` : undefined
        },
        { 
          label: 'Scholarships', 
          url: `https://www.google.com/search?q=${q}+scholarship`,
          isOfficial: false
        },
        { 
          label: 'Payment', 
          url: `https://www.google.com/search?q=${q}+fee+payment+portal`,
          isOfficial: false
        },
      ],
      reviews: [
        { 
          label: 'Student Reviews', 
          url: `https://www.google.com/search?q=${q}+student+reviews`,
          isOfficial: false
        },
        { 
          label: 'Shiksha Reviews', 
          url: searchQueries.shiksha || `https://www.shiksha.com/search?q=${q}`,
          isOfficial: false
        },
        { 
          label: 'Careers360', 
          url: searchQueries.careers360 || extendedData?.careers360_url || `https://www.careers360.com/search?q=${q}`,
          isOfficial: !!extendedData?.careers360_url
        },
      ],
      resources: [
        { 
          label: 'Google Search', 
          url: searchQueries.google_official || `https://www.google.com/search?q=${q}`,
          isOfficial: false
        },
        { 
          label: 'YouTube', 
          url: searchQueries.youtube || `https://www.youtube.com/results?search_query=${q}`,
          isOfficial: false
        },
        { 
          label: 'LinkedIn', 
          url: searchQueries.linkedin || `https://www.linkedin.com/search/results/all/?keywords=${q}`,
          isOfficial: false
        },
      ],
    }
  }

  const resource = buildResourceLinks(collegeName)

  // Advanced link data with enhanced categorization
  const linkCategories = {
    official: {
      name: 'Official Website',
      url: extendedPrediction.website,
      icon: Globe,
      color: 'bg-blue-50 text-blue-700 hover:bg-blue-100 border-blue-200'
    },
    academics: {
      name: 'Academic Info',
      url: extendedPrediction.brochure || extendedPrediction.program_details,
      icon: BookOpen,
      color: 'bg-green-50 text-green-700 hover:bg-green-100 border-green-200'
    },
    admissions: {
      name: 'Apply Now',
      url: extendedPrediction.admission_details || extendedPrediction.application_link,
      icon: UserCheck,
      color: 'bg-orange-50 text-orange-700 hover:bg-orange-100 border-orange-200'
    },
    brochure: {
      name: 'Brochure',
      url: extendedPrediction.brochure,
      icon: FileText,
      color: 'bg-purple-50 text-purple-700 hover:bg-purple-100 border-purple-200'
    },
    placement: {
      name: 'Placement Info',
      url: extendedPrediction.placement_link || `${extendedPrediction.website}/placement`,
      icon: TrendingUp,
      color: 'bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border-indigo-200'
    },
    hostel: {
      name: 'Hostel Info',
      url: extendedPrediction.hostel_link || `${extendedPrediction.website}/hostel`,
      icon: Home,
      color: 'bg-pink-50 text-pink-700 hover:bg-pink-100 border-pink-200'
    },
    facilities: {
      name: 'Facilities',
      url: extendedPrediction.facilities_link || `${extendedPrediction.website}/facilities`,
      icon: Building2,
      color: 'bg-teal-50 text-teal-700 hover:bg-teal-100 border-teal-200'
    },
    contact: {
      name: 'Contact Info',
      url: extendedPrediction.contact_link || `${extendedPrediction.website}/contact`,
      icon: Phone,
      color: 'bg-gray-50 text-gray-700 hover:bg-gray-100 border-gray-200'
    },
    location: {
      name: 'Location',
      url: `https://maps.google.com/?q=${encodeURIComponent(collegeName)}`,
      icon: MapPin,
      color: 'bg-red-50 text-red-700 hover:bg-red-100 border-red-200'
    },
    reviews: {
      name: 'Student Reviews',
      url: `https://www.collegedekho.com/colleges/${encodeURIComponent(collegeName.toLowerCase().replace(/\s+/g, '-'))}`,
      icon: MessageCircle,
      color: 'bg-cyan-50 text-cyan-700 hover:bg-cyan-100 border-cyan-200'
    },
    fees: {
      name: 'Fee Structure',
      url: extendedPrediction.fees_link || `${extendedPrediction.website}/fees`,
      icon: IndianRupee,
      color: 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border-emerald-200'
    },
    scholarship: {
      name: 'Scholarships',
      url: extendedPrediction.scholarship_link || `${extendedPrediction.website}/scholarship`,
      icon: Gift,
      color: 'bg-amber-50 text-amber-700 hover:bg-amber-100 border-amber-200'
    }
  }

  const availableLinks = Object.entries(linkCategories).filter(([_, link]) => link.url)

  const handleShare = async (type: 'copy' | 'email' | 'whatsapp') => {
    const shareText = `Check out ${collegeName} - ${courseName}. Confidence: ${prediction.confidence}. ${extendedPrediction.website || 'Visit college website for more info.'}`
    
    switch (type) {
      case 'copy':
        await navigator.clipboard.writeText(shareText)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
        break
      case 'email':
        window.open(`mailto:?subject=College Recommendation: ${collegeName}&body=${encodeURIComponent(shareText)}`)
        break
      case 'whatsapp':
        window.open(`https://wa.me/?text=${encodeURIComponent(shareText)}`)
        break
    }
    setShowShareMenu(false)
  }

  const toggleFavorite = async () => {
    setIsFavorited(!isFavorited)
    try {
      const uid = 'local-user'
      if (!isFavorited) {
        await api.saveCollege(uid, collegeName)
      }
    } catch (error) {
      console.error('Error saving favorite:', error)
    }
  }

  const toggleCompare = () => {
    if (onToggleCompare) onToggleCompare()
  }

  return (
    <motion.div
      whileHover={{ y: -4, scale: 1.01 }}
      transition={{ duration: 0.3 }}
      className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 hover:shadow-2xl transition-all duration-300 relative overflow-hidden"
    >
      {/* Enhanced Background Pattern */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-blue-50 to-purple-50 rounded-full -mr-16 -mt-16 opacity-50"></div>
      <div className="absolute bottom-0 left-0 w-20 h-20 bg-gradient-to-tr from-green-50 to-blue-50 rounded-full -ml-10 -mb-10 opacity-30"></div>
      
      <div className="relative">
        {/* Enhanced Header Section */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h4 className="text-xl font-bold text-gray-900 leading-tight hover:text-blue-600 transition-colors cursor-pointer">
                {collegeName}
              </h4>
              {extendedPrediction.nirf_rank && (
                <div className="bg-gradient-to-r from-orange-400 to-orange-500 text-white px-2 py-1 rounded-full text-xs font-bold shadow-sm">
                  NIRF #{extendedPrediction.nirf_rank}
                </div>
              )}
              {/* Featured Badge */}
              <div className="bg-gradient-to-r from-yellow-400 to-yellow-500 text-white px-2 py-1 rounded-full text-xs font-bold flex items-center">
                <Star className="w-3 h-3 mr-1" />
                Featured
              </div>
            </div>
            
            <p className="text-lg text-gray-600 mb-3 font-medium">
              {courseName}
            </p>
            
            {/* Enhanced Location and Fees */}
            <div className="space-y-2">
              {(extendedPrediction.location || prediction.country) && (
                <div className="flex items-center text-sm text-gray-500">
                  <MapPin className="w-4 h-4 mr-2 text-gray-400" />
                  <span className="hover:text-gray-700 transition-colors">{extendedPrediction.location || prediction.country}</span>
                </div>
              )}
              
              {extendedPrediction.fees && (
                <div className="flex items-center text-sm text-green-600 font-medium">
                  <span className="w-4 h-4 mr-2 text-green-400">₹</span>
                  <span className="hover:text-green-700 transition-colors">{extendedPrediction.fees}</span>
                </div>
              )}
            </div>
          </div>

            {/* Enhanced Confidence Badge and Actions */}
          <div className="flex flex-col items-end gap-2">
            <div className={`flex items-center px-4 py-2 rounded-full text-sm font-semibold border ${confidenceColor} shadow-sm`}>
              <ConfidenceIcon className="w-4 h-4 mr-2" />
              {(prediction.confidence || (prediction as any).confidence_level || 'Unknown')} Match
            </div>
            
            {/* Quick Actions */}
            <div className="flex items-center gap-1">
              <motion.button
                whileTap={{ scale: 0.95 }}
                onClick={toggleFavorite}
                className={`p-2 rounded-full transition-all duration-200 ${
                  isFavorited 
                    ? 'bg-red-100 text-red-600 hover:bg-red-200' 
                    : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                }`}
                title={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
              >
                <Heart className={`w-4 h-4 ${isFavorited ? 'fill-current' : ''}`} />
              </motion.button>
              
              {compareEnabled && (
                <motion.button
                  whileTap={{ scale: 0.95 }}
                  onClick={toggleCompare}
                  className={`p-2 rounded-full transition-all duration-200 ${
                    isComparing 
                      ? 'bg-blue-100 text-blue-600 hover:bg-blue-200' 
                      : 'bg-gray-100 text-gray-500 hover:bg-gray-200'
                  }`}
                  title={isComparing ? 'Remove from compare' : 'Add to compare'}
                >
                  <BarChart2 className="w-4 h-4" />
                </motion.button>
              )}
              
              <div className="relative">
                <motion.button
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setShowShareMenu(!showShareMenu)}
                  className="p-2 rounded-full bg-gray-100 text-gray-500 hover:bg-gray-200 transition-all duration-200"
                  title="Share college"
                >
                  <Share2 className="w-4 h-4" />
                </motion.button>
                
                {/* Share Menu */}
                {showShareMenu && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.95, y: -10 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    className="absolute right-0 top-12 bg-white rounded-lg shadow-xl border border-gray-200 p-2 z-10 min-w-[120px]"
                  >
                    <button
                      onClick={() => handleShare('copy')}
                      className="flex items-center w-full px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded transition-colors"
                    >
                      <Copy className="w-4 h-4 mr-2" />
                      {copied ? 'Copied!' : 'Copy'}
                    </button>
                    <button
                      onClick={() => handleShare('email')}
                      className="flex items-center w-full px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded transition-colors"
                    >
                      <FileText className="w-4 h-4 mr-2" />
                      Email
                    </button>
                    <button
                      onClick={() => handleShare('whatsapp')}
                      className="flex items-center w-full px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded transition-colors"
                    >
                      <Share2 className="w-4 h-4 mr-2" />
                      WhatsApp
                    </button>
                  </motion.div>
                )}
              </div>
            </div>
              {/* AI Summary Button */}
              <motion.button
                whileTap={{ scale: 0.97 }}
                onClick={async () => {
                  if (aiSummary) { setAiSummary(null); return }
                  try {
                    setAiLoading(true)
                    const res = await api.getAISummary(collegeName)
                    setAiSummary({ overview: res.overview, pros: res.pros || [], cons: res.cons || [], summary: res.summary })
                  } catch (e) {
                    console.error('AI summary failed', e)
                  } finally {
                    setAiLoading(false)
                  }
                }}
                className={`mt-2 px-3 py-1.5 rounded-lg text-xs border ${aiSummary ? 'border-purple-300 bg-purple-50 text-purple-700' : 'border-gray-200 text-gray-700 hover:bg-gray-50'}`}
              >
                {aiLoading ? 'Loading AI…' : aiSummary ? 'Hide AI Summary' : 'AI Summary'}
              </motion.button>
          </div>
        </div>

        {/* Enhanced Stats Grid */}
        <div className="bg-gradient-to-r from-gray-50 to-blue-50 rounded-xl p-4 mb-4 border border-gray-100">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
            {exam === 'ielts' ? (
              <>
                <div className="bg-white rounded-lg p-3 shadow-sm">
                  <div className="text-gray-500 mb-1 font-medium flex items-center">
                    <Info className="w-3 h-3 mr-1" />
                    IELTS Required
                  </div>
                  <div className="font-bold text-gray-900">
                    {prediction.min_ielts && prediction.preferred_ielts ? 
                      `${prediction.min_ielts} - ${prediction.preferred_ielts}` : 
                      prediction.min_ielts ? `${prediction.min_ielts}+` : 'N/A'}
                  </div>
                </div>
                {prediction.acceptance_rate && (
                  <div className="bg-white rounded-lg p-3 shadow-sm">
                    <div className="text-gray-500 mb-1 font-medium flex items-center">
                      <TrendingUp className="w-3 h-3 mr-1" />
                      Acceptance Rate
                    </div>
                    <div className="font-bold text-gray-900">
                      {prediction.acceptance_rate}%
                    </div>
                  </div>
                )}
              </>
            ) : (
              <>
                <div className="bg-white rounded-lg p-3 shadow-sm">
                  <div className="text-gray-500 mb-1 font-medium flex items-center">
                    <BarChart2 className="w-3 h-3 mr-1" />
                    Rank Range
                  </div>
                  <div className="font-bold text-gray-900">
                    {prediction.opening_rank && prediction.closing_rank ?
                      `${prediction.opening_rank.toLocaleString()} - ${prediction.closing_rank.toLocaleString()}` :
                      'N/A'}
                  </div>
                </div>
                
                {prediction.category && (
                  <div className="bg-white rounded-lg p-3 shadow-sm">
                    <div className="text-gray-500 mb-1 font-medium">Category</div>
                    <div className="font-bold text-gray-900">{prediction.category}</div>
                  </div>
                )}
                
                {prediction.quota && (
                  <div className="bg-white rounded-lg p-3 shadow-sm">
                    <div className="text-gray-500 mb-1 font-medium">Quota</div>
                    <div className="font-bold text-gray-900">{prediction.quota}</div>
                  </div>
                )}
                
                {extendedPrediction.nirf_rank && (
                  <div className="bg-white rounded-lg p-3 shadow-sm">
                    <div className="text-gray-500 mb-1 font-medium flex items-center">
                      <Star className="w-3 h-3 mr-1" />
                      NIRF Rank
                    </div>
                    <div className="font-bold text-orange-600">#{extendedPrediction.nirf_rank}</div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>

        {/* Enhanced Links Section */}
        {availableLinks.length > 0 && (
          <div className="border-t border-gray-100 pt-4 mt-4">
            <div className="flex items-center justify-between mb-3">
              <div className="text-sm font-medium text-gray-700 flex items-center">
                <Globe className="w-4 h-4 mr-2" />
                Quick Access Links:
              </div>
              <div className="text-xs text-gray-500">
                {availableLinks.length} available
              </div>
            </div>
            <div className="flex flex-wrap gap-2">
              {availableLinks.map(([key, link]) => {
                const IconComponent = link.icon
                return (
                  <motion.a
                    key={key}
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className={`inline-flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 border ${link.color} shadow-sm hover:shadow-md`}
                  >
                    <IconComponent className="w-4 h-4 mr-2" />
                    {link.name}
                    <ExternalLink className="w-3 h-3 ml-2 opacity-60" />
                  </motion.a>
                )
              })}
            </div>
          </div>
        )}

        {/* Comprehensive All Links Section */}
        <div className="border-t border-gray-100 pt-4 mt-4">
          <div className="flex items-center justify-between mb-3">
            <div className="text-sm font-medium text-gray-700 flex items-center">
              <ExternalLink className="w-4 h-4 mr-2" />
              All College Links:
            </div>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {/* Official Links */}
            <div className="space-y-2">
              <div className="text-xs font-semibold text-gray-600 uppercase tracking-wide">Official</div>
              <a href={extendedPrediction.website} target="_blank" rel="noopener noreferrer" className="block text-xs text-blue-600 hover:text-blue-800 hover:underline">🏛️ Official Website</a>
              <a href={extendedPrediction.brochure} target="_blank" rel="noopener noreferrer" className="block text-xs text-blue-600 hover:text-blue-800 hover:underline">📄 Brochure</a>
              <a href={extendedPrediction.admission_details} target="_blank" rel="noopener noreferrer" className="block text-xs text-blue-600 hover:text-blue-800 hover:underline">📝 Apply Now</a>
            </div>
            
            {/* Academic Links */}
            <div className="space-y-2">
              <div className="text-xs font-semibold text-gray-600 uppercase tracking-wide">Academic</div>
              <a href="https://www.nirfindia.org/2023/EngineeringRanking.html" target="_blank" rel="noopener noreferrer" className="block text-xs text-green-600 hover:text-green-800 hover:underline">🏆 NIRF Ranking</a>
              <a href={`${extendedPrediction.website}/placement`} target="_blank" rel="noopener noreferrer" className="block text-xs text-green-600 hover:text-green-800 hover:underline">📈 Placement Info</a>
              <a href={`${extendedPrediction.website}/facilities`} target="_blank" rel="noopener noreferrer" className="block text-xs text-green-600 hover:text-green-800 hover:underline">🏢 Facilities</a>
            </div>
            
            {/* Student Life */}
            <div className="space-y-2">
              <div className="text-xs font-semibold text-gray-600 uppercase tracking-wide">Student Life</div>
              <a href={`${extendedPrediction.website}/hostel`} target="_blank" rel="noopener noreferrer" className="block text-xs text-purple-600 hover:text-purple-800 hover:underline">🏠 Hostel Info</a>
              <a href={`https://maps.google.com/?q=${encodeURIComponent(collegeName)}`} target="_blank" rel="noopener noreferrer" className="block text-xs text-purple-600 hover:text-purple-800 hover:underline">📍 Location</a>
              <a href={`${extendedPrediction.website}/contact`} target="_blank" rel="noopener noreferrer" className="block text-xs text-purple-600 hover:text-purple-800 hover:underline">📞 Contact</a>
            </div>
            
            {/* Financial */}
            <div className="space-y-2">
              <div className="text-xs font-semibold text-gray-600 uppercase tracking-wide">Financial</div>
              <a href={`${extendedPrediction.website}/fees`} target="_blank" rel="noopener noreferrer" className="block text-xs text-orange-600 hover:text-orange-800 hover:underline">💰 Fee Structure</a>
              <a href={`${extendedPrediction.website}/scholarship`} target="_blank" rel="noopener noreferrer" className="block text-xs text-orange-600 hover:text-orange-800 hover:underline">🎁 Scholarships</a>
              <a href={`${extendedPrediction.website}/payment`} target="_blank" rel="noopener noreferrer" className="block text-xs text-orange-600 hover:text-orange-800 hover:underline">💳 Payment</a>
            </div>
            
            {/* Reviews & Social */}
            <div className="space-y-2">
              <div className="text-xs font-semibold text-gray-600 uppercase tracking-wide">Reviews</div>
              <a href={`https://www.collegedekho.com/colleges/${encodeURIComponent(collegeName.toLowerCase().replace(/\s+/g, '-'))}`} target="_blank" rel="noopener noreferrer" className="block text-xs text-cyan-600 hover:text-cyan-800 hover:underline">💬 Student Reviews</a>
              <a href={`https://www.shiksha.com/college/${encodeURIComponent(collegeName.toLowerCase().replace(/\s+/g, '-'))}`} target="_blank" rel="noopener noreferrer" className="block text-xs text-cyan-600 hover:text-cyan-800 hover:underline">📚 Shiksha Reviews</a>
              <a href={`https://www.careers360.com/colleges/${encodeURIComponent(collegeName.toLowerCase().replace(/\s+/g, '-'))}`} target="_blank" rel="noopener noreferrer" className="block text-xs text-cyan-600 hover:text-cyan-800 hover:underline">🔍 Careers360</a>
            </div>
            
            {/* Additional Resources */}
            <div className="space-y-2">
              <div className="text-xs font-semibold text-gray-600 uppercase tracking-wide">Resources</div>
              <a href={`https://www.google.com/search?q=${encodeURIComponent(collegeName + ' official website')}`} target="_blank" rel="noopener noreferrer" className="block text-xs text-gray-600 hover:text-gray-800 hover:underline">🔍 Google Search</a>
              <a href={`https://www.youtube.com/results?search_query=${encodeURIComponent(collegeName + ' campus tour')}`} target="_blank" rel="noopener noreferrer" className="block text-xs text-gray-600 hover:text-gray-800 hover:underline">📹 YouTube</a>
              <a href={`https://www.linkedin.com/school/${encodeURIComponent(collegeName.toLowerCase().replace(/\s+/g, '-'))}`} target="_blank" rel="noopener noreferrer" className="block text-xs text-gray-600 hover:text-gray-800 hover:underline">💼 LinkedIn</a>
            </div>
          </div>
        </div>

        {/* Expandable Section */}
        <div className="border-t border-gray-100 pt-4 mt-4">
          {aiSummary && (
            <div className="mb-4 bg-gradient-to-r from-violet-50 to-purple-50 border border-purple-200 rounded-lg p-4">
              <h5 className="text-sm font-semibold text-purple-800 mb-2">🤖 AI Summary</h5>
              <p className="text-sm text-gray-700 mb-3">{aiSummary.summary || aiSummary.overview}</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {aiSummary.pros && aiSummary.pros.length > 0 && (
                  <div>
                    <div className="text-xs font-semibold text-green-700 mb-1">Pros</div>
                    <ul className="list-disc list-inside text-xs text-gray-700 space-y-1">
                      {aiSummary.pros.slice(0,5).map((p, i) => (<li key={i}>{p}</li>))}
                    </ul>
                  </div>
                )}
                {aiSummary.cons && aiSummary.cons.length > 0 && (
                  <div>
                    <div className="text-xs font-semibold text-red-700 mb-1">Cons</div>
                    <ul className="list-disc list-inside text-xs text-gray-700 space-y-1">
                      {aiSummary.cons.slice(0,5).map((c, i) => (<li key={i}>{c}</li>))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}
          <motion.button
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center justify-between w-full text-left text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors"
          >
            <span className="flex items-center">
              <Eye className="w-4 h-4 mr-2" />
              {isExpanded ? 'Show Less' : 'View More Details'}
            </span>
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </motion.button>
          
          {isExpanded && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="mt-4 space-y-4"
            >
              {/* Trends Chart */}
              {prediction.college && exam !== 'ielts' && (
                <div className="bg-gray-50 rounded-lg p-4">
                  <h5 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
                    <TrendingUp className="w-4 h-4 mr-2" />
                    Cutoff Trends
                  </h5>
                  <TrendChart collegeName={prediction.college} exam={exam} />
                </div>
              )}
              
              {/* Additional Information */}
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-100">
                <h5 className="text-sm font-medium text-blue-800 mb-2">💡 Pro Tips</h5>
                <ul className="text-xs text-blue-700 space-y-1">
                  <li>• Visit the official website for the most accurate admission requirements</li>
                  <li>• Check application deadlines and required documents</li>
                  <li>• Contact the admissions office for personalized guidance</li>
                  <li>• Consider visiting the campus if possible</li>
                </ul>
              </div>
            </motion.div>
          )}
        </div>

        {/* Enhanced Actions Bar */}
        <div className="flex flex-wrap gap-2 justify-between items-center mt-6 pt-4 border-t border-gray-100">
          <div className="flex flex-wrap gap-2">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-4 py-2 rounded-lg hover:shadow-lg transition-all duration-200 text-sm font-semibold flex items-center"
            >
              <BarChart2 className="w-4 h-4 mr-2" />
              View Trends
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={async () => {
                const uid = 'local-user'
                try {
                  await api.saveCollege(uid, collegeName)
                  alert('✅ College saved to your list!')
                } catch (error) {
                  alert('❌ Error saving college. Please try again.')
                }
              }}
              className="bg-white border-2 border-blue-200 text-blue-700 px-4 py-2 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 text-sm font-semibold flex items-center"
            >
              <Bookmark className="w-4 h-4 mr-2" />
              Save
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={async () => {
                const email = prompt('📧 Enter your email for cutoff alerts:')
                if (email && email.includes('@')) {
                  try {
                    await api.subscribeAlerts(email)
                    alert('🔔 Successfully subscribed to alerts!')
                  } catch (error) {
                    alert('❌ Subscription failed. Please try again.')
                  }
                } else if (email) {
                  alert('❌ Please enter a valid email address.')
                }
              }}
              className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-all duration-200 text-sm font-semibold flex items-center"
            >
              <Bell className="w-4 h-4 mr-2" />
              Get Alerts
            </motion.button>
          </div>
          
          {extendedPrediction.website && (
            <motion.a
              href={extendedPrediction.website}
              target="_blank"
              rel="noopener noreferrer"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-gradient-to-r from-green-600 to-green-700 text-white px-6 py-2 rounded-lg hover:shadow-lg transition-all duration-200 text-sm font-semibold flex items-center"
            >
              <Globe className="w-4 h-4 mr-2" />
              Visit Official Site
              <ExternalLink className="w-3 h-3 ml-2" />
            </motion.a>
          )}
        </div>

        {/* Quick Resources Section */}
        <div className="mt-6 pt-4 border-t border-gray-100">
          {/* Official Website Patterns Section */}
          {resource.official[0].isOfficial && (prediction as any)?.official_links?.website_patterns && (
            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="text-sm font-semibold text-green-800 mb-2">🌐 Official Website Patterns</div>
              <div className="flex flex-wrap gap-2">
                {(prediction as any).official_links.website_patterns.map((url: string, index: number) => (
                  <a 
                    key={index} 
                    href={url} 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="px-3 py-1.5 text-xs bg-green-100 border border-green-300 rounded-lg hover:bg-green-200 text-green-700"
                  >
                    {url.replace('https://', '').replace('www.', '')}
                  </a>
                ))}
              </div>
              <div className="text-xs text-green-600 mt-2">
                These are the most likely official website URLs for this college. Try them to find the actual website.
              </div>
            </div>
          )}
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <div className="text-sm font-semibold text-gray-800 mb-2">Official</div>
              <div className="flex flex-wrap gap-2">
                {resource.official.map((l) => (
                  <a key={l.label} href={l.url} target="_blank" rel="noopener noreferrer" 
                     className={`px-3 py-1.5 text-xs border rounded-lg hover:bg-gray-50 ${
                       l.isOfficial ? 'bg-green-50 border-green-200 text-green-700' : 'bg-gray-50 border-gray-200'
                     }`}>
                    {l.label} {l.isOfficial && '✓'}
                  </a>
                ))}
              </div>
            </div>
            <div>
              <div className="text-sm font-semibold text-gray-800 mb-2">Academic</div>
              <div className="flex flex-wrap gap-2">
                {resource.academic.map((l) => (
                  <a key={l.label} href={l.url} target="_blank" rel="noopener noreferrer" 
                     className="px-3 py-1.5 text-xs border rounded-lg hover:bg-gray-50">
                    {l.label}
                    {l.extraInfo && <span className="ml-1 text-xs text-gray-500">({l.extraInfo})</span>}
                  </a>
                ))}
              </div>
            </div>
            <div>
              <div className="text-sm font-semibold text-gray-800 mb-2">Student Life</div>
              <div className="flex flex-wrap gap-2">
                {resource.studentLife.map((l) => (
                  <a key={l.label} href={l.url} target="_blank" rel="noopener noreferrer" 
                     className="px-3 py-1.5 text-xs border rounded-lg hover:bg-gray-50">
                    {l.label}
                    {l.extraInfo && <span className="ml-1 text-xs text-gray-500">({l.extraInfo})</span>}
                  </a>
                ))}
              </div>
            </div>
            <div>
              <div className="text-sm font-semibold text-gray-800 mb-2">Financial</div>
              <div className="flex flex-wrap gap-2">
                {resource.financial.map((l) => (
                  <a key={l.label} href={l.url} target="_blank" rel="noopener noreferrer" 
                     className="px-3 py-1.5 text-xs border rounded-lg hover:bg-gray-50">
                    {l.label}
                    {l.extraInfo && <span className="ml-1 text-xs text-gray-500">({l.extraInfo})</span>}
                  </a>
                ))}
              </div>
            </div>
            <div>
              <div className="text-sm font-semibold text-gray-800 mb-2">Reviews</div>
              <div className="flex flex-wrap gap-2">
                {resource.reviews.map((l) => (
                  <a key={l.label} href={l.url} target="_blank" rel="noopener noreferrer" 
                     className={`px-3 py-1.5 text-xs border rounded-lg hover:bg-gray-50 ${
                       l.isOfficial ? 'bg-blue-50 border-blue-200 text-blue-700' : 'bg-gray-50 border-gray-200'
                     }`}>
                    {l.label} {l.isOfficial && '✓'}
                  </a>
                ))}
              </div>
            </div>
            <div>
              <div className="text-sm font-semibold text-gray-800 mb-2">Resources</div>
              <div className="flex flex-wrap gap-2">
                {resource.resources.map((l) => (
                  <a key={l.label} href={l.url} target="_blank" rel="noopener noreferrer" 
                     className="px-3 py-1.5 text-xs border rounded-lg hover:bg-gray-50">
                    {l.label}
                  </a>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  )
}
