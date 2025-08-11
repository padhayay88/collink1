import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL
  ? `${process.env.NEXT_PUBLIC_API_URL}/api/v1`
  : 'http://localhost:8000/api/v1'

// Types
export interface Prediction {
  college: string
  branch?: string
  course?: string
  university?: string
  country?: string
  opening_rank?: number
  closing_rank?: number
  min_ielts?: number
  preferred_ielts?: number
  confidence?: string
  confidence_level?: string
  category?: string
  quota?: string
  acceptance_rate?: number
}

export interface PredictionResponse {
  exam: string
  rank: number
  category: string
  predictions: Prediction[]
  response_time: number
  data_source: string
}

export interface PredictionRequest {
  exam: string
  rank: number
  category: string
  gender?: string
  quota?: string
  tolerance_percent?: number
  states?: string[]
  load_full_data?: boolean
}

export interface CollegeInfo {
  name: string
  overview: string
  established: number
  location: string
  affiliation: string
  nirf_rank: number
  website: string
  contact: {
    phone: string
    email: string
    address: string
  }
  facilities: string[]
  placement_stats: {
    average_package: number
    highest_package: number
    placement_percentage: number
    top_recruiters: string[]
    internship_offers: number
    international_offers: number
  }
  courses_offered: string[]
  ratings: {
    academics: number
    campus: number
    placements: number
    roi: number
    faculty: number
    infrastructure: number
    overall: number
  }
  pros: string[]
  cons: string[]
  fees: {
    tuition_fee: number
    hostel_fee: number
    mess_fee: number
    other_charges: number
    total_annual: number
  }
  admission_criteria: {
    jee_advanced_rank: string
    category_wise: {
      general: string
      obc: string
      sc: string
      st: string
    }
  }
  research_highlights: string[]
  student_life: {
    cultural_fest: string
    technical_fest: string
    sports_facilities: string
    clubs: number
    annual_events: number
  }
}

export interface ExamInfo {
  id: string
  name: string
  description: string
  supported: boolean
}

export interface TrendPoint {
  year: number
  opening_rank?: number
  closing_rank?: number
}

