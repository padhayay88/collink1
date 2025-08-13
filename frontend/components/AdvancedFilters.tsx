import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Filter, 
  MapPin, 
  DollarSign, 
  GraduationCap, 
  Star, 
  Users, 
  Calendar,
  Search,
  X,
  ChevronDown,
  Sliders,
  BookOpen,
  Award,
  Building2,
  Zap,
  Target,
  TrendingUp
} from 'lucide-react'

interface FilterState {
  location: string[]
  feeRange: [number, number]
  nirfRank: [number, number]
  courseType: string[]
  collegeType: string[]
  placementRate: [number, number]
  searchQuery: string
  admissionType: string
  accreditation: string[]
  facilities: string[]
}

interface AdvancedFiltersProps {
  onFilterChange: (filters: FilterState) => void
  totalResults: number
}

const AdvancedFilters: React.FC<AdvancedFiltersProps> = ({ onFilterChange, totalResults }) => {
  const [isOpen, setIsOpen] = useState(false)
  const [filters, setFilters] = useState<FilterState>({
    location: [],
    feeRange: [0, 500000],
    nirfRank: [1, 200],
    courseType: [],
    collegeType: [],
    placementRate: [50, 100],
    searchQuery: '',
    admissionType: 'All',
    accreditation: [],
    facilities: []
  })

  const [activeTab, setActiveTab] = useState('location')

  const locations = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow']
  const courseTypes = ['Engineering', 'Medical', 'Management', 'Arts', 'Science', 'Commerce', 'Law', 'Architecture']
  const collegeTypes = ['Government', 'Private', 'Deemed University', 'Autonomous', 'Central University']
  const admissionTypes = ['All', 'Merit Based', 'Entrance Exam', 'Direct Admission', 'Management Quota']
  const accreditations = ['NAAC A++', 'NAAC A+', 'NAAC A', 'NBA Accredited', 'ISO Certified']
  const facilities = ['Hostel', 'Library', 'Labs', 'Sports', 'WiFi', 'Cafeteria', 'Medical', 'Transport']

  const updateFilters = (newFilters: Partial<FilterState>) => {
    const updated = { ...filters, ...newFilters }
    setFilters(updated)
    onFilterChange(updated)
  }

  const clearAllFilters = () => {
    const defaultFilters: FilterState = {
      location: [],
      feeRange: [0, 500000],
      nirfRank: [1, 200],
      courseType: [],
      collegeType: [],
      placementRate: [50, 100],
      searchQuery: '',
      admissionType: 'All',
      accreditation: [],
      facilities: []
    }
    setFilters(defaultFilters)
    onFilterChange(defaultFilters)
  }

  const activeFilterCount = () => {
    let count = 0
    if (filters.location.length > 0) count++
    if (filters.courseType.length > 0) count++
    if (filters.collegeType.length > 0) count++
    if (filters.admissionType !== 'All') count++
    if (filters.accreditation.length > 0) count++
    if (filters.facilities.length > 0) count++
    if (filters.searchQuery) count++
    return count
  }

  const TabButton = ({ id, label, icon: Icon }: { id: string; label: string; icon: React.ComponentType<any> }) => (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={() => setActiveTab(id)}
      className={`flex items-center px-4 py-2 rounded-lg font-medium transition-all ${
        activeTab === id
          ? 'bg-blue-600 text-white shadow-md'
          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
      }`}
    >
      <Icon className="w-4 h-4 mr-2" />
      {label}
    </motion.button>
  )

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-100 mb-6">
      {/* Header */}
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setIsOpen(!isOpen)}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold flex items-center gap-2 shadow-md hover:shadow-lg transition-all"
            >
              <Sliders className="w-5 h-5" />
              Advanced Filters
              {activeFilterCount() > 0 && (
                <span className="bg-white text-blue-600 px-2 py-1 rounded-full text-xs font-bold">
                  {activeFilterCount()}
                </span>
              )}
              <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
            </motion.button>
            
            {/* Search Bar */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search colleges, courses, locations..."
                value={filters.searchQuery}
                onChange={(e) => updateFilters({ searchQuery: e.target.value })}
                className="pl-10 pr-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent w-80 text-sm"
              />
              {filters.searchQuery && (
                <button
                  onClick={() => updateFilters({ searchQuery: '' })}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="text-sm text-gray-600">
              <span className="font-semibold text-blue-600">{totalResults}</span> colleges found
            </div>
            {activeFilterCount() > 0 && (
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={clearAllFilters}
                className="text-red-600 hover:text-red-700 font-medium text-sm flex items-center gap-1"
              >
                <X className="w-4 h-4" />
                Clear All
              </motion.button>
            )}
          </div>
        </div>
      </div>

      {/* Filters Panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="p-6">
              {/* Filter Tabs */}
              <div className="flex flex-wrap gap-2 mb-6 pb-4 border-b border-gray-100">
                <TabButton id="location" label="Location" icon={MapPin} />
                <TabButton id="fees" label="Fees & Ranking" icon={DollarSign} />
                <TabButton id="courses" label="Courses & Type" icon={GraduationCap} />
                <TabButton id="admission" label="Admission" icon={BookOpen} />
                <TabButton id="facilities" label="Facilities" icon={Building2} />
                <TabButton id="advanced" label="Advanced" icon={Zap} />
              </div>

              {/* Filter Content */}
              <AnimatePresence mode="wait">
                <motion.div
                  key={activeTab}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.2 }}
                >
                  {activeTab === 'location' && (
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
                        <MapPin className="w-5 h-5 mr-2 text-blue-600" />
                        Select Locations
                      </h3>
                      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                        {locations.map((location) => (
                          <motion.label
                            key={location}
                            whileHover={{ scale: 1.02 }}
                            className="flex items-center p-3 border border-gray-200 rounded-lg hover:border-blue-300 cursor-pointer transition-colors"
                          >
                            <input
                              type="checkbox"
                              checked={filters.location.includes(location)}
                              onChange={(e) => {
                                const newLocations = e.target.checked
                                  ? [...filters.location, location]
                                  : filters.location.filter(l => l !== location)
                                updateFilters({ location: newLocations })
                              }}
                              className="mr-3 text-blue-600 focus:ring-blue-500"
                            />
                            <span className="text-sm font-medium">{location}</span>
                          </motion.label>
                        ))}
                      </div>
                    </div>
                  )}

                  {activeTab === 'fees' && (
                    <div className="space-y-6">
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
                          <DollarSign className="w-5 h-5 mr-2 text-blue-600" />
                          Annual Fee Range
                        </h3>
                        <div className="bg-gray-50 p-4 rounded-lg">
                          <div className="flex items-center justify-between mb-3">
                            <span className="text-sm text-gray-600">₹{filters.feeRange[0].toLocaleString()}</span>
                            <span className="text-sm text-gray-600">₹{filters.feeRange[1].toLocaleString()}</span>
                          </div>
                          <input
                            type="range"
                            min="0"
                            max="500000"
                            step="10000"
                            value={filters.feeRange[1]}
                            onChange={(e) => updateFilters({ feeRange: [filters.feeRange[0], parseInt(e.target.value)] })}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                          />
                        </div>
                      </div>

                      <div>
                        <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
                          <Star className="w-5 h-5 mr-2 text-orange-500" />
                          NIRF Ranking Range
                        </h3>
                        <div className="bg-gray-50 p-4 rounded-lg">
                          <div className="flex items-center justify-between mb-3">
                            <span className="text-sm text-gray-600">Rank {filters.nirfRank[0]}</span>
                            <span className="text-sm text-gray-600">Rank {filters.nirfRank[1]}</span>
                          </div>
                          <input
                            type="range"
                            min="1"
                            max="200"
                            value={filters.nirfRank[1]}
                            onChange={(e) => updateFilters({ nirfRank: [filters.nirfRank[0], parseInt(e.target.value)] })}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                          />
                        </div>
                      </div>
                    </div>
                  )}

                  {activeTab === 'courses' && (
                    <div className="space-y-6">
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
                          <GraduationCap className="w-5 h-5 mr-2 text-blue-600" />
                          Course Type
                        </h3>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                          {courseTypes.map((course) => (
                            <motion.label
                              key={course}
                              whileHover={{ scale: 1.02 }}
                              className="flex items-center p-3 border border-gray-200 rounded-lg hover:border-blue-300 cursor-pointer transition-colors"
                            >
                              <input
                                type="checkbox"
                                checked={filters.courseType.includes(course)}
                                onChange={(e) => {
                                  const newCourses = e.target.checked
                                    ? [...filters.courseType, course]
                                    : filters.courseType.filter(c => c !== course)
                                  updateFilters({ courseType: newCourses })
                                }}
                                className="mr-3 text-blue-600 focus:ring-blue-500"
                              />
                              <span className="text-sm font-medium">{course}</span>
                            </motion.label>
                          ))}
                        </div>
                      </div>

                      <div>
                        <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
                          <Building2 className="w-5 h-5 mr-2 text-green-600" />
                          College Type
                        </h3>
                        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                          {collegeTypes.map((type) => (
                            <motion.label
                              key={type}
                              whileHover={{ scale: 1.02 }}
                              className="flex items-center p-3 border border-gray-200 rounded-lg hover:border-green-300 cursor-pointer transition-colors"
                            >
                              <input
                                type="checkbox"
                                checked={filters.collegeType.includes(type)}
                                onChange={(e) => {
                                  const newTypes = e.target.checked
                                    ? [...filters.collegeType, type]
                                    : filters.collegeType.filter(t => t !== type)
                                  updateFilters({ collegeType: newTypes })
                                }}
                                className="mr-3 text-green-600 focus:ring-green-500"
                              />
                              <span className="text-sm font-medium">{type}</span>
                            </motion.label>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}

                  {activeTab === 'admission' && (
                    <div className="space-y-6">
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
                          <BookOpen className="w-5 h-5 mr-2 text-blue-600" />
                          Admission Type
                        </h3>
                        <select
                          value={filters.admissionType}
                          onChange={(e) => updateFilters({ admissionType: e.target.value })}
                          className="w-full p-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          {admissionTypes.map((type) => (
                            <option key={type} value={type}>{type}</option>
                          ))}
                        </select>
                      </div>

                      <div>
                        <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
                          <Award className="w-5 h-5 mr-2 text-yellow-600" />
                          Accreditation
                        </h3>
                        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                          {accreditations.map((accred) => (
                            <motion.label
                              key={accred}
                              whileHover={{ scale: 1.02 }}
                              className="flex items-center p-3 border border-gray-200 rounded-lg hover:border-yellow-300 cursor-pointer transition-colors"
                            >
                              <input
                                type="checkbox"
                                checked={filters.accreditation.includes(accred)}
                                onChange={(e) => {
                                  const newAccred = e.target.checked
                                    ? [...filters.accreditation, accred]
                                    : filters.accreditation.filter(a => a !== accred)
                                  updateFilters({ accreditation: newAccred })
                                }}
                                className="mr-3 text-yellow-600 focus:ring-yellow-500"
                              />
                              <span className="text-sm font-medium">{accred}</span>
                            </motion.label>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}

                  {activeTab === 'facilities' && (
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
                        <Building2 className="w-5 h-5 mr-2 text-purple-600" />
                        Campus Facilities
                      </h3>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        {facilities.map((facility) => (
                          <motion.label
                            key={facility}
                            whileHover={{ scale: 1.02 }}
                            className="flex items-center p-3 border border-gray-200 rounded-lg hover:border-purple-300 cursor-pointer transition-colors"
                          >
                            <input
                              type="checkbox"
                              checked={filters.facilities.includes(facility)}
                              onChange={(e) => {
                                const newFacilities = e.target.checked
                                  ? [...filters.facilities, facility]
                                  : filters.facilities.filter(f => f !== facility)
                                updateFilters({ facilities: newFacilities })
                              }}
                              className="mr-3 text-purple-600 focus:ring-purple-500"
                            />
                            <span className="text-sm font-medium">{facility}</span>
                          </motion.label>
                        ))}
                      </div>
                    </div>
                  )}

                  {activeTab === 'advanced' && (
                    <div className="space-y-6">
                      <div>
                        <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
                          <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
                          Placement Rate (%)
                        </h3>
                        <div className="bg-gray-50 p-4 rounded-lg">
                          <div className="flex items-center justify-between mb-3">
                            <span className="text-sm text-gray-600">{filters.placementRate[0]}%</span>
                            <span className="text-sm text-gray-600">{filters.placementRate[1]}%</span>
                          </div>
                          <input
                            type="range"
                            min="50"
                            max="100"
                            value={filters.placementRate[0]}
                            onChange={(e) => updateFilters({ placementRate: [parseInt(e.target.value), filters.placementRate[1]] })}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                          />
                        </div>
                      </div>

                      <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg border border-blue-200">
                        <h4 className="font-semibold text-blue-900 mb-2 flex items-center">
                          <Zap className="w-4 h-4 mr-2" />
                          AI-Powered Recommendations
                        </h4>
                        <p className="text-sm text-blue-700 mb-3">
                          Get personalized college suggestions based on your preferences and profile.
                        </p>
                        <motion.button
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                          className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors flex items-center gap-2"
                        >
                          <Target className="w-4 h-4" />
                          Enable AI Matching
                        </motion.button>
                      </div>
                    </div>
                  )}
                </motion.div>
              </AnimatePresence>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default AdvancedFilters
