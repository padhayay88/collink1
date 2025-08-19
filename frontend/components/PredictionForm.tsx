import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Calculator, TrendingUp, Users, Globe, Calendar, ClipboardPaste, MapPin, Layers } from 'lucide-react'
import { api } from '../lib/api'
import axios from 'axios'
import toast from 'react-hot-toast'

interface PredictionFormProps {
  onPrediction: (data: any) => void
  isLoading: boolean
  onPreferencesChange?: (prefs: { states: string[]; scope: 'all-india' | 'by-state'; budget?: number; ownership?: 'any' | 'government' | 'private' }) => void
  onLoadingChange?: (loading: boolean) => void
}

export default function PredictionForm({ onPrediction, isLoading, onPreferencesChange, onLoadingChange }: PredictionFormProps) {
  const [formData, setFormData] = useState({
    exam: 'jee',
    rank: '',
    category: 'General',
    gender: 'All',
    quota: 'All India',
    tolerance_percent: 0,
    states: [] as string[],
    scope: 'all-india' as 'all-india' | 'by-state',
    ownership: 'any' as 'any' | 'government' | 'private',
    budget: 0 as number,
    jeeType: 'advanced' as 'advanced' | 'mains'
  })
  const emitPrefs = (next?: Partial<typeof formData>) => {
    const curr = { ...formData, ...(next || {}) }
    onPreferencesChange?.({ states: curr.states, scope: curr.scope, budget: curr.budget || 0, ownership: curr.ownership })
  }

  const [stateOptions, setStateOptions] = useState<string[]>([])
  const [loadingStates, setLoadingStates] = useState(false)

  const ensureStatesLoaded = async () => {
    if (stateOptions.length > 0) return
    setLoadingStates(true)
    try {
      const list = await api.getSupportedStates('jee')
      setStateOptions(list)
    } finally {
      setLoadingStates(false)
    }
  }

  const [loading, setLoading] = useState(false)

  const exams = [
    { id: 'jee', name: 'JEE Exam', icon: Calculator, description: 'Choose between JEE Main and JEE Advanced' },
    { id: 'neet', name: 'NEET UG', icon: Users, description: 'National Eligibility cum Entrance Test' },
    { id: 'ielts', name: 'IELTS', icon: Globe, description: 'International English Language Testing System' },
    { id: 'cat', name: 'MBA (CAT)', icon: Layers, description: 'Find MBA colleges by CAT percentile' }
  ]

  const categories = ['General', 'OBC-NCL', 'SC', 'ST', 'EWS']
  const genders = ['All', 'Male', 'Female']
  const quotas = ['All India', 'Home State', 'Other State']

  // Comprehensive mock data generator with 1.2M rank coverage and detailed links
  const generateMockPredictions = (payload: any) => {
    const rank = payload.rank
    const exam = payload.exam
    const category = payload.category
    
    // Category multiplier for realistic rank calculations
    const getCategoryMultiplier = (cat: string) => {
      switch (cat) {
        case 'General': return 1.0
        case 'EWS': return 0.9
        case 'OBC-NCL': return 0.7
        case 'SC': return 0.5
        case 'ST': return 0.4
        default: return 1.0
      }
    }
    
    const multiplier = getCategoryMultiplier(category)
    const adjustedRank = rank * multiplier
    let mockColleges = []
    
    if (exam === 'jee' || exam === 'JEE Advanced') {
      // Premium IITs - Top Tier (Rank 1-1000)
      if (adjustedRank <= 1000) {
        mockColleges = [
          {
            college: "Indian Institute of Technology, Bombay",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(1 / multiplier),
            closing_rank: Math.floor(67 / multiplier),
            confidence: "High",
            category: category,
            quota: "All India",
            location: "Mumbai, Maharashtra",
            fees: "₹2,50,000/year",
            nirf_rank: 3,
            website: "https://www.iitb.ac.in",
            brochure: "https://www.iitb.ac.in/newacadhome/toacademic.jsp",
            admission_details: "https://www.iitb.ac.in/newacadhome/toacademic.jsp"
          },
          {
            college: "Indian Institute of Technology, Delhi",
            branch: "Electrical Engineering",
            opening_rank: Math.floor(45 / multiplier),
            closing_rank: Math.floor(150 / multiplier),
            confidence: "High",
            category: category,
            quota: "All India",
            location: "New Delhi",
            fees: "₹2,50,000/year",
            nirf_rank: 2,
            website: "https://home.iitd.ac.in",
            brochure: "https://home.iitd.ac.in/academics.php",
            admission_details: "https://jee.iitd.ac.in"
          },
          {
            college: "Indian Institute of Technology, Kanpur",
            branch: "Mechanical Engineering",
            opening_rank: Math.floor(80 / multiplier),
            closing_rank: Math.floor(250 / multiplier),
            confidence: "High",
            category: category,
            quota: "All India",
            location: "Kanpur, Uttar Pradesh",
            fees: "₹2,50,000/year",
            nirf_rank: 4,
            website: "https://www.iitk.ac.in",
            brochure: "https://www.iitk.ac.in/doaa/",
            admission_details: "https://www.iitk.ac.in/doaa/admissions"
          },
          {
            college: "Indian Institute of Technology, Kharagpur",
            branch: "Chemical Engineering",
            opening_rank: Math.floor(200 / multiplier),
            closing_rank: Math.floor(500 / multiplier),
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Kharagpur, West Bengal",
            fees: "₹2,50,000/year",
            nirf_rank: 5,
            website: "http://www.iitkgp.ac.in",
            brochure: "http://www.iitkgp.ac.in/academics",
            admission_details: "http://www.iitkgp.ac.in/admissions"
          },
          {
            college: "Indian Institute of Technology, Madras",
            branch: "Civil Engineering",
            opening_rank: Math.floor(300 / multiplier),
            closing_rank: Math.floor(800 / multiplier),
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Chennai, Tamil Nadu",
            fees: "₹2,50,000/year",
            nirf_rank: 1,
            website: "https://www.iitm.ac.in",
            brochure: "https://www.iitm.ac.in/academics",
            admission_details: "https://www.iitm.ac.in/admissions"
          }
        ]
      } 
      // Good IITs and Top NITs (Rank 1000-5000)
      else if (adjustedRank <= 5000) {
        mockColleges = [
          {
            college: "Indian Institute of Technology, Roorkee",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(500 / multiplier),
            closing_rank: Math.floor(1200 / multiplier),
            confidence: "High",
            category: category,
            quota: "All India",
            location: "Roorkee, Uttarakhand",
            fees: "₹2,50,000/year",
            nirf_rank: 6,
            website: "https://www.iitr.ac.in",
            brochure: "https://www.iitr.ac.in/academics",
            admission_details: "https://www.iitr.ac.in/admissions"
          },
          {
            college: "Indian Institute of Technology, BHU Varanasi",
            branch: "Electronics and Communication",
            opening_rank: Math.floor(800 / multiplier),
            closing_rank: Math.floor(2000 / multiplier),
            confidence: "High",
            category: category,
            quota: "All India",
            location: "Varanasi, Uttar Pradesh",
            fees: "₹2,50,000/year",
            nirf_rank: 11,
            website: "https://www.iitbhu.ac.in",
            brochure: "https://www.iitbhu.ac.in/contents/academics",
            admission_details: "https://www.iitbhu.ac.in/contents/admissions"
          },
          {
            college: "National Institute of Technology, Tiruchirappalli",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(1500 / multiplier),
            closing_rank: Math.floor(3500 / multiplier),
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Tiruchirappalli, Tamil Nadu",
            fees: "₹1,50,000/year",
            nirf_rank: 9,
            website: "https://www.nitt.edu",
            brochure: "https://www.nitt.edu/home/academics/",
            admission_details: "https://www.nitt.edu/home/admissions/"
          },
          {
            college: "National Institute of Technology, Warangal",
            branch: "Electrical Engineering",
            opening_rank: Math.floor(2000 / multiplier),
            closing_rank: Math.floor(4500 / multiplier),
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Warangal, Telangana",
            fees: "₹1,50,000/year",
            nirf_rank: 19,
            website: "https://www.nitw.ac.in",
            brochure: "https://www.nitw.ac.in/main/academics/",
            admission_details: "https://www.nitw.ac.in/main/admissions/"
          }
        ]
      } 
      // Mid-tier IITs and Good NITs (Rank 5000-25000)
      else if (adjustedRank <= 25000) {
        mockColleges = [
          {
            college: "Indian Institute of Technology, Ropar",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(3000 / multiplier),
            closing_rank: Math.floor(8000 / multiplier),
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Ropar, Punjab",
            fees: "₹2,50,000/year",
            nirf_rank: 31,
            website: "https://www.iitrpr.ac.in",
            brochure: "https://www.iitrpr.ac.in/academics",
            admission_details: "https://www.iitrpr.ac.in/admissions"
          },
          {
            college: "National Institute of Technology, Karnataka",
            branch: "Electronics and Communication",
            opening_rank: Math.floor(4000 / multiplier),
            closing_rank: Math.floor(10000 / multiplier),
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Surathkal, Karnataka",
            fees: "₹1,50,000/year",
            nirf_rank: 13,
            website: "https://www.nitk.ac.in",
            brochure: "https://www.nitk.ac.in/academics",
            admission_details: "https://www.nitk.ac.in/admissions"
          },
          {
            college: "National Institute of Technology, Calicut",
            branch: "Mechanical Engineering",
            opening_rank: Math.floor(5000 / multiplier),
            closing_rank: Math.floor(12000 / multiplier),
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Calicut, Kerala",
            fees: "₹1,35,000/year",
            nirf_rank: 23,
            website: "https://www.nitc.ac.in",
            brochure: "https://www.nitc.ac.in/academics",
            admission_details: "https://www.nitc.ac.in/admissions"
          },
          {
            college: "Birla Institute of Technology and Science, Pilani",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(8000 / multiplier),
            closing_rank: Math.floor(15000 / multiplier),
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Pilani, Rajasthan",
            fees: "₹4,50,000/year",
            nirf_rank: 30,
            website: "https://www.bits-pilani.ac.in",
            brochure: "https://www.bits-pilani.ac.in/academics/",
            admission_details: "https://www.bitsadmission.com"
          },
          {
            college: "Delhi Technological University",
            branch: "Computer Engineering",
            opening_rank: Math.floor(12000 / multiplier),
            closing_rank: Math.floor(20000 / multiplier),
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Delhi",
            fees: "₹80,000/year",
            nirf_rank: 58,
            website: "http://www.dtu.ac.in",
            brochure: "http://www.dtu.ac.in/academics/",
            admission_details: "http://www.dtu.ac.in/admissions/"
          }
        ]
      }
      // Lower NITs and Good State Colleges (Rank 25000-100000)
      else if (adjustedRank <= 100000) {
        mockColleges = [
          {
            college: "National Institute of Technology, Jaipur",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(25000 / multiplier),
            closing_rank: Math.floor(45000 / multiplier),
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Jaipur, Rajasthan",
            fees: "₹1,50,000/year",
            nirf_rank: 37,
            website: "https://www.mnit.ac.in",
            brochure: "https://www.mnit.ac.in/academics/",
            admission_details: "https://www.mnit.ac.in/admissions/"
          },
          {
            college: "National Institute of Technology, Bhopal",
            branch: "Electronics and Communication",
            opening_rank: Math.floor(30000 / multiplier),
            closing_rank: Math.floor(55000 / multiplier),
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Bhopal, Madhya Pradesh",
            fees: "₹1,35,000/year",
            nirf_rank: 65,
            website: "https://www.manit.ac.in",
            brochure: "https://www.manit.ac.in/content/academics",
            admission_details: "https://www.manit.ac.in/content/admissions"
          },
          {
            college: "Jadavpur University",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(35000 / multiplier),
            closing_rank: Math.floor(60000 / multiplier),
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Kolkata, West Bengal",
            fees: "₹25,000/year",
            nirf_rank: 12,
            website: "http://www.jaduniv.edu.in",
            brochure: "http://www.jaduniv.edu.in/academics.php",
            admission_details: "http://www.jaduniv.edu.in/view_department.php?deptid=97"
          },
          {
            college: "Vellore Institute of Technology",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(40000 / multiplier),
            closing_rank: Math.floor(80000 / multiplier),
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Vellore, Tamil Nadu",
            fees: "₹1,98,000/year",
            nirf_rank: 11,
            website: "https://vit.ac.in",
            brochure: "https://vit.ac.in/academics",
            admission_details: "https://viteee.vit.ac.in"
          },
          {
            college: "Manipal Institute of Technology",
            branch: "Information Technology",
            opening_rank: Math.floor(45000 / multiplier),
            closing_rank: Math.floor(90000 / multiplier),
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Manipal, Karnataka",
            fees: "₹3,45,000/year",
            nirf_rank: 45,
            website: "https://manipal.edu",
            brochure: "https://manipal.edu/mit/academics.html",
            admission_details: "https://manipal.edu/mu/admission.html"
          }
        ]
      }
      // State Universities and Private Colleges (Rank 100000-500000)
      else if (adjustedRank <= 500000) {
        mockColleges = [
          {
            college: "PSG College of Technology",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(100000 / multiplier),
            closing_rank: Math.floor(200000 / multiplier),
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Coimbatore, Tamil Nadu",
            fees: "₹85,000/year",
            nirf_rank: 52,
            website: "https://www.psgtech.edu",
            brochure: "https://www.psgtech.edu/academics.html",
            admission_details: "https://www.psgtech.edu/admissions.html"
          },
          {
            college: "SSN College of Engineering",
            branch: "Electronics and Communication",
            opening_rank: Math.floor(120000 / multiplier),
            closing_rank: Math.floor(250000 / multiplier),
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Chennai, Tamil Nadu",
            fees: "₹1,50,000/year",
            nirf_rank: 67,
            website: "https://www.ssn.edu.in",
            brochure: "https://www.ssn.edu.in/academics/",
            admission_details: "https://www.ssn.edu.in/admissions/"
          },
          {
            college: "SRM Institute of Science and Technology",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(150000 / multiplier),
            closing_rank: Math.floor(300000 / multiplier),
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Kattankulathur, Tamil Nadu",
            fees: "₹2,50,000/year",
            nirf_rank: 41,
            website: "https://www.srmist.edu.in",
            brochure: "https://www.srmist.edu.in/academics/",
            admission_details: "https://www.srmist.edu.in/admissions/"
          },
          {
            college: "Amity University",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(200000 / multiplier),
            closing_rank: Math.floor(400000 / multiplier),
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Noida, Uttar Pradesh",
            fees: "₹3,24,000/year",
            nirf_rank: 85,
            website: "https://www.amity.edu",
            brochure: "https://www.amity.edu/academics/",
            admission_details: "https://www.amity.edu/admissions/"
          },
          {
            college: "Lovely Professional University",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(250000 / multiplier),
            closing_rank: Math.floor(500000 / multiplier),
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Phagwara, Punjab",
            fees: "₹1,60,000/year",
            nirf_rank: 78,
            website: "https://www.lpu.in",
            brochure: "https://www.lpu.in/academics.php",
            admission_details: "https://www.lpu.in/admissions/"
          }
        ]
      }
      // Private and Regional Colleges (Rank 500000-1200000)
      else if (adjustedRank <= 1200000) {
        mockColleges = [
          {
            college: "Chandigarh University",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(500000 / multiplier),
            closing_rank: Math.floor(800000 / multiplier),
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Mohali, Punjab",
            fees: "₹1,60,000/year",
            nirf_rank: 95,
            website: "https://www.cuchd.in",
            brochure: "https://www.cuchd.in/academics/",
            admission_details: "https://www.cuchd.in/admissions/"
          },
          {
            college: "Bennett University",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(600000 / multiplier),
            closing_rank: Math.floor(900000 / multiplier),
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Greater Noida, Uttar Pradesh",
            fees: "₹2,95,000/year",
            nirf_rank: 98,
            website: "https://www.bennett.edu.in",
            brochure: "https://www.bennett.edu.in/academics/",
            admission_details: "https://www.bennett.edu.in/admissions/"
          },
          {
            college: "Galgotias University",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(700000 / multiplier),
            closing_rank: Math.floor(1000000 / multiplier),
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Greater Noida, Uttar Pradesh",
            fees: "₹1,45,000/year",
            nirf_rank: 87,
            website: "https://www.galgotiasuniversity.edu.in",
            brochure: "https://www.galgotiasuniversity.edu.in/academics/",
            admission_details: "https://www.galgotiasuniversity.edu.in/admissions/"
          },
          {
            college: "Sharda University",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(800000 / multiplier),
            closing_rank: Math.floor(1100000 / multiplier),
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Greater Noida, Uttar Pradesh",
            fees: "₹1,86,000/year",
            nirf_rank: 89,
            website: "https://www.sharda.ac.in",
            brochure: "https://www.sharda.ac.in/academics/",
            admission_details: "https://www.sharda.ac.in/admissions/"
          },
          {
            college: "Graphic Era Hill University",
            branch: "Computer Science and Engineering",
            opening_rank: Math.floor(900000 / multiplier),
            closing_rank: Math.floor(1200000 / multiplier),
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Dehradun, Uttarakhand",
            fees: "₹1,25,000/year",
            nirf_rank: 92,
            website: "https://www.gehu.ac.in",
            brochure: "https://www.gehu.ac.in/academics/",
            admission_details: "https://www.gehu.ac.in/admissions/"
          }
        ]
      }
    } else if (exam === 'neet') {
      // NEET comprehensive college database
      if (adjustedRank <= 100) {
        mockColleges = [
          {
            college: "All India Institute of Medical Sciences, New Delhi",
            course: "MBBS",
            opening_rank: 1,
            closing_rank: 50,
            confidence: "High",
            category: category,
            quota: "All India",
            location: "New Delhi",
            fees: "₹1,663/year",
            website: "https://www.aiims.edu",
            brochure: "https://www.aiimsexams.ac.in/",
            admission_details: "https://www.aiimsexams.ac.in/"
          },
          {
            college: "Postgraduate Institute of Medical Education and Research",
            course: "MBBS",
            opening_rank: 45,
            closing_rank: 90,
            confidence: "High",
            category: category,
            quota: "All India",
            location: "Chandigarh",
            fees: "₹4,600/year",
            website: "https://www.pgimer.edu.in",
            brochure: "https://www.pgimer.edu.in/PGIMER_PORTAL/PGIMERPORTAL/GlobalPages/index.jsp",
            admission_details: "https://www.pgimer.edu.in/PGIMER_PORTAL/PGIMERPORTAL/home.jsp"
          }
        ]
      }
      else if (adjustedRank <= 1000) {
        mockColleges = [
          {
            college: "Christian Medical College, Vellore",
            course: "MBBS",
            opening_rank: 100,
            closing_rank: 500,
            confidence: "High",
            category: category,
            quota: "All India",
            location: "Vellore, Tamil Nadu",
            fees: "₹90,000/year",
            website: "https://www.cmch-vellore.edu",
            brochure: "https://www.cmch-vellore.edu/admissions/",
            admission_details: "https://www.cmch-vellore.edu/web/admissions"
          },
          {
            college: "Armed Forces Medical College",
            course: "MBBS",
            opening_rank: 200,
            closing_rank: 800,
            confidence: "High",
            category: category,
            quota: "All India",
            location: "Pune, Maharashtra",
            fees: "₹50,000/year",
            website: "https://afmc.nic.in",
            brochure: "https://afmc.nic.in/admission.htm",
            admission_details: "https://afmc.nic.in/neet.htm"
          }
        ]
      }
      else if (adjustedRank <= 10000) {
        mockColleges = [
          {
            college: "King George's Medical University",
            course: "MBBS",
            opening_rank: 1000,
            closing_rank: 5000,
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Lucknow, Uttar Pradesh",
            fees: "₹67,000/year",
            website: "https://www.kgmu.org",
            brochure: "https://www.kgmu.org/academic_section.htm",
            admission_details: "https://www.kgmu.org/admission.htm"
          },
          {
            college: "Maulana Azad Medical College",
            course: "MBBS",
            opening_rank: 2000,
            closing_rank: 8000,
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "New Delhi",
            fees: "₹24,200/year",
            website: "http://mamc.ac.in",
            brochure: "http://mamc.ac.in/academics.php",
            admission_details: "http://mamc.ac.in/admission.php"
          }
        ]
      }
      else if (adjustedRank <= 100000) {
        mockColleges = [
          {
            college: "Kasturba Medical College, Manipal",
            course: "MBBS",
            opening_rank: 10000,
            closing_rank: 50000,
            confidence: "Medium",
            category: category,
            quota: "All India",
            location: "Manipal, Karnataka",
            fees: "₹21,50,000/year",
            website: "https://manipal.edu/kmc-manipal.html",
            brochure: "https://manipal.edu/kmc-manipal/academics.html",
            admission_details: "https://manipal.edu/mu/admission.html"
          },
          {
            college: "JSS Medical College",
            course: "MBBS",
            opening_rank: 20000,
            closing_rank: 80000,
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Mysuru, Karnataka",
            fees: "₹18,75,000/year",
            website: "https://www.jssuni.edu.in",
            brochure: "https://www.jssuni.edu.in/Web/WebContent/Academics.aspx",
            admission_details: "https://www.jssuni.edu.in/Web/WebContent/Admissions.aspx"
          }
        ]
      }
      else if (adjustedRank <= 500000) {
        mockColleges = [
          {
            college: "Saveetha Medical College",
            course: "MBBS",
            opening_rank: 100000,
            closing_rank: 300000,
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Chennai, Tamil Nadu",
            fees: "₹24,50,000/year",
            website: "https://www.saveetha.ac.in",
            brochure: "https://www.saveetha.ac.in/medical/",
            admission_details: "https://www.saveetha.ac.in/admissions/"
          },
          {
            college: "SRM Medical College Hospital and Research Centre",
            course: "MBBS",
            opening_rank: 200000,
            closing_rank: 450000,
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Kattankulathur, Tamil Nadu",
            fees: "₹22,50,000/year",
            website: "https://www.srmist.edu.in",
            brochure: "https://www.srmist.edu.in/medical-college/",
            admission_details: "https://www.srmist.edu.in/admissions/"
          }
        ]
      }
      else if (adjustedRank <= 1200000) {
        mockColleges = [
          {
            college: "Bharath Institute of Higher Education and Research",
            course: "MBBS",
            opening_rank: 500000,
            closing_rank: 900000,
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Chennai, Tamil Nadu",
            fees: "₹25,00,000/year",
            website: "https://www.bharathuniv.ac.in",
            brochure: "https://www.bharathuniv.ac.in/medical-college/",
            admission_details: "https://www.bharathuniv.ac.in/admissions/"
          },
          {
            college: "Kalinga Institute of Medical Sciences",
            course: "MBBS",
            opening_rank: 600000,
            closing_rank: 1100000,
            confidence: "Low",
            category: category,
            quota: "All India",
            location: "Bhubaneswar, Odisha",
            fees: "₹18,90,000/year",
            website: "https://kims.ac.in",
            brochure: "https://kims.ac.in/academics/",
            admission_details: "https://kims.ac.in/admissions/"
          }
        ]
      }
    } else if (exam === 'ielts') {
      // IELTS comprehensive university database
      if (rank >= 8.0) {
        mockColleges = [
          {
            university: "Harvard University",
            course: "Computer Science",
            country: "USA",
            min_ielts: 7.0,
            preferred_ielts: 8.0,
            confidence: "High",
            acceptance_rate: 3,
            website: "https://www.harvard.edu",
            application_link: "https://college.harvard.edu/admissions",
            program_details: "https://www.seas.harvard.edu/computer-science"
          },
          {
            university: "Stanford University",
            course: "Engineering",
            country: "USA",
            min_ielts: 7.0,
            preferred_ielts: 8.0,
            confidence: "High",
            acceptance_rate: 4,
            website: "https://www.stanford.edu",
            application_link: "https://admission.stanford.edu",
            program_details: "https://engineering.stanford.edu"
          },
          {
            university: "University of Oxford",
            course: "Computer Science",
            country: "UK",
            min_ielts: 7.0,
            preferred_ielts: 7.5,
            confidence: "High",
            acceptance_rate: 17,
            website: "https://www.ox.ac.uk",
            application_link: "https://www.ox.ac.uk/admissions",
            program_details: "https://www.cs.ox.ac.uk"
          }
        ]
      }
      else if (rank >= 7.0) {
        mockColleges = [
          {
            university: "University of Toronto",
            course: "Computer Science",
            country: "Canada",
            min_ielts: 6.5,
            preferred_ielts: 7.0,
            confidence: "High",
            acceptance_rate: 43,
            website: "https://www.utoronto.ca",
            application_link: "https://future.utoronto.ca/apply",
            program_details: "https://web.cs.toronto.edu"
          },
          {
            university: "University of British Columbia",
            course: "Engineering",
            country: "Canada",
            min_ielts: 6.5,
            preferred_ielts: 7.0,
            confidence: "High",
            acceptance_rate: 52,
            website: "https://www.ubc.ca",
            application_link: "https://you.ubc.ca/applying-ubc/",
            program_details: "https://engineering.ubc.ca"
          },
          {
            university: "University of Melbourne",
            course: "Information Technology",
            country: "Australia",
            min_ielts: 6.5,
            preferred_ielts: 7.0,
            confidence: "Medium",
            acceptance_rate: 70,
            website: "https://www.unimelb.edu.au",
            application_link: "https://study.unimelb.edu.au/how-to-apply",
            program_details: "https://cis.unimelb.edu.au"
          }
        ]
      }
      else if (rank >= 6.0) {
        mockColleges = [
          {
            university: "University of Sydney",
            course: "Business Administration",
            country: "Australia",
            min_ielts: 6.0,
            preferred_ielts: 6.5,
            confidence: "Medium",
            acceptance_rate: 75,
            website: "https://www.sydney.edu.au",
            application_link: "https://www.sydney.edu.au/study/how-to-apply.html",
            program_details: "https://www.sydney.edu.au/business/"
          },
          {
            university: "Auckland University of Technology",
            course: "Computer Science",
            country: "New Zealand",
            min_ielts: 6.0,
            preferred_ielts: 6.5,
            confidence: "Medium",
            acceptance_rate: 80,
            website: "https://www.aut.ac.nz",
            application_link: "https://www.aut.ac.nz/study/study-options/apply-to-aut",
            program_details: "https://www.aut.ac.nz/study/study-options/engineering-computer-and-mathematical-sciences"
          },
          {
            university: "Ryerson University",
            course: "Engineering",
            country: "Canada",
            min_ielts: 6.5,
            preferred_ielts: 7.0,
            confidence: "Low",
            acceptance_rate: 85,
            website: "https://www.torontomu.ca",
            application_link: "https://www.torontomu.ca/admissions/",
            program_details: "https://www.torontomu.ca/engineering/"
          }
        ]
      }
      else {
        mockColleges = [
          {
            university: "University of Winnipeg",
            course: "General Studies",
            country: "Canada",
            min_ielts: 5.5,
            preferred_ielts: 6.0,
            confidence: "Low",
            acceptance_rate: 90,
            website: "https://www.uwinnipeg.ca",
            application_link: "https://www.uwinnipeg.ca/future-student/",
            program_details: "https://www.uwinnipeg.ca/academics/"
          },
          {
            university: "Southern Cross University",
            course: "Information Technology",
            country: "Australia",
            min_ielts: 5.5,
            preferred_ielts: 6.0,
            confidence: "Low",
            acceptance_rate: 95,
            website: "https://www.scu.edu.au",
            application_link: "https://www.scu.edu.au/study-at-scu/how-to-apply/",
            program_details: "https://www.scu.edu.au/study-at-scu/courses/"
          }
        ]
      }
    }
    
    return {
      exam: payload.exam,
      rank: payload.rank,
      category: payload.category,
      predictions: mockColleges,
      total_colleges: mockColleges.length
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.rank) {
      toast.error('Please enter your rank')
      return
    }

    // Exam-specific basic validation
    if ((formData.exam === 'jee' || formData.exam === 'neet') && parseFloat(formData.rank) <= 0) {
      toast.error('Please enter a valid positive number')
      return
    }

    // Validate IELTS score range
    if (formData.exam === 'ielts' && (parseFloat(formData.rank) < 0 || parseFloat(formData.rank) > 9)) {
      toast.error('IELTS score must be between 0 and 9')
      return
    }
    // Validate CAT percentile range
    if (formData.exam === 'cat' && (parseFloat(formData.rank) < 0 || parseFloat(formData.rank) > 100)) {
      toast.error('CAT percentile must be between 0 and 100')
      return
    }

    setLoading(true)
    onLoadingChange?.(true)

    try {
      // For IELTS, we expect a score instead of rank
      const payload = {
        exam: formData.exam,
        rank: formData.exam === 'ielts' ? parseFloat(formData.rank) : parseInt(formData.rank),
        category: formData.category,
        gender: formData.gender,
        quota: formData.quota,
        tolerance_percent: Number(formData.tolerance_percent) || 0,
        states: formData.scope === 'by-state' ? formData.states : undefined,
        ownership: formData.ownership !== 'any' ? formData.ownership : undefined,
        load_full_data: false,  // Use essential data for faster response
        limit: 300,  // reasonable cap
        per_college_limit: 1
      }

      let predictionData
      try {
        if (formData.exam === 'cat') {
          // CAT percentile flow (Option A): use NIRF-based CSV endpoint
          const percentileVal = parseFloat(formData.rank)
          const data = await api.getMBAByNIRFPercentile({ percentile: percentileVal, limit: 200 })
          const mapped = {
            exam: 'cat',
            rank: percentileVal, // percentile
            predictions: (data.colleges || []).map((c: any) => ({
              college: c.name,
              branch: 'MBA',
              opening_rank: null,
              closing_rank: null,
              category: null,
              quota: null,
              location: c.location ?? null,
              nirf_rank: c.nirf_rank ?? null,
              nirf_score: c.nirf_score ?? null,
              nirf_percentile: c.nirf_percentile ?? null,
              exam_type: 'cat',
              year: null
            })),
            total_colleges: data.total || 0,
            source: data.source
          }
          predictionData = mapped
          toast.success('CAT MBA colleges (NIRF) loaded!')
        } else if (formData.exam === 'combined') {
          // Use combined endpoint for multi-exam predictions
          const combinedPayload = {
            exams: ['jee', 'neet', 'ielts'],
            rank: parseInt(formData.rank),
            category: formData.category,
            gender: formData.gender,
            quota: formData.quota,
            tolerance_percent: Number(formData.tolerance_percent) || 0,
            states: formData.scope === 'by-state' ? formData.states : undefined,
            ownership: formData.ownership !== 'any' ? formData.ownership : undefined,
            limit: 300
          }
          const response = await axios.post('http://localhost:8000/api/v1/predict/combined', combinedPayload)
          predictionData = response.data
          toast.success('Multi-exam predictions loaded!')
        } else {
          const response = await axios.post('http://localhost:8000/api/v1/predict', payload)
          predictionData = response.data
          // Add total_colleges for backward compatibility
          predictionData.total_colleges = predictionData.predictions?.length || 0
          toast.success(`Predictions loaded in ${predictionData.response_time?.toFixed(3)}s!`)
        }
      } catch (apiError) {
        // If API fails, use mock data
        console.log('API not available, using fallback')
        if (formData.exam === 'cat') {
          predictionData = { exam: 'cat', rank: parseFloat(formData.rank), predictions: [], total_colleges: 0 }
          toast.error('CAT endpoint unavailable. Showing no results.')
        } else {
          predictionData = generateMockPredictions(payload)
          toast.success('Showing mock predictions')
        }
      }
      
      onPrediction(predictionData)
    } catch (error: any) {
      console.error('Prediction error:', error)
      toast.error('Failed to get predictions')
    } finally {
      setLoading(false)
    }
  }

  const pasteFromClipboard = async () => {
    try {
      const text = await navigator.clipboard.readText()
      if (!text) return
      const value = formData.exam === 'ielts' ? parseFloat(text) : parseInt(text, 10)
      if (!isNaN(value as any)) {
        setFormData({ ...formData, rank: String(value) })
        toast.success('Pasted from clipboard!')
      }
    } catch (err) {
      // Silently ignore clipboard errors
    }
  }

  const selectedExam = exams.find(e => e.id === formData.exam)

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl shadow-xl p-8"
    >
      {/* Icon and Title */}
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <TrendingUp className="w-8 h-8 text-blue-600" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Get College Predictions</h2>
        <p className="text-gray-600 text-sm">Enter your details to find colleges that match your rank</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Exam Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Select Competitive Exam
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {exams.map((exam) => (
              <button
                key={exam.id}
                type="button"
                onClick={() => setFormData({ ...formData, exam: exam.id })}
                className={`text-left rounded-xl p-4 border transition-all duration-200 h-full ${
                  formData.exam === exam.id
                    ? 'bg-blue-50 border-blue-300 shadow-sm'
                    : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                }`}
              >
                <div className="flex items-start">
                  <exam.icon className={`w-5 h-5 mr-3 mt-0.5 ${formData.exam === exam.id ? 'text-blue-600' : 'text-gray-500'}`} />
                  <div>
                    <div className={`font-semibold ${formData.exam === exam.id ? 'text-blue-900' : 'text-gray-900'}`}>{exam.name}</div>
                    <div className="text-xs text-gray-500 leading-snug">{exam.description}</div>
                  </div>
                </div>
              </button>
            ))}
          </div>
          {/* JEE sub-selection */}
          {formData.exam === 'jee' && (
            <div className="mt-3">
              <label className="block text-xs font-medium text-gray-600 mb-2">Choose JEE Type</label>
              <div className="inline-flex rounded-lg border border-gray-200 overflow-hidden">
                <button
                  type="button"
                  className={`px-3 py-2 text-sm font-medium ${formData.jeeType === 'mains' ? 'bg-blue-50 text-blue-700' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
                  onClick={() => setFormData({ ...formData, jeeType: 'mains' })}
                >
                  JEE Main
                </button>
                <button
                  type="button"
                  className={`px-3 py-2 text-sm font-medium border-l border-gray-200 ${formData.jeeType === 'advanced' ? 'bg-blue-50 text-blue-700' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
                  onClick={() => setFormData({ ...formData, jeeType: 'advanced' })}
                >
                  JEE Advanced
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Scope: All-India vs State-wise */}
        {formData.exam !== 'ielts' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Search Scope</label>
            <div className="flex gap-3">
              <button
                type="button"
                className={`px-3 py-2 rounded-lg border ${formData.scope === 'all-india' ? 'border-blue-500 bg-blue-50 text-blue-700' : 'border-gray-200'}`}
                onClick={() => { const next = { ...formData, scope: 'all-india' as 'all-india' }; setFormData(next); emitPrefs(next) }}
              >All India</button>
              <button
                type="button"
                className={`px-3 py-2 rounded-lg border ${formData.scope === 'by-state' ? 'border-blue-500 bg-blue-50 text-blue-700' : 'border-gray-200'}`}
                onClick={async () => { await ensureStatesLoaded(); const next = { ...formData, scope: 'by-state' as 'by-state' }; setFormData(next); emitPrefs(next) }}
              >Choose States</button>
            </div>
            {formData.scope === 'by-state' && (
              <div className="mt-3">
                <label className="block text-sm text-gray-600 mb-1">Select one or more states</label>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2 max-h-48 overflow-auto border rounded-lg p-2">
                  {loadingStates ? (
                    <div className="col-span-full text-center text-gray-500 py-4">Loading states...</div>
                  ) : (
                    stateOptions.map((st) => {
                      const selected = formData.states.includes(st)
                      return (
                        <button
                          type="button"
                          key={st}
                          onClick={() => {
                            const nextStates = selected ? formData.states.filter(s => s !== st) : [...formData.states, st]
                            const next = { ...formData, states: nextStates }
                            setFormData(next)
                            emitPrefs(next)
                          }}
                          className={`px-2 py-1.5 text-sm rounded border ${selected ? 'border-blue-500 bg-blue-50 text-blue-700' : 'border-gray-200 text-gray-700 hover:bg-gray-50'}`}
                          title={st}
                        >
                          <span className="inline-flex items-center gap-2"><MapPin className="w-3 h-3" /> {st}</span>
                        </button>
                      )
                    })
                  )}
                </div>
                <p className="mt-1 text-xs text-gray-500">If no state is selected, All India is used.</p>

                {/* Ownership filter */}
                <div className="mt-4">
                  <label className="block text-sm text-gray-600 mb-1">Ownership</label>
                  <div className="inline-flex rounded-lg border border-gray-200 overflow-hidden">
                    <button
                      type="button"
                      className={`px-3 py-2 text-sm font-medium ${formData.ownership === 'any' ? 'bg-blue-50 text-blue-700' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
                      onClick={() => { const next = { ...formData, ownership: 'any' as const }; setFormData(next); emitPrefs(next) }}
                    >Any</button>
                    <button
                      type="button"
                      className={`px-3 py-2 text-sm font-medium border-l border-gray-200 ${formData.ownership === 'government' ? 'bg-blue-50 text-blue-700' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
                      onClick={() => { const next = { ...formData, ownership: 'government' as const }; setFormData(next); emitPrefs(next) }}
                    >Government</button>
                    <button
                      type="button"
                      className={`px-3 py-2 text-sm font-medium border-l border-gray-200 ${formData.ownership === 'private' ? 'bg-blue-50 text-blue-700' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
                      onClick={() => { const next = { ...formData, ownership: 'private' as const }; setFormData(next); emitPrefs(next) }}
                    >Private</button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Budget */}
        {formData.exam !== 'ielts' && (
          <div>
            <label htmlFor="budget" className="block text-sm font-medium text-gray-700 mb-2">
              Annual Fee Budget (INR)
            </label>
            <div className="flex items-center gap-3">
              <input
                type="range"
                id="budget"
                min={0}
                max={600000}
                step={10000}
                value={formData.budget}
                onChange={(e) => { const next = { ...formData, budget: Number(e.target.value) }; setFormData(next); emitPrefs(next) }}
                className="w-full"
              />
              <span className="w-28 text-right text-sm text-gray-700">₹{(formData.budget || 0).toLocaleString()}</span>
            </div>
            <p className="mt-1 text-xs text-gray-500">Used by AI Picks to prioritize affordable colleges.</p>
          </div>
        )}

        {/* Rank Input (hidden for BA) */}
        {formData.exam !== 'ba' && (
          <div>
            <label htmlFor="rank" className="block text-sm font-medium text-gray-700 mb-2">
              {formData.exam === 'ielts' 
                ? 'Your IELTS Score' 
                : formData.exam === 'cat'
                  ? 'Your CAT Percentile'
                  : formData.exam === 'jee' && formData.jeeType === 'mains' 
                    ? 'Your JEE Main All India Rank' 
                    : formData.exam === 'jee' && formData.jeeType === 'advanced' 
                      ? 'Your JEE Advanced rank'
                      : 'Your rank'}
            </label>
            <div className="relative">
              <TrendingUp className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="number"
                id="rank"
                value={formData.rank}
                onChange={(e) => setFormData({ ...formData, rank: e.target.value })}
                placeholder={formData.exam === 'ielts' 
                  ? 'e.g., 7.5' 
                  : formData.exam === 'cat'
                    ? 'e.g., 95.5'
                    : formData.exam === 'jee' && formData.jeeType === 'mains' 
                      ? 'e.g., 150000 (AIR)' 
                      : formData.exam === 'jee' && formData.jeeType === 'advanced' 
                        ? 'e.g., 5000' 
                        : 'e.g., 1500'}
                className="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
                min={formData.exam === 'ielts' ? '0' : (formData.exam === 'cat' ? '0' : '1')}
                max={formData.exam === 'ielts' 
                  ? '9' 
                  : formData.exam === 'cat'
                    ? '100'
                    : (formData.exam === 'jee' 
                        ? (formData.jeeType === 'advanced' ? '200000' : '1200000') 
                        : formData.exam === 'neet' 
                          ? '200000' 
                          : undefined)}
                step={formData.exam === 'ielts' || formData.exam === 'cat' ? '0.1' : '1'}
              />
              <button
                type="button"
                onClick={pasteFromClipboard}
                title="Paste from clipboard"
                className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-md text-gray-500 hover:text-gray-700 hover:bg-gray-100"
              >
                <ClipboardPaste className="w-4 h-4" />
              </button>
            </div>
            <p className="mt-1 text-sm text-gray-500">
              {formData.exam === 'ielts' 
                ? 'Enter your overall IELTS score (0-9)'
                : formData.exam === 'cat'
                  ? 'Enter your CAT percentile (0-100)'
                  : formData.exam === 'jee' && formData.jeeType === 'mains'
                    ? 'Enter your JEE Main All India Rank'
                    : formData.exam === 'jee' && formData.jeeType === 'advanced'
                      ? 'Enter your JEE Advanced rank'
                      : 'Enter your rank'}
            </p>
          </div>
        )}

        {/* Category */}
        {formData.exam !== 'ielts' && (
          <div>
            <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
              Category
            </label>
            <select
              id="category"
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {categories.map((category) => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </div>
        )}

        {/* Gender */}
        <div>
          <label htmlFor="gender" className="block text-sm font-medium text-gray-700 mb-2">
            Gender
          </label>
          <select
            id="gender"
            value={formData.gender}
            onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
            className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {genders.map((gender) => (
              <option key={gender} value={gender}>{gender}</option>
            ))}
          </select>
        </div>

        {/* Quota */}
        {formData.exam !== 'ielts' && (
          <div>
            <label htmlFor="quota" className="block text-sm font-medium text-gray-700 mb-2">
              Quota
            </label>
            <select
              id="quota"
              value={formData.quota}
              onChange={(e) => setFormData({ ...formData, quota: e.target.value })}
              className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {quotas.map((quota) => (
                <option key={quota} value={quota}>{quota}</option>
              ))}
            </select>
          </div>
        )}

        {/* Tolerance Percent */}
        {formData.exam !== 'ielts' && (
          <div>
            <label htmlFor="tolerance" className="block text-sm font-medium text-gray-700 mb-2">
              Rank Tolerance (optional)
            </label>
            <div className="flex items-center gap-3">
              <input
                type="range"
                id="tolerance"
                min={0}
                max={20}
                step={1}
                value={formData.tolerance_percent}
                onChange={(e) => setFormData({ ...formData, tolerance_percent: Number(e.target.value) })}
                className="w-full"
              />
              <span className="w-14 text-right text-sm text-gray-700">{formData.tolerance_percent}%</span>
            </div>
            <p className="mt-1 text-xs text-gray-500">Allows a small buffer above the closing rank. 0% = strict.</p>
          </div>
        )}

        {/* Submit Button */}
        <motion.button
          type="submit"
          disabled={loading || isLoading}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className={`w-full py-3 px-6 rounded-lg font-semibold text-white transition-all duration-200 ${
            loading || isLoading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl'
          }`}
        >
          {loading || isLoading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Generating Predictions...
            </div>
          ) : (
            'Get College Predictions'
          )}
        </motion.button>
      </form>

      {/* Bottom Info Section */}
      <div className="mt-8 pt-6 border-t border-gray-100">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
          <div className="space-y-2">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
              <Globe className="w-6 h-6 text-blue-600" />
            </div>
            <div className="text-sm font-medium text-gray-900">All India Coverage</div>
            <div className="text-xs text-gray-600">Colleges from across India</div>
          </div>
          <div className="space-y-2">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
              <TrendingUp className="w-6 h-6 text-blue-600" />
            </div>
            <div className="text-sm font-medium text-gray-900">Real Data</div>
            <div className="text-xs text-gray-600">Based on official sources</div>
          </div>
          <div className="space-y-2">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
              <Calendar className="w-6 h-6 text-blue-600" />
            </div>
            <div className="text-sm font-medium text-gray-900">Updated 2024</div>
            <div className="text-xs text-gray-600">Latest cutoff data</div>
          </div>
        </div>
      </div>
    </motion.div>
  )
}


