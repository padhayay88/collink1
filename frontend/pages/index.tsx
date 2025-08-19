import Head from 'next/head'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowRight, CheckCircle, BarChart2, GraduationCap, Search, TrendingUp, Globe, Star, Users } from 'lucide-react'
import Header from '../components/Header'
import Hero from '../components/Hero'
import LanguageSwitcher from '../components/LanguageSwitcher'
import { useEffect, useState } from 'react'

export default function Home() {
  const [counts, setCounts] = useState<{ neet: number; jee: number; pdf_universities: number; total: number } | null>(null)
  const [loadingCounts, setLoadingCounts] = useState<boolean>(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch('/api/v1/stats')
        if (res.ok) {
          const data = await res.json()
          setCounts({ neet: data.neet || 0, jee: data.jee || 0, pdf_universities: data.pdf_universities || 0, total: data.total || 0 })
        } else {
          // Fallback to local Next.js API route which returns dummy stats
          try {
            const resLocal = await fetch('/api/stats')
            if (resLocal.ok) {
              const dataLocal = await resLocal.json()
              setCounts({ neet: dataLocal.neet || 0, jee: dataLocal.jee || 0, pdf_universities: dataLocal.pdf_universities || 0, total: dataLocal.total || 0 })
            }
          } catch {}
        }
      } catch (e) {
        // Fallback if network error
        try {
          const resLocal = await fetch('/api/stats')
          if (resLocal.ok) {
            const dataLocal = await resLocal.json()
            setCounts({ neet: dataLocal.neet || 0, jee: dataLocal.jee || 0, pdf_universities: dataLocal.pdf_universities || 0, total: dataLocal.total || 0 })
          }
        } catch {}
      } finally {
        setLoadingCounts(false)
      }
    }
    fetchStats()
  }, [])

  const features = [
    {
      icon: <GraduationCap className="w-8 h-8" />,
      title: 'College Predictions',
      description: 'Get accurate predictions based on your competitive exam rank with confidence scores.',
      color: 'from-blue-500 to-blue-600'
    },
    {
      icon: <Search className="w-8 h-8" />,
      title: 'Smart Search',
      description: 'Find colleges with advanced search, filters, and detailed insights.',
      color: 'from-purple-500 to-purple-600'
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: 'Real Data',
      description: 'Based on authentic data from official sources like JoSAA, MCC, and university websites.',
      color: 'from-green-500 to-green-600'
    },
    {
      icon: <Globe className="w-8 h-8" />,
      title: 'All India Coverage',
      description: 'Comprehensive coverage of colleges across India and international universities.',
      color: 'from-orange-500 to-orange-600'
    },
    {
      icon: <Star className="w-8 h-8" />,
      title: 'Detailed Insights',
      description: 'Get ratings, fees, placements, pros/cons, and NIRF rankings for each college.',
      color: 'from-pink-500 to-pink-600'
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: 'Multiple Exams',
      description: 'Support for JEE Advanced, NEET UG, and IELTS with comprehensive data.',
      color: 'from-indigo-500 to-indigo-600'
    }
  ]

  const stats = [
    { number: loadingCounts ? '…' : String(counts?.jee ?? 0), label: 'JEE Colleges (Careers360)' },
    { number: loadingCounts ? '…' : String(counts?.neet ?? 0), label: 'NEET Colleges (Careers360)' },
    { number: loadingCounts ? '…' : String(counts?.pdf_universities ?? 0), label: 'Universities (PDF)' },
    { number: loadingCounts ? '…' : String(counts?.total ?? 0), label: 'Total Listed' }
  ]

  return (
    <>
      <Head>
        <title>Collink - Find Your Perfect College Match</title>
        <meta name="description" content="Get accurate college predictions based on your competitive exam rank. Discover colleges with detailed insights, ratings, and placement data." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <Header />
        <Hero />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4 md:hidden">
          <LanguageSwitcher />
        </div>

        {/* Quote Section */}
        <section className="py-8 md:py-12">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="bg-white/70 backdrop-blur rounded-2xl border border-gray-200 shadow-sm p-6 md:p-8"
            >
              <blockquote className="text-center">
                <p className="text-xl md:text-2xl font-semibold text-slate-900 leading-relaxed">
                  “Right college. Right course. Right now — powered by real data, AI insights, and your ambitions.”
                </p>
                <footer className="mt-3 text-slate-600 text-sm">— Collink AI Recommendations</footer>
              </blockquote>
            </motion.div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-slate-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mb-3">
                Why Choose Collink?
              </h2>
              <p className="text-base md:text-lg text-slate-600 max-w-3xl mx-auto">
                We provide comprehensive college prediction and search tools to help you make informed decisions about your future.
              </p>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: index * 0.06 }}
                  className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow duration-200 border border-gray-200"
                >
                  <div className="w-12 h-12 rounded-lg bg-slate-100 flex items-center justify-center text-slate-700 mb-4">
                    {feature.icon}
                  </div>
                  <h3 className="text-lg font-semibold text-slate-900 mb-1">{feature.title}</h3>
                  <p className="text-slate-600 text-sm leading-6">{feature.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-center mb-12"
            >
              <h2 className="text-4xl font-bold text-gray-900 mb-4">Trusted by Students</h2>
              <p className="text-xl text-gray-600">Our platform helps thousands of students find their perfect college match</p>
            </motion.div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              {stats.map((stat, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="text-center"
                >
                  <div className="text-4xl md:text-5xl font-bold text-gray-900 mb-2">
                    {stat.number}
                  </div>
                  <div className="text-gray-600 font-medium">
                    {stat.label}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Data Section with cards and side image */}
        <section className="py-20 bg-slate-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
              {/* Left: content */}
              <div>
                <div className="text-center lg:text-left mb-10">
                  <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 mb-3">Data</h2>
                  <p className="text-slate-600 max-w-2xl">
                    We simplify information for you on over {counts?.total ?? 0} colleges, multiple exams, and diverse courses across India.
                  </p>
                </div>

                <div className="space-y-6">
                  {/* Rankings Card */}
                  <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
                    <div className="flex items-start gap-3">
                      <div className="w-10 h-10 rounded-lg bg-slate-100 flex items-center justify-center text-slate-700">
                        <BarChart2 className="w-5 h-5" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-slate-900">Rankings</h3>
                        <p className="text-sm text-slate-600 mt-1">Transparent and data-driven rankings to help you compare colleges.</p>
                        <div className="flex flex-wrap gap-2 mt-4">
                          <Link href="/colleges" className="px-3 py-1.5 rounded-full text-sm border border-gray-200 bg-white hover:border-blue-300">Top Engineering</Link>
                          <Link href="/colleges" className="px-3 py-1.5 rounded-full text-sm border border-gray-200 bg-white hover:border-blue-300">Top MBA</Link>
                          <Link href="/colleges" className="px-3 py-1.5 rounded-full text-sm border border-gray-200 bg-white hover:border-blue-300">Top Medical</Link>
                          <Link href="/colleges" className="px-3 py-1.5 rounded-full text-sm border border-gray-200 bg-white hover:border-blue-300">Top Universities</Link>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Exams Card */}
                  <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
                    <div className="flex items-start gap-3">
                      <div className="w-10 h-10 rounded-lg bg-slate-100 flex items-center justify-center text-slate-700">
                        <GraduationCap className="w-5 h-5" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-slate-900">Exams</h3>
                        <p className="text-sm text-slate-600 mt-1">Easy access to details and predictors for popular exams.</p>
                        <div className="flex flex-wrap gap-2 mt-4">
                          <Link href="/predict?exam=jee" className="px-3 py-1.5 rounded-full text-sm border border-gray-200 bg-white hover:border-blue-300">JEE</Link>
                          <Link href="/predict?exam=neet" className="px-3 py-1.5 rounded-full text-sm border border-gray-200 bg-white hover:border-blue-300">NEET</Link>
                          <Link href="/predict?exam=ielts" className="px-3 py-1.5 rounded-full text-sm border border-gray-200 bg-white hover:border-blue-300">IELTS</Link>
                          <Link href="/search" className="px-3 py-1.5 rounded-full text-sm border border-gray-200 bg-white hover:border-blue-300">Search All</Link>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right: illustration image */}
              <div className="relative">
                <div className="mx-auto max-w-md lg:max-w-none">
                  <img src="/data/image3.png" alt="Data Illustration" className="w-full h-auto rounded-xl shadow-md object-contain" />
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 bg-white">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                Ready to Find Your Perfect College?
              </h2>
              <p className="text-xl text-gray-600 mb-8">
                Get started with Collink today and discover colleges that match your rank and preferences.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                  href="/predict"
                  className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-full text-lg font-semibold hover:shadow-lg transform hover:scale-105 transition-all duration-200"
                >
                  Start Predicting
                </Link>
                <Link
                  href="/search"
                  className="bg-white text-gray-700 px-8 py-4 rounded-full text-lg font-semibold border-2 border-gray-200 hover:border-blue-300 hover:shadow-lg transform hover:scale-105 transition-all duration-200"
                >
                  Search Colleges
                </Link>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Footer */}
        <footer className="bg-gray-900 text-white py-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <div>
                <div className="flex items-center space-x-2 mb-4">
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                    <GraduationCap className="w-5 h-5 text-white" />
                  </div>
                  <span className="text-xl font-bold">Collink</span>
                </div>
                <p className="text-gray-400">
                  Your trusted partner in college selection and career guidance.
                </p>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
                <ul className="space-y-2 text-gray-400">
                  <li><Link href="/predict" className="hover:text-white transition-colors">Predict Colleges</Link></li>
                  <li><Link href="/search" className="hover:text-white transition-colors">Search Colleges</Link></li>
                  <li><Link href="/colleges" className="hover:text-white transition-colors">Browse Colleges</Link></li>
                  <li><Link href="/about" className="hover:text-white transition-colors">About Us</Link></li>
                </ul>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold mb-4">Exams</h3>
                <ul className="space-y-2 text-gray-400">
                  <li><Link href="/predict?exam=jee" className="hover:text-white transition-colors">JEE Advanced</Link></li>
                  <li><Link href="/predict?exam=neet" className="hover:text-white transition-colors">NEET UG</Link></li>
                  <li><Link href="/predict?exam=ielts" className="hover:text-white transition-colors">IELTS</Link></li>
                </ul>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold mb-4">Contact</h3>
                <ul className="space-y-2 text-gray-400">
                  <li>Email: info@collink.com</li>
                  <li>Phone: +91 98765 43210</li>
                  <li>Address: India</li>
                </ul>
              </div>
            </div>
            
            <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
              <p>&copy; 2024 Collink. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}

