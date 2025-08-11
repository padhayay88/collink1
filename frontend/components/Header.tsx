import React, { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import { motion, AnimatePresence } from 'framer-motion'
import { GraduationCap, Menu, X, Search, BookOpen, TrendingUp, MapPin, User, LogOut } from 'lucide-react'
import { api } from '../lib/api'
import LanguageSwitcher from './LanguageSwitcher'
import { useAuth } from '../lib/auth'

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [isStateModalOpen, setIsStateModalOpen] = useState(false)
  const [states, setStates] = useState<string[]>([])
  const [loadingStates, setLoadingStates] = useState(false)
  const [stateQuery, setStateQuery] = useState('')
  const router = useRouter()
  const { user, isAuthenticated, logout } = useAuth()

  // Trimmed top navigation per request: remove States and AI Chat from header
  const navigation = [
    { name: 'Home', href: '/', icon: GraduationCap },
    { name: 'Predict', href: '/predict', icon: TrendingUp },
    { name: 'Colleges', href: '/colleges', icon: BookOpen },
    { name: 'Search', href: '/search', icon: Search },
  ]

  const isActive = (href: string) => {
    if (href === '/') {
      return router.pathname === '/'
    }
    return router.pathname.startsWith(href)
  }

  const openStateModal = async () => {
    setIsStateModalOpen(true)
    if (states.length === 0) {
      setLoadingStates(true)
      try {
        const list = await api.getSupportedStates('jee')
        setStates(list)
      } finally {
        setLoadingStates(false)
      }
    }
  }

  const filteredStates = states.filter(s => s.toLowerCase().includes(stateQuery.toLowerCase()))

  return (
    <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-2"
          >
            <Link href="/" className="flex items-center space-x-2 hover:opacity-80 transition-opacity">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <GraduationCap className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">Collink</span>
            </Link>
          </motion.div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-2">
            {navigation.map((item, index) => (
              <motion.div
                key={item.name}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Link
                  href={item.href}
                  className={`flex items-center gap-1 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                    isActive(item.href)
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  <item.icon className="w-4 h-4" />
                  <span>{item.name}</span>
                </Link>
              </motion.div>
            ))}
          </nav>

          {/* CTA + Choose State + Auth (Login/Register beside each other) */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="hidden md:flex items-center gap-3"
          >
            <LanguageSwitcher />
            <button
              onClick={openStateModal}
              className="flex items-center gap-2 px-3 py-2 rounded-lg border border-gray-200 text-gray-700 hover:bg-gray-50"
              title="Choose State"
            >
              <MapPin className="w-4 h-4" />
              <span>Choose State</span>
            </button>
            {isAuthenticated ? (
              <div className="flex items-center space-x-3">
                <Link
                  href="/profile"
                  className="flex items-center space-x-2 px-3 py-2 text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors"
                >
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                    <User className="w-4 h-4 text-white" />
                  </div>
                  <span className="text-sm font-medium text-gray-700">{user?.name}</span>
                </Link>
                <button
                  onClick={logout}
                  className="flex items-center space-x-1 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  <span className="text-sm">Logout</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  href="/login"
                  className="px-3 py-2 text-gray-700 hover:text-gray-900 font-medium transition-colors"
                >
                  Sign In
                </Link>
                <Link
                  href="/register"
                  className="px-3 py-2 text-gray-700 hover:text-gray-900 font-medium transition-colors"
                >
                  Sign Up
                </Link>
              </div>
            )}
            <Link
              href="/predict"
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-lg font-medium hover:shadow-lg transform hover:scale-105 transition-all duration-200 ml-1"
            >
              Get Started
            </Link>
          </motion.div>

          {/* Mobile actions: Choose State + Menu (AI Chat moved to bottom elsewhere) */}
          <div className="md:hidden flex items-center gap-2">
            <motion.button
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              onClick={openStateModal}
              className="p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-50 transition-colors"
              aria-label="Choose State"
              title="Choose State"
            >
              <MapPin className="w-6 h-6" />
            </motion.button>
            <motion.button
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-50 transition-colors"
              aria-label="Toggle menu"
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </motion.button>
          </div>
        </div>
      </div>

       {/* Mobile Navigation (no AI Chat, no States link) */}
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-white border-t border-gray-200"
          >
            <div className="px-4 py-2 space-y-1">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={() => setIsMenuOpen(false)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-base font-medium transition-colors ${
                    isActive(item.href)
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  <item.icon className="w-5 h-5" />
                  <span>{item.name}</span>
                </Link>
              ))}
              <div className="pt-2 space-y-2">
                <div className="flex gap-2">
                  <button
                    onClick={() => { setIsMenuOpen(false); openStateModal() }}
                    className="flex-1 border border-gray-200 text-gray-700 px-4 py-2 rounded-lg text-center"
                  >
                    <span className="inline-flex items-center gap-2 justify-center"><MapPin className="w-5 h-5" /> Choose State</span>
                  </button>
                  <Link
                    href="/predict"
                    onClick={() => setIsMenuOpen(false)}
                    className="block w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-lg text-center font-medium"
                  >
                    Get Started
                  </Link>
                </div>
                {isAuthenticated ? (
                  <div className="pt-2 border-t border-gray-200">
                    <Link
                      href="/profile"
                      onClick={() => setIsMenuOpen(false)}
                      className="flex items-center justify-center space-x-2 px-4 py-2 text-gray-700 hover:text-gray-900 font-medium transition-colors mb-3"
                    >
                      <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                        <User className="w-4 h-4 text-white" />
                      </div>
                      <span className="text-sm font-medium text-gray-700">{user?.name}</span>
                    </Link>
                    <button
                      onClick={() => { setIsMenuOpen(false); logout(); }}
                      className="w-full flex items-center justify-center space-x-2 px-4 py-2 text-gray-700 hover:text-gray-900 font-medium transition-colors"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>Logout</span>
                    </button>
                  </div>
                ) : (
                  <div className="flex gap-2 pt-2 border-t border-gray-200">
                    <Link
                      href="/login"
                      onClick={() => setIsMenuOpen(false)}
                      className="flex-1 text-center px-4 py-2 text-gray-700 hover:text-gray-900 font-medium transition-colors"
                    >
                      Sign In
                    </Link>
                    <Link
                      href="/register"
                      onClick={() => setIsMenuOpen(false)}
                      className="flex-1 text-center px-4 py-2 text-gray-700 hover:text-gray-900 font-medium transition-colors"
                    >
                      Sign Up
                    </Link>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* State Selector Modal */}
      <AnimatePresence>
        {isStateModalOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[60] bg-black/40 flex items-center justify-center p-4"
            onClick={() => setIsStateModalOpen(false)}
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="bg-white w-full max-w-2xl rounded-2xl shadow-xl overflow-hidden"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between px-5 py-4 border-b">
                <div className="flex items-center gap-2 text-gray-900 font-semibold">
                  <MapPin className="w-5 h-5" /> Choose State
                </div>
                <button onClick={() => setIsStateModalOpen(false)} className="p-2 rounded hover:bg-gray-100">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="p-5 space-y-4">
                <input
                  value={stateQuery}
                  onChange={(e) => setStateQuery(e.target.value)}
                  placeholder="Search state..."
                  className="w-full border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                {loadingStates ? (
                  <div className="py-8 text-center text-gray-500">Loading states...</div>
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-80 overflow-auto">
                    {filteredStates.map((st) => (
                      <Link
                        key={st}
                        href={{ pathname: '/state', query: { name: st } }}
                        onClick={() => setIsStateModalOpen(false)}
                        className="px-3 py-2 rounded-lg border border-gray-200 hover:bg-gray-50 text-gray-800"
                      >
                        {st}
                      </Link>
                    ))}
                    {filteredStates.length === 0 && (
                      <div className="col-span-2 text-center text-gray-500 py-6">No states found</div>
                    )}
                  </div>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  )
}
