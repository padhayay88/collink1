import Head from 'next/head'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowRight, CheckCircle, BarChart2, GraduationCap, Search, TrendingUp, Globe, Star, Users } from 'lucide-react'
import Header from '../components/Header'
import Hero from '../components/Hero'
import LanguageSwitcher from '../components/LanguageSwitcher'

export default function Home() {
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
    { number: '80+', label: 'Colleges & Universities' },
    { number: '3', label: 'Competitive Exams' },
    { number: '100%', label: 'Real Data' },
    { number: '2023', label: 'Latest Data' }
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

        {/* Features Section */}
        <section className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Why Choose Collink?
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                We provide comprehensive college prediction and search tools to help you make informed decisions about your future.
              </p>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {features.map((feature, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100"
                >
                  <div className={`w-16 h-16 bg-gradient-to-r ${feature.color} rounded-2xl flex items-center justify-center text-white mb-6`}>
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-4">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {feature.description}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-center mb-12"
            >
              <h2 className="text-4xl font-bold text-white mb-4">
                Trusted by Students
              </h2>
              <p className="text-xl text-blue-100">
                Our platform helps thousands of students find their perfect college match
              </p>
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
                  <div className="text-4xl md:text-5xl font-bold text-white mb-2">
                    {stat.number}
                  </div>
                  <div className="text-blue-100 font-medium">
                    {stat.label}
                  </div>
                </motion.div>
              ))}
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

