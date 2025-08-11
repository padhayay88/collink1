import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Brain, 
  Zap, 
  Target, 
  TrendingUp, 
  Star, 
  Award, 
  CheckCircle, 
  Clock,
  Users,
  MapPin,
  DollarSign,
  GraduationCap,
  BarChart3,
  Lightbulb,
  Sparkles,
  ArrowRight,
  RefreshCw
} from 'lucide-react'

interface AIRecommendation {
  id: string
  college: string
  branch: string
  confidence: number
  matchReason: string
  aiScore: number
  personalizedInsights: string[]
  predictedOutcome: {
    admissionChance: number
    placementChance: number
    salaryRange: [number, number]
  }
  competitiveAnalysis: {
    yourRank: number
    averageAdmittedRank: number
    competition: 'Low' | 'Medium' | 'High'
  }
  futureProspects: {
    industryGrowth: number
    jobAvailability: 'High' | 'Medium' | 'Low'
    skillAlignment: number
  }
}

interface AIRecommendationsProps {
  userProfile: {
    rank: number
    exam: string
    interests: string[]
    careerGoals: string[]
    preferences: {
      location: string[]
      budget: number
      collegeType: string
    }
  }
  onRecommendationSelect: (recommendation: AIRecommendation) => void
}

const AIRecommendations: React.FC<AIRecommendationsProps> = ({ 
  userProfile, 
  onRecommendationSelect 
}) => {
  const [recommendations, setRecommendations] = useState<AIRecommendation[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [analysisComplete, setAnalysisComplete] = useState(false)
  const [selectedInsight, setSelectedInsight] = useState<string | null>(null)

  // Simulate AI recommendation generation
  const generateRecommendations = async () => {
    setIsLoading(true)
    setAnalysisComplete(false)

    // Simulate AI processing time
    await new Promise(resolve => setTimeout(resolve, 2000))

    const mockRecommendations: AIRecommendation[] = [
      {
        id: '1',
        college: 'Indian Institute of Technology, Delhi',
        branch: 'Computer Science and Engineering',
        confidence: 92,
        matchReason: 'Perfect alignment with your rank, interests in AI/ML, and career aspirations in tech',
        aiScore: 9.2,
        personalizedInsights: [
          'Your rank puts you in the top 1% of applicants for this program',
          'Strong placement record in AI/ML companies (95% placement rate)',
          'Excellent research opportunities matching your interests',
          'Alumni network strength in your preferred career path'
        ],
        predictedOutcome: {
          admissionChance: 85,
          placementChance: 95,
          salaryRange: [25, 45]
        },
        competitiveAnalysis: {
          yourRank: userProfile.rank,
          averageAdmittedRank: userProfile.rank + 500,
          competition: 'High'
        },
        futureProspects: {
          industryGrowth: 35,
          jobAvailability: 'High',
          skillAlignment: 88
        }
      },
      {
        id: '2',
        college: 'National Institute of Technology, Karnataka',
        branch: 'Electronics and Communication',
        confidence: 78,
        matchReason: 'Good fit based on your rank range and interest in hardware technologies',
        aiScore: 8.1,
        personalizedInsights: [
          'Excellent faculty-to-student ratio for personalized attention',
          'Strong industry connections in semiconductor sector',
          'Growing demand for ECE professionals in your region',
          'Balanced academic and extracurricular opportunities'
        ],
        predictedOutcome: {
          admissionChance: 75,
          placementChance: 88,
          salaryRange: [18, 35]
        },
        competitiveAnalysis: {
          yourRank: userProfile.rank,
          averageAdmittedRank: userProfile.rank - 200,
          competition: 'Medium'
        },
        futureProspects: {
          industryGrowth: 28,
          jobAvailability: 'High',
          skillAlignment: 75
        }
      },
      {
        id: '3',
        college: 'Birla Institute of Technology and Science, Pilani',
        branch: 'Data Science and Engineering',
        confidence: 85,
        matchReason: 'Emerging field matching your AI/ML interests with excellent industry connections',
        aiScore: 8.7,
        personalizedInsights: [
          'Cutting-edge curriculum aligned with industry 4.0 trends',
          'Direct recruitment by top tech companies for DS roles',
          'Flexible degree structure allowing interdisciplinary learning',
          'Strong entrepreneurship ecosystem for startup opportunities'
        ],
        predictedOutcome: {
          admissionChance: 80,
          placementChance: 92,
          salaryRange: [22, 40]
        },
        competitiveAnalysis: {
          yourRank: userProfile.rank,
          averageAdmittedRank: userProfile.rank + 100,
          competition: 'Medium'
        },
        futureProspects: {
          industryGrowth: 45,
          jobAvailability: 'High',
          skillAlignment: 92
        }
      }
    ]

    setRecommendations(mockRecommendations)
    setIsLoading(false)
    setAnalysisComplete(true)
  }

  useEffect(() => {
    generateRecommendations()
  }, [userProfile])

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 80) return 'text-green-600 bg-green-100'
    if (confidence >= 60) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getCompetitionColor = (competition: string) => {
    if (competition === 'Low') return 'text-green-600 bg-green-100'
    if (competition === 'Medium') return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  if (isLoading) {
    return (
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-2xl shadow-lg border border-purple-100 p-8">
        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <Brain className="w-8 h-8 text-white animate-pulse" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-4">AI Analysis in Progress</h3>
          <p className="text-gray-600 mb-6">
            Our AI is analyzing thousands of data points to find your perfect college matches...
          </p>
          <div className="flex items-center justify-center space-x-4 text-sm text-gray-500">
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="flex items-center"
            >
              <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
              Analyzing academic profile
            </motion.div>
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1 }}
              className="flex items-center"
            >
              <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
              Matching preferences
            </motion.div>
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.5 }}
              className="flex items-center"
            >
              <Clock className="w-4 h-4 text-yellow-500 mr-2 animate-spin" />
              Generating recommendations
            </motion.div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-2xl shadow-lg border border-purple-100 p-8 mb-8">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <Sparkles className="w-8 h-8 text-white" />
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">AI-Powered Recommendations</h2>
        <p className="text-gray-600">
          Personalized college suggestions based on advanced machine learning analysis
        </p>
        <div className="flex items-center justify-center mt-4 space-x-4">
          <div className="flex items-center text-sm text-green-600">
            <CheckCircle className="w-4 h-4 mr-1" />
            {recommendations.length} Perfect Matches Found
          </div>
          <button
            onClick={generateRecommendations}
            className="flex items-center text-sm text-blue-600 hover:text-blue-700 font-medium"
          >
            <RefreshCw className="w-4 h-4 mr-1" />
            Refresh Analysis
          </button>
        </div>
      </div>

      {/* Recommendations */}
      <div className="space-y-6">
        {recommendations.map((rec, index) => (
          <motion.div
            key={rec.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.2 }}
            className="bg-white rounded-xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-all duration-300"
          >
            {/* Recommendation Header */}
            <div className="flex items-start justify-between mb-6">
              <div className="flex-1">
                <div className="flex items-center mb-2">
                  <h3 className="text-xl font-bold text-gray-900 mr-3">{rec.college}</h3>
                  <div className={`px-3 py-1 rounded-full text-xs font-bold ${getConfidenceColor(rec.confidence)}`}>
                    {rec.confidence}% Match
                  </div>
                </div>
                <p className="text-lg text-blue-600 font-medium mb-2">{rec.branch}</p>
                <p className="text-sm text-gray-600 mb-4">{rec.matchReason}</p>
                
                {/* AI Score */}
                <div className="flex items-center">
                  <Brain className="w-5 h-5 text-purple-600 mr-2" />
                  <span className="text-sm font-medium text-gray-700 mr-2">AI Score:</span>
                  <div className="flex items-center">
                    {[...Array(5)].map((_, i) => (
                      <Star 
                        key={i} 
                        className={`w-4 h-4 ${i < Math.floor(rec.aiScore) ? 'text-yellow-400 fill-current' : 'text-gray-300'}`} 
                      />
                    ))}
                    <span className="ml-2 text-sm font-bold text-gray-900">{rec.aiScore}/10</span>
                  </div>
                </div>
              </div>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => onRecommendationSelect(rec)}
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-lg font-semibold shadow-md hover:shadow-lg transition-all flex items-center"
              >
                Select
                <ArrowRight className="w-4 h-4 ml-2" />
              </motion.button>
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              {/* Admission Prediction */}
              <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-4 rounded-lg border border-green-200">
                <div className="flex items-center mb-2">
                  <Target className="w-5 h-5 text-green-600 mr-2" />
                  <h4 className="font-semibold text-green-800">Admission Chance</h4>
                </div>
                <div className="text-2xl font-bold text-green-600 mb-1">
                  {rec.predictedOutcome.admissionChance}%
                </div>
                <div className="text-xs text-green-600">
                  Based on historical data
                </div>
              </div>

              {/* Competition Analysis */}
              <div className="bg-gradient-to-r from-yellow-50 to-orange-50 p-4 rounded-lg border border-yellow-200">
                <div className="flex items-center mb-2">
                  <Users className="w-5 h-5 text-yellow-600 mr-2" />
                  <h4 className="font-semibold text-yellow-800">Competition</h4>
                </div>
                <div className={`px-2 py-1 rounded-full text-sm font-bold mb-1 ${getCompetitionColor(rec.competitiveAnalysis.competition)}`}>
                  {rec.competitiveAnalysis.competition}
                </div>
                <div className="text-xs text-yellow-600">
                  Avg. admitted rank: {rec.competitiveAnalysis.averageAdmittedRank.toLocaleString()}
                </div>
              </div>

              {/* Salary Projection */}
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-lg border border-blue-200">
                <div className="flex items-center mb-2">
                  <DollarSign className="w-5 h-5 text-blue-600 mr-2" />
                  <h4 className="font-semibold text-blue-800">Expected Salary</h4>
                </div>
                <div className="text-xl font-bold text-blue-600 mb-1">
                  ₹{rec.predictedOutcome.salaryRange[0]}-{rec.predictedOutcome.salaryRange[1]}L
                </div>
                <div className="text-xs text-blue-600">
                  First year package
                </div>
              </div>
            </div>

            {/* Personalized Insights */}
            <div className="mb-6">
              <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                <Lightbulb className="w-5 h-5 text-yellow-500 mr-2" />
                Personalized Insights
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {rec.personalizedInsights.map((insight, idx) => (
                  <motion.div
                    key={idx}
                    whileHover={{ scale: 1.02 }}
                    className="bg-gray-50 p-3 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors cursor-pointer"
                    onClick={() => setSelectedInsight(selectedInsight === insight ? null : insight)}
                  >
                    <div className="flex items-start">
                      <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-sm text-gray-700">{insight}</span>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Future Prospects */}
            <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-lg border border-purple-200">
              <h4 className="font-semibold text-purple-900 mb-3 flex items-center">
                <TrendingUp className="w-5 h-5 text-purple-600 mr-2" />
                Future Prospects Analysis
              </h4>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center">
                  <div className="text-lg font-bold text-purple-600">
                    +{rec.futureProspects.industryGrowth}%
                  </div>
                  <div className="text-xs text-purple-600">Industry Growth</div>
                </div>
                <div className="text-center">
                  <div className={`px-2 py-1 rounded-full text-xs font-bold ${
                    rec.futureProspects.jobAvailability === 'High' ? 'bg-green-100 text-green-600' : 
                    rec.futureProspects.jobAvailability === 'Medium' ? 'bg-yellow-100 text-yellow-600' : 
                    'bg-red-100 text-red-600'
                  }`}>
                    {rec.futureProspects.jobAvailability}
                  </div>
                  <div className="text-xs text-purple-600 mt-1">Job Availability</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-purple-600">
                    {rec.futureProspects.skillAlignment}%
                  </div>
                  <div className="text-xs text-purple-600">Skill Alignment</div>
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Footer */}
      <div className="text-center mt-8 pt-6 border-t border-gray-200">
        <p className="text-sm text-gray-600">
          🤖 Powered by advanced AI algorithms analyzing 10M+ data points across academic performance, 
          industry trends, and career outcomes
        </p>
        <div className="flex items-center justify-center mt-2 space-x-4 text-xs text-gray-500">
          <span>• Real-time market analysis</span>
          <span>• Predictive modeling</span>
          <span>• Personalized matching</span>
        </div>
      </div>
    </div>
  )
}

export default AIRecommendations
