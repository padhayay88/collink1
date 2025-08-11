import React, { useState } from 'react'
import Head from 'next/head'
import Header from '../components/Header'
import { motion } from 'framer-motion'
import { Search, Filter, MapPin, TrendingUp, Star, Users, BookOpen } from 'lucide-react'

export default function SearchPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [filters, setFilters] = useState({
    exam: '',
    location: '',
    type: '',
    rating: ''
  })

  const mockColleges = [
    {
      id: 1,
      name: 'Indian Institute of Technology, Bombay',
      location: 'Mumbai, Maharashtra',
      type: 'Government',
      rating: 9.2,
      fees: '₹2.5L/year',
      placement: '₹15L CTC',
      nirf: 3,
      exams: ['JEE Advanced'],
      logo: '/images/iit-bombay.png'
    },
    {
      id: 2,
      name: 'All India Institute of Medical Sciences',
      location: 'New Delhi',
      type: 'Government',
      rating: 9.8,
      fees: '₹1.5L/year',
      placement: '₹12L CTC',
      nirf: 1,
      exams: ['NEET UG'],
      logo: '/images/aiims.png'
    },
    {
      id: 3,
      name: 'Indian Institute of Science',
      location: 'Bangalore, Karnataka',
      type: 'Government',
      rating: 9.5,
      fees: '₹3L/year',
      placement: '₹18L CTC',
      nirf: 1,
      exams: ['JEE Advanced', 'GATE'],
      logo: '/images/iisc.png'
    }
  ]

  const filteredColleges = mockColleges.filter(college =>
    college.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    college.location.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <>
      <Head>
        <title>Search Colleges - Collink</title>
        <meta name="description" content="Search and discover colleges with detailed information about fees, placements, and ratings." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <Header />
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Page Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Search Colleges
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Discover and compare colleges with detailed information about fees, placements, ratings, and more.
            </p>
          </motion.div>

          {/* Search & Filters */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-2xl shadow-xl p-6 mb-8"
          >
            <div className="flex flex-col lg:flex-row gap-4">
              {/* Search Bar */}
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search colleges, locations..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              {/* Filters */}
              <div className="flex flex-wrap lg:flex-nowrap gap-3">
                <select
                  value={filters.exam}
                  onChange={(e) => setFilters({ ...filters, exam: e.target.value })}
                  className="px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">All Exams</option>
                  <option value="jee">JEE Advanced</option>
                  <option value="neet">NEET UG</option>
                  <option value="ielts">IELTS</option>
                </select>

                <select
                  value={filters.type}
                  onChange={(e) => setFilters({ ...filters, type: e.target.value })}
                  className="px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">All Types</option>
                  <option value="government">Government</option>
                  <option value="private">Private</option>
                  <option value="deemed">Deemed University</option>
                </select>

                <button className="flex items-center px-4 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
                  <Filter className="w-4 h-4 mr-2" />
                  More Filters
                </button>
              </div>
            </div>
          </motion.div>

          {/* Results */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-semibold text-gray-900">
                {filteredColleges.length} Colleges Found
              </h2>
              <select className="px-4 py-2 border border-gray-200 rounded-lg">
                <option>Sort by Relevance</option>
                <option>Sort by Rating</option>
                <option>Sort by NIRF Ranking</option>
                <option>Sort by Fees</option>
              </select>
            </div>

            <div className="grid grid-cols-1 gap-6">
              {filteredColleges.map((college, index) => (
                <motion.div
                  key={college.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 p-6 border border-gray-100"
                >
                  <div className="flex flex-col lg:flex-row gap-6">
                    {/* College Logo/Image */}
                    <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold text-xl flex-shrink-0">
                      {college.name.split(' ').map(word => word[0]).join('').slice(0, 3)}
                    </div>

                    {/* College Info */}
                    <div className="flex-1">
                      <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between mb-4">
                        <div>
                          <h3 className="text-xl font-bold text-gray-900 mb-2">
                            {college.name}
                          </h3>
                          <div className="flex items-center text-gray-600 mb-2">
                            <MapPin className="w-4 h-4 mr-2" />
                            <span>{college.location}</span>
                            <span className="mx-2">•</span>
                            <span>{college.type}</span>
                          </div>
                        </div>

                        {/* Rating & NIRF */}
                        <div className="flex items-center space-x-4">
                          <div className="text-center">
                            <div className="flex items-center">
                              <Star className="w-4 h-4 text-yellow-500 mr-1" />
                              <span className="font-semibold">{college.rating}</span>
                            </div>
                            <span className="text-sm text-gray-500">Rating</span>
                          </div>
                          <div className="text-center">
                            <div className="font-semibold">#{college.nirf}</div>
                            <span className="text-sm text-gray-500">NIRF</span>
                          </div>
                        </div>
                      </div>

                      {/* College Stats */}
                      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                        <div>
                          <div className="font-semibold text-gray-900">{college.fees}</div>
                          <span className="text-sm text-gray-500">Fees</span>
                        </div>
                        <div>
                          <div className="font-semibold text-gray-900">{college.placement}</div>
                          <span className="text-sm text-gray-500">Avg. Package</span>
                        </div>
                        <div className="col-span-2">
                          <div className="flex flex-wrap gap-2">
                            {college.exams.map((exam, idx) => (
                              <span
                                key={idx}
                                className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full"
                              >
                                {exam}
                              </span>
                            ))}
                          </div>
                          <span className="text-sm text-gray-500">Entrance Exams</span>
                        </div>
                      </div>

                      {/* Action Buttons */}
                      <div className="flex flex-wrap gap-3">
                        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                          View Details
                        </button>
                        <button className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors">
                          Compare
                        </button>
                        <button className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors">
                          Save
                        </button>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* No Results */}
            {filteredColleges.length === 0 && (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Search className="w-8 h-8 text-gray-400" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  No colleges found
                </h3>
                <p className="text-gray-600">
                  Try adjusting your search terms or filters to find more results.
                </p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </>
  )
}
