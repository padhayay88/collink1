import React, { useState } from 'react'
import Head from 'next/head'
import Header from '../components/Header'
import { motion } from 'framer-motion'
import { MapPin, Star, Users, BookOpen, TrendingUp, Award, DollarSign, Building } from 'lucide-react'

export default function Colleges() {
  const [selectedCategory, setSelectedCategory] = useState('all')

  // Enhanced college data with overview, pros/cons
  const collegeData = [
    {
      id: 1,
      name: 'Indian Institute of Technology, Bombay',
      location: 'Mumbai, Maharashtra',
      type: 'Government',
      category: 'engineering',
      rating: 9.2,
      fees: '₹2.5L/year',
      placement: '₹15L CTC',
      nirf: 3,
      exams: ['JEE Advanced'],
      established: 1958,
      students: 10000,
      faculty: 600,
      overview: 'IIT Bombay is one of the premier engineering institutions in India, known for its excellence in technical education and research. It offers undergraduate, postgraduate, and doctoral programs.',
      pros: [
        'Excellent placement record with top companies',
        'World-class faculty and research facilities',
        'Strong alumni network in Silicon Valley and global companies',
        'Beautiful campus with modern infrastructure',
        'Low fees for high-quality education'
      ],
      cons: [
        'Extremely competitive admission process',
        'High academic pressure and stress',
        'Limited seats available',
        'Mumbai\'s high cost of living'
      ],
      departments: ['Computer Science', 'Electrical Engineering', 'Mechanical Engineering', 'Chemical Engineering'],
      logo: '/images/iit-bombay.png'
    },
    {
      id: 2,
      name: 'All India Institute of Medical Sciences',
      location: 'New Delhi',
      type: 'Government',
      category: 'medical',
      rating: 9.8,
      fees: '₹1.5L/year',
      placement: '₹12L CTC',
      nirf: 1,
      exams: ['NEET UG'],
      established: 1956,
      students: 3000,
      faculty: 800,
      overview: 'AIIMS Delhi is India\'s premier medical institute, providing world-class medical education, research, and patient care. It is known for producing some of the finest doctors in the country.',
      pros: [
        'Best medical education in India',
        'Excellent hospital for clinical training',
        'Highly respected degree globally',
        'Very low fees for quality education',
        'Strong research opportunities'
      ],
      cons: [
        'Extremely difficult to get admission',
        'High academic and work pressure',
        'Limited seats (100 MBBS seats)',
        'Intense competition among students'
      ],
      departments: ['Medicine', 'Surgery', 'Pediatrics', 'Radiology', 'Pathology'],
      logo: '/images/aiims.png'
    },
    {
      id: 3,
      name: 'Harvard University',
      location: 'Cambridge, Massachusetts, USA',
      type: 'Private',
      category: 'international',
      rating: 9.9,
      fees: '$54,000/year',
      placement: '$120,000 CTC',
      nirf: 1,
      exams: ['IELTS', 'SAT'],
      established: 1636,
      students: 23000,
      faculty: 2400,
      overview: 'Harvard University is a prestigious Ivy League institution known for its academic excellence, research, and notable alumni including US presidents and Nobel Prize winners.',
      pros: [
        'World\'s most prestigious university',
        'Excellent research opportunities',
        'Strong global alumni network',
        'Access to world-class resources',
        'High earning potential after graduation'
      ],
      cons: [
        'Extremely expensive tuition and living costs',
        'Highly competitive admission process',
        'High academic pressure',
        'Limited financial aid for international students'
      ],
      departments: ['Business', 'Medicine', 'Law', 'Engineering', 'Liberal Arts'],
      logo: '/images/harvard.png'
    }
  ]

  const categories = [
    { id: 'all', name: 'All Colleges', count: collegeData.length },
    { id: 'engineering', name: 'Engineering', count: collegeData.filter(c => c.category === 'engineering').length },
    { id: 'medical', name: 'Medical', count: collegeData.filter(c => c.category === 'medical').length },
    { id: 'international', name: 'International', count: collegeData.filter(c => c.category === 'international').length },
  ]

  const filteredColleges = selectedCategory === 'all' 
    ? collegeData 
    : collegeData.filter(college => college.category === selectedCategory)

  return (
    <>
      <Head>
        <title>Browse Colleges - Collink</title>
        <meta name="description" content="Browse detailed college information including overview, pros & cons, fees, placements and more." />
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
              Browse Colleges
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Explore detailed information about top colleges including overview, pros & cons, fees, placements and more.
            </p>
          </motion.div>

          {/* Category Filter */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-2xl shadow-xl p-6 mb-8"
          >
            <div className="flex flex-wrap gap-4">
              {categories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
                    selectedCategory === category.id
                      ? 'bg-blue-600 text-white shadow-lg'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {category.name} ({category.count})
                </button>
              ))}
            </div>
          </motion.div>

          {/* Colleges Grid */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="grid grid-cols-1 gap-8"
          >
            {filteredColleges.map((college, index) => (
              <motion.div
                key={college.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden"
              >
                {/* College Header */}
                <div className="p-6 border-b border-gray-100">
                  <div className="flex flex-col lg:flex-row gap-6">
                    {/* Logo */}
                    <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold text-2xl flex-shrink-0">
                      {college.name.split(' ').map(word => word[0]).join('').slice(0, 3)}
                    </div>

                    {/* Basic Info */}
                    <div className="flex-1">
                      <h2 className="text-2xl font-bold text-gray-900 mb-2">
                        {college.name}
                      </h2>
                      <div className="flex flex-wrap items-center gap-4 text-gray-600 mb-4">
                        <div className="flex items-center">
                          <MapPin className="w-4 h-4 mr-2" />
                          <span>{college.location}</span>
                        </div>
                        <div className="flex items-center">
                          <Building className="w-4 h-4 mr-2" />
                          <span>{college.type}</span>
                        </div>
                        <div className="flex items-center">
                          <Users className="w-4 h-4 mr-2" />
                          <span>{college.students.toLocaleString()} Students</span>
                        </div>
                        <div className="flex items-center">
                          <BookOpen className="w-4 h-4 mr-2" />
                          <span>Est. {college.established}</span>
                        </div>
                      </div>

                      {/* Quick Stats */}
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="text-center p-3 bg-gray-50 rounded-lg">
                          <div className="flex items-center justify-center mb-1">
                            <Star className="w-4 h-4 text-yellow-500 mr-1" />
                            <span className="font-bold">{college.rating}</span>
                          </div>
                          <span className="text-sm text-gray-600">Rating</span>
                        </div>
                        <div className="text-center p-3 bg-gray-50 rounded-lg">
                          <div className="font-bold">#{college.nirf}</div>
                          <span className="text-sm text-gray-600">NIRF</span>
                        </div>
                        <div className="text-center p-3 bg-gray-50 rounded-lg">
                          <div className="font-bold">{college.fees}</div>
                          <span className="text-sm text-gray-600">Fees</span>
                        </div>
                        <div className="text-center p-3 bg-gray-50 rounded-lg">
                          <div className="font-bold">{college.placement}</div>
                          <span className="text-sm text-gray-600">Avg Package</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* College Details */}
                <div className="p-6">
                  {/* Overview */}
                  <div className="mb-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">Overview</h3>
                    <p className="text-gray-700 leading-relaxed">{college.overview}</p>
                  </div>

                  {/* Pros & Cons */}
                  <div className="grid md:grid-cols-2 gap-6 mb-6">
                    <div>
                      <h4 className="text-lg font-semibold text-green-800 mb-3 flex items-center">
                        <Award className="w-5 h-5 mr-2" />
                        Pros
                      </h4>
                      <ul className="space-y-2">
                        {college.pros.map((pro, idx) => (
                          <li key={idx} className="flex items-start">
                            <div className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                            <span className="text-gray-700 text-sm">{pro}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h4 className="text-lg font-semibold text-red-800 mb-3 flex items-center">
                        <TrendingUp className="w-5 h-5 mr-2" />
                        Cons
                      </h4>
                      <ul className="space-y-2">
                        {college.cons.map((con, idx) => (
                          <li key={idx} className="flex items-start">
                            <div className="w-2 h-2 bg-red-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                            <span className="text-gray-700 text-sm">{con}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  {/* Departments & Exams */}
                  <div className="grid md:grid-cols-2 gap-6 mb-6">
                    <div>
                      <h4 className="text-lg font-semibold text-gray-900 mb-3">Departments</h4>
                      <div className="flex flex-wrap gap-2">
                        {college.departments.map((dept, idx) => (
                          <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
                            {dept}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <h4 className="text-lg font-semibold text-gray-900 mb-3">Entrance Exams</h4>
                      <div className="flex flex-wrap gap-2">
                        {college.exams.map((exam, idx) => (
                          <span key={idx} className="px-3 py-1 bg-purple-100 text-purple-800 text-sm font-medium rounded-full">
                            {exam}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex flex-wrap gap-3">
                    <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium">
                      Get Prediction
                    </button>
                    <button className="bg-gray-100 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-200 transition-colors font-medium">
                      Compare
                    </button>
                    <button className="bg-gray-100 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-200 transition-colors font-medium">
                      Save to Wishlist
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </>
  )
}
