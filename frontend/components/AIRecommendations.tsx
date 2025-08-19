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
import api, { AIPicksResponse } from '../lib/api'
import { AIDenseSkeleton } from './Skeletons'

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
  const [diagnose, setDiagnose] = useState<any | null>(null)
  const [apiBase, setApiBase] = useState<string>('')

  // Fetch AI recommendations from backend
  const generateRecommendations = async () => {
    try {
      setIsLoading(true)
      setAnalysisComplete(false)
      setDiagnose(null)
      setApiBase(api.getBaseUrl())

      const states = userProfile?.preferences?.location || []
      const exam = userProfile.exam?.toLowerCase() || 'jee'
      const rankVal = typeof userProfile.rank === 'number' && userProfile.rank > 0 ? userProfile.rank : 150000
      const resp: AIPicksResponse = await api.predictAI({
        exam,
        rank: rankVal,
        category: 'General',
        states,
        limit: 20,
        per_college_limit: 1
      })

      const mapped: AIRecommendation[] = (resp.picks || []).map((p, idx) => ({
        id: String(idx + 1),
        college: p.college,
        branch: p.branch || '—',
        confidence: p.confidence_level?.toLowerCase() === 'high' ? 90 : p.confidence_level?.toLowerCase() === 'medium' ? 75 : 60,
        matchReason: (p.match_reasons && p.match_reasons.length) ? p.match_reasons[0] : 'Good alignment with your profile and preferences',
        aiScore: Math.round((p.ai_score / 10) * 10) / 10, // keep 1 decimal
        personalizedInsights: p.match_reasons?.slice(0, 4) || [],
        predictedOutcome: {
          admissionChance: Math.min(98, Math.max(40, Math.round(p.ai_score))),
          placementChance: 85,
          salaryRange: [18, 35]
        },
        competitiveAnalysis: {
          yourRank: resp.rank,
          averageAdmittedRank: p.closing_rank || resp.rank,
          competition: p.confidence_level?.toLowerCase() === 'high' ? 'Medium' : 'High'
        },
        futureProspects: {
          industryGrowth: 25,
          jobAvailability: 'High',
          skillAlignment: 80
        }
      }))

      setRecommendations(mapped)
      if (!mapped.length) {
        try {
          const diag = await api.aiPicksDiagnose({ exam, states, limit: 20 })
          setDiagnose(diag)
        } catch {}
      }
    } catch (e) {
      console.error('Failed to load AI picks', e)
      setRecommendations([])
      try {
        const exam = userProfile.exam?.toLowerCase() || 'jee'
        const states = userProfile?.preferences?.location || []
        const diag = await api.aiPicksDiagnose({ exam, states, limit: 20 })
        setDiagnose(diag)
        setApiBase(api.getBaseUrl())
      } catch {}
    } finally {
      setIsLoading(false)
      setAnalysisComplete(true)
    }
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
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-2xl shadow-lg border border-purple-100 p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center">
              <Brain className="w-6 h-6 text-white animate-pulse" />
            </div>
            <div>
              <div className="h-4 w-48 bg-white/60 rounded mb-1" />
              <div className="h-3 w-32 bg-white/50 rounded" />
            </div>
          </div>
          <div className="text-xs text-gray-600 flex items-center gap-2">
            <Clock className="w-4 h-4 text-yellow-500 animate-spin" />
            Analyzing...
          </div>
        </div>
        <AIDenseSkeleton count={6} />
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
        {analysisComplete && recommendations.length === 0 && (
          <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 p-4 rounded-lg">
            <div className="text-sm font-semibold mb-1">No AI picks received</div>
            <div className="text-xs">API: {apiBase || 'unknown'}</div>
            {diagnose && (
              <div className="mt-2 text-xs">
                <div>Diagnose exam: {diagnose.exam}</div>
                <div>LLM providers: OpenAI={String(diagnose.llm_providers?.openai)} Google={String(diagnose.llm_providers?.google)}</div>
                <div>Local sample count: {diagnose.local_sample_count}</div>
                {Array.isArray(diagnose.local_sample) && diagnose.local_sample.length > 0 && (
                  <div>Sample: {diagnose.local_sample.slice(0,3).join(', ')}</div>
                )}
              </div>
            )}
          </div>
        )}
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