// API Functions
export const api = {
  // Prediction APIs
  async predictColleges(request: PredictionRequest): Promise<PredictionResponse> {
    try {
      const response = await axios.post(`${API_BASE_URL}/predict`, request)
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to get predictions')
    }
  },

  // Combined predictions (multi-exam)
  async predictCombined(payload: { exams: string[]; rank: number; category?: string; gender?: string; quota?: string; tolerance_percent?: number; states?: string[]; limit?: number }): Promise<{ exams: string[]; rank: number; category: string; predictions: any[]; total: number }> {
    try {
      const response = await axios.post(`${API_BASE_URL}/predict/combined`, payload)
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to load combined predictions')
    }
  },

  // Live seat availability (stub)
  async getLiveSeats(params: { exam?: string; state?: string }): Promise<{ exam: string; state?: string; last_updated: string; sources: string[]; colleges: any[] }>{
    const { exam = 'jee', state } = params
    try {
      const response = await axios.get(`${API_BASE_URL}/live-seats`, { params: { exam, state } })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch live seats')
    }
  },

  // Gamification
  async getUserProgress(userId: string): Promise<{ user_id: string; points: number; level: number; badges: string[]; achievements: string[] }>{
    try {
      const response = await axios.get(`${API_BASE_URL}/gamification/${userId}`)
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to get user progress')
    }
  },

  async earnPoints(userId: string, action: string = 'prediction', points: number = 10): Promise<{ status: string; points_earned: number; total_points: number }>{
    try {
      const response = await axios.post(`${API_BASE_URL}/gamification/${userId}/earn`, { action, points })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to earn points')
    }
  },

  async getSamplePredictions(): Promise<any> {
    try {
      const response = await axios.get(`${API_BASE_URL}/predict/sample`)
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to get sample predictions')
    }
  },

  // Features: Trends
  async getRankTrends(collegeName: string, exam: string, years = 5): Promise<{ college: string; exam: string; trends: TrendPoint[] }>{
    try {
      const response = await axios.get(`${API_BASE_URL}/trends`, { params: { college: collegeName, exam, years } })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to get rank trends')
    }
  },

  // Features: AI Summary
  async getAISummary(collegeName: string): Promise<{ name: string; overview: string; pros: string[]; cons: string[]; summary: string }>{
    try {
      const response = await axios.post(`${API_BASE_URL}/ai/summary`, { college_name: collegeName })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to get AI summary')
    }
  },

  // Features: Predict Future
  async predictFuture(payload: { exam: string; current_rank: number; mock_test_scores?: number[]; category?: string; gender?: string; quota?: string }): Promise<any> {
    try {
      const response = await axios.post(`${API_BASE_URL}/predict/future`, payload)
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to predict future colleges')
    }
  },

  // Features: Save / Compare / Alerts
  async saveCollege(userId: string, college: string): Promise<{ status: string; user_id: string; colleges: string[] }>{
    try {
      const response = await axios.post(`${API_BASE_URL}/saves`, { user_id: userId, college })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to save college')
    }
  },

  async listSaved(userId: string): Promise<{ user_id: string; colleges: string[] }>{
    try {
      const response = await axios.get(`${API_BASE_URL}/saves`, { params: { user_id: userId } })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to list saved colleges')
    }
  },

  async compareColleges(colleges: string[]): Promise<{ colleges: Array<{ name: string; location?: string; nirf_rank?: number; fees?: number; average_package?: number; overall_rating?: number }> }>{
    try {
      const response = await axios.post(`${API_BASE_URL}/compare`, { colleges })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to compare colleges')
    }
  },

  async subscribeAlerts(email: string, exam = 'jee'): Promise<{ status: string; email: string; exam: string }>{
    try {
      const response = await axios.post(`${API_BASE_URL}/alerts/subscribe`, { email, exam })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to subscribe to alerts')
    }
  },

  // College APIs
  async getCollegeInfo(collegeName: string): Promise<CollegeInfo> {
    try {
      const response = await axios.get(`${API_BASE_URL}/college/${encodeURIComponent(collegeName)}`)
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to get college information')
    }
  },

  async getAllColleges(params?: { exam?: string; limit?: number }): Promise<{ colleges: CollegeInfo[]; total: number; exam?: string | null }> {
    try {
      const response = await axios.get(`${API_BASE_URL}/colleges`, { params })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to get colleges')
    }
  },

  // Search APIs
  async searchColleges(query: string, filters?: any): Promise<CollegeInfo[]> {
    try {
      const params = new URLSearchParams({ query })
      if (filters) {
        Object.keys(filters).forEach(key => {
          if (filters[key]) {
            params.append(key, filters[key])
          }
        })
      }
      const response = await axios.get(`${API_BASE_URL}/search?${params.toString()}`)
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to search colleges')
    }
  },

  // State + Ownership APIs
  async getSupportedStates(exam: string = 'jee'): Promise<string[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/colleges/states`, { params: { exam } })
      return response.data.states || []
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to get states')
    }
  },

  // Branch browsing (JEE)
  async listJEEBranches(limit: number = 0): Promise<{ exam: string; count: number; branches: string[] }>{
    try {
      const response = await axios.get(`${API_BASE_URL}/colleges/branches`, { params: { exam: 'jee', limit } })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to load branches')
    }
  },

  async getCollegesByBranch(params: { branch: string; rank: number; limit?: number; category?: string }): Promise<{ branch: string; rank: number; total: number; colleges: Array<{ college: string; branch: string; opening_rank?: number; closing_rank?: number; location?: string; category?: string; quota?: string }> }>{
    const { branch, rank, limit = 100, category = 'General' } = params
    try {
      const response = await axios.get(`${API_BASE_URL}/colleges/by-branch`, { params: { branch, rank, limit, category } })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to load colleges for branch')
    }
  },

  async getCollegesByState(params: { state: string; ownership?: 'government' | 'private'; exam?: string; limit?: number }): Promise<{
    state: string
    ownership_filter?: string
    exam: string
    counts: { government: number; private: number; unknown: number }
    colleges: Array<{ name: string; location: string; type: string; exam_type?: string; branch?: string; opening_rank?: number; closing_rank?: number }>
    total: number
  }> {
    const { state, ownership, exam = 'jee', limit = 200 } = params
    try {
      const response = await axios.get(`${API_BASE_URL}/colleges/by-state`, {
        params: { state, ownership, exam, limit }
      })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to get colleges by state')
    }
  },

  // Exam APIs
  async getSupportedExams(): Promise<ExamInfo[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/exams`)
      return response.data.exams
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to get supported exams')
    }
  },

  // Health check
  async healthCheck(): Promise<{ status: string; service: string }> {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`)
      return response.data
    } catch (error: any) {
      throw new Error('API health check failed')
    }
  }
  ,
  // AI Chat
  async aiChat(messages: Array<{ role: 'system' | 'user' | 'assistant'; content: string }>, provider?: 'openai' | 'google' | 'local', model?: string): Promise<{ provider: string; content: string }>{
    try {
      const response = await axios.post(`${API_BASE_URL}/ai/chat`, { messages, provider, model })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'AI chat failed')
    }
  }
}

// Export default for backward compatibility
export default api
