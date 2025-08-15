import React, { useState } from 'react'
import Head from 'next/head'
import Header from '../components/Header'
import PredictionForm from '../components/PredictionForm'
import CollegeSuggestions from '../components/CollegeSuggestions'
import AIRecommendations from '../components/AIRecommendations'
import { motion } from 'framer-motion'
import { PredictionResponse } from '../lib/api'
import SaveCompareBar from '../components/SaveCompareBar'
import BranchBrowser from '../components/BranchBrowser'
import dynamic from 'next/dynamic'
import CollegeSearch from '../components/CollegeSearch'
import CollegeOverview from '../components/CollegeOverview'

const CollegesAside = dynamic(() => import('../components/CollegesAside'), { ssr: false })

export default function Predict() {
  const [predictionData, setPredictionData] = useState<PredictionResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [activeTab, setActiveTab] = useState<'traditional' | 'ai'>('traditional')
  const [prefs, setPrefs] = useState<{ states: string[]; scope: 'all-india' | 'by-state'; budget?: number }>({ states: [], scope: 'all-india', budget: 0 })

  const handlePrediction = (data: PredictionResponse) => {
    setPredictionData(data)
    setActiveTab('traditional')
  }

  return (
    <>
      <Head>
        <title>College Predictions - Collink</title>
        <meta name="description" content="Get accurate college predictions based on your competitive exam rank." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 relative overflow-hidden">
        {/* Background decoration */}
        <div className="absolute top-0 left-0 w-full h-full opacity-30">
          <div className="absolute top-20 left-10 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl animate-pulse"></div>
          <div className="absolute top-40 right-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl animate-pulse" style={{animationDelay: '2s'}}></div>
          <div className="absolute bottom-20 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl animate-pulse" style={{animationDelay: '4s'}}></div>
        </div>
        
        <div className="relative z-10">
          <Header />
          
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Page Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              College Predictions
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Enter your competitive exam rank and get accurate predictions for colleges that match your profile.
            </p>
          </motion.div>

          {!predictionData ? (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
              {/* Prediction Form */}
              <div className="max-w-lg mx-auto lg:mx-0">
                <PredictionForm 
                  onPrediction={handlePrediction}
                  isLoading={isLoading}
                  onPreferencesChange={(p) => setPrefs(p)}
                />
              </div>

              {/* Welcome Message */}
              <div className="max-w-lg mx-auto lg:mx-0">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-white rounded-2xl shadow-xl p-8 text-center"
                >
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">
                    Get Your Predictions
                  </h3>
                  <p className="text-gray-600 mb-8 text-sm leading-relaxed">
                    Fill out the form on the left to see college predictions based on your rank.
                  </p>
                  <div className="space-y-3">
                    <div className="flex items-center justify-center space-x-3 text-sm text-gray-600">
                      <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                      <span>High Confidence</span>
                    </div>
                    <div className="flex items-center justify-center space-x-3 text-sm text-gray-600">
                      <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                      <span>Medium Confidence</span>
                    </div>
                    <div className="flex items-center justify-center space-x-3 text-sm text-gray-600">
                      <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                      <span>Low Confidence</span>
                    </div>
                  </div>
                </motion.div>
              </div>
            </div>
          ) : (
            <div>
              {/* Form at top for re-prediction */}
              <div className="mb-12">
                <PredictionForm 
                  onPrediction={handlePrediction}
                  isLoading={isLoading}
                />
              </div>

              {/* Results Tabs */}
              <div className="mb-6">
                <div className="inline-flex rounded-lg border border-gray-200 overflow-hidden">
                  <button
                    className={`px-4 py-2 text-sm font-medium ${activeTab === 'traditional' ? 'bg-blue-50 text-blue-700' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
                    onClick={() => setActiveTab('traditional')}
                  >
                    Traditional ({predictionData.predictions.length})
                  </button>
                  <button
                    className={`px-4 py-2 text-sm font-medium border-l border-gray-200 ${activeTab === 'ai' ? 'bg-purple-50 text-purple-700' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
                    onClick={() => setActiveTab('ai')}
                  >
                    AI Picks
                  </button>
                </div>
              </div>

              {activeTab === 'traditional' ? (
                <>
                  {/* Branches first */}
                  <BranchBrowser rank={predictionData.rank} exam={predictionData.exam} />
                  {/* Then colleges list */}
                  <CollegeSuggestions
                    predictions={predictionData.predictions}
                    exam={predictionData.exam || 'jee'}
                    rank={predictionData.rank}
                    category={predictionData.category}
                  />
                </>
              ) : (
                <div className="mt-4">
                  <AIRecommendations
                    userProfile={{
                      rank: predictionData.rank,
                      exam: predictionData.exam,
                      interests: [],
                      careerGoals: [],
                      preferences: { location: prefs.scope === 'by-state' ? prefs.states : [], budget: prefs.budget || 0, collegeType: 'Any' }
                    }}
                    onRecommendationSelect={() => {}}
                  />
                </div>
              )}
            </div>
          )}

          {/* Additional Info */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            <div className="bg-white rounded-2xl p-6 shadow-lg">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">How It Works</h3>
              <p className="text-gray-600 text-sm">
                Our algorithm analyzes your rank against historical cutoff data to provide accurate predictions with confidence scores.
              </p>
            </div>
            
            <div className="bg-white rounded-2xl p-6 shadow-lg">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Real Data</h3>
              <p className="text-gray-600 text-sm">
                All predictions are based on authentic data from official sources like JoSAA, MCC, and university websites.
              </p>
            </div>
            
            <div className="bg-white rounded-2xl p-6 shadow-lg">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Updated 2023</h3>
              <p className="text-gray-600 text-sm">
                We use the latest 2023 cutoff data to ensure the most accurate and up-to-date predictions.
              </p>
            </div>
          </motion.div>

          {/* College Search and Overview */}
          <div className="mt-16">
            <CollegeSearch onSearch={(term) => { /* Implement search handler if needed */ }} />
            <CollegeOverview selectedCollege={null} />
          </div>
          </div>
        </div>
        <SaveCompareBar userId="local-user" />
        <CollegesAside />
      </div>
    </>
  )
}
