import React, { useMemo } from 'react'
import { motion } from 'framer-motion'
import { CheckCircle, AlertTriangle, XCircle, MapPin, TrendingUp, ExternalLink, Save, BarChart2, Bell } from 'lucide-react'
import api, { TrendPoint } from '../lib/api'

interface Prediction {
  college: string
  branch?: string
  course?: string
  university?: string
  country?: string
  opening_rank?: number
  closing_rank?: number
  min_ielts?: number
  preferred_ielts?: number
  confidence: string
  category?: string
  quota?: string
  acceptance_rate?: number
}

interface PredictionResultsProps {
  predictions: Prediction[]
  exam: string
  rank: number
  category: string
}

export default function PredictionResults({ predictions, exam, rank, category }: PredictionResultsProps) {
  const getConfidenceColor = (confidence: string) => {
    switch (confidence.toLowerCase()) {
      case 'high':
        return 'text-green-700 bg-green-100'
      case 'medium':
        return 'text-yellow-700 bg-yellow-100'
      case 'low':
        return 'text-red-700 bg-red-100'
      default:
        return 'text-gray-700 bg-gray-100'
    }
  }

  const getConfidenceIcon = (confidence: string) => {
    switch (confidence.toLowerCase()) {
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
      return `${opening} - ${closing}`
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

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl shadow-xl overflow-hidden"
    >
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6">
        <h2 className="text-2xl font-bold mb-2">Prediction Results</h2>
        <div className="flex flex-wrap gap-4 text-blue-100">
          <span>Exam: {exam.toUpperCase()}</span>
          <span>{exam === 'ielts' ? 'Score' : 'Rank'}: {rank}</span>
          {category && exam !== 'ielts' && <span>Category: {category}</span>}
          <span>Total Results: {predictions.length}</span>
        </div>
      </div>

      {/* Results */}
      <div className="p-6">
        {predictions.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <TrendingUp className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No Predictions Found</h3>
            <p className="text-gray-600">
              Try adjusting your rank or category to get better predictions.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {predictions.map((prediction, index) => {
              const ConfidenceIcon = getConfidenceIcon(prediction.confidence)
              
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow duration-200"
                >
                  <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                    {/* College Info */}
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="text-lg font-bold text-gray-900">
                            {prediction.college || prediction.university}
                          </h3>
                          <p className="text-gray-600">
                            {prediction.branch || prediction.course}
                          </p>
                          {prediction.country && (
                            <div className="flex items-center text-sm text-gray-500 mt-1">
                              <MapPin className="w-4 h-4 mr-1" />
                              {prediction.country}
                            </div>
                          )}
                        </div>

                        {/* Confidence Badge */}
                        <div className={`flex items-center px-3 py-1 rounded-full text-sm font-medium ${getConfidenceColor(prediction.confidence)}`}>
                          <ConfidenceIcon className="w-4 h-4 mr-1" />
                          {prediction.confidence} Confidence
                        </div>
                      </div>

                      {/* Stats Grid */}
                      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
                        {exam === 'ielts' ? (
                          <>
                            <div>
                              <div className="text-gray-500">IELTS Required</div>
                              <div className="font-semibold text-gray-900">
                                {formatIELTSScore(prediction.min_ielts, prediction.preferred_ielts)}
                              </div>
                            </div>
                            {prediction.acceptance_rate && (
                              <div>
                                <div className="text-gray-500">Acceptance Rate</div>
                                <div className="font-semibold text-gray-900">
                                  {prediction.acceptance_rate}%
                                </div>
                              </div>
                            )}
                          </>
                        ) : (
                          <>
                            <div>
                              <div className="text-gray-500">Rank Range</div>
                              <div className="font-semibold text-gray-900">
                                {formatRankRange(prediction.opening_rank, prediction.closing_rank)}
                              </div>
                            </div>
                            {prediction.category && (
                              <div>
                                <div className="text-gray-500">Category</div>
                                <div className="font-semibold text-gray-900">{prediction.category}</div>
                              </div>
                            )}
                            {prediction.quota && (
                              <div>
                                <div className="text-gray-500">Quota</div>
                                <div className="font-semibold text-gray-900">{prediction.quota}</div>
                              </div>
                            )}
                          </>
                        )}
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex flex-wrap gap-2 lg:flex-col lg:items-end">
                      <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium flex items-center">
                        <BarChart2 className="w-4 h-4 mr-1" /> Rank Trends
                      </button>
                      <button className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium flex items-center">
                        <Save className="w-4 h-4 mr-1" /> Save
                      </button>
                      <button className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium flex items-center">
                        <Bell className="w-4 h-4 mr-1" /> Alerts
                      </button>
                      <button className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium flex items-center">
                        <ExternalLink className="w-4 h-4 mr-1" /> Website
                      </button>
                    </div>
                  </div>
                </motion.div>
              )
            })}
          </div>
        )}
      </div>

      {/* Summary */}
      {predictions.length > 0 && (
        <div className="bg-gray-50 p-6 border-t border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="flex items-center">
              <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
              <div>
                <div className="font-medium">High Confidence</div>
                <div className="text-gray-600">
                  {predictions.filter(p => p.confidence.toLowerCase() === 'high').length} colleges
                </div>
              </div>
            </div>
            <div className="flex items-center">
              <AlertTriangle className="w-5 h-5 text-yellow-600 mr-2" />
              <div>
                <div className="font-medium">Medium Confidence</div>
                <div className="text-gray-600">
                  {predictions.filter(p => p.confidence.toLowerCase() === 'medium').length} colleges
                </div>
              </div>
            </div>
            <div className="flex items-center">
              <XCircle className="w-5 h-5 text-red-600 mr-2" />
              <div>
                <div className="font-medium">Low Confidence</div>
                <div className="text-gray-600">
                  {predictions.filter(p => p.confidence.toLowerCase() === 'low').length} colleges
                </div>
              </div>
            </div>
          </div>

          <div className="mt-4 p-3 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-800">
              <strong>Note:</strong> These predictions are based on historical data and trends. 
              Actual cutoffs may vary. Please verify with official sources before making final decisions.
            </p>
          </div>
        </div>
      )}
    </motion.div>
  )
}
