import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowRight, Target, BookOpen, TrendingUp } from 'lucide-react'

export default function Hero() {
  return (
    <div className="relative overflow-hidden bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-12">
      {/* Background Elements */}
      <div className="absolute inset-0 opacity-30">
        <img
          src="/images/campus.jpg"
          alt="College Campus"
          className="object-cover w-full h-full rounded-lg"
        />
      </div>

      <div className="relative max-w-7xl mx-auto">
        <div className="relative z-10 pb-8 sm:pb-16 md:pb-20 lg:w-full lg:pb-28 xl:pb-32">
          <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
            <div className="lg:grid lg:grid-cols-12 lg:gap-8 items-center">
              <div className="sm:text-center md:max-w-2xl md:mx-auto lg:col-span-6 lg:text-left">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8 }}
                >
                  <h1 className="text-5xl tracking-tight font-extrabold text-white sm:text-6xl md:text-7xl">
                    <span className="block xl:inline">collink</span>
                  </h1>
                  <p className="mt-6 text-lg text-white max-w-xl sm:mx-auto md:mx-0">
                    Discover your best-fit colleges based on JEE, NEET, or IELTS scores with our advanced prediction algorithm.
                  </p>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: 0.2 }}
                  className="mt-8 flex flex-col sm:flex-row sm:justify-start gap-4"
                >
                  <Link
                    href="/predict"
                    className="inline-flex items-center justify-center rounded-md border border-transparent bg-white px-8 py-3 text-base font-semibold text-blue-700 shadow-sm hover:bg-blue-50 sm:px-10 md:text-lg"
                  >
                    Try Predictor
                  </Link>
                  <Link
                    href="/search"
                    className="inline-flex items-center justify-center rounded-md border border-white border-opacity-30 px-8 py-3 text-base font-semibold text-white shadow-sm hover:bg-white hover:bg-opacity-20 sm:px-10 md:text-lg"
                  >
                    Search Colleges
                  </Link>
                </motion.div>
              </div>

              {/* Right side - Campus Image */}
              <div className="mt-12 relative sm:max-w-lg sm:mx-auto lg:mt-0 lg:max-w-none lg:mx-0 lg:col-span-6 lg:flex lg:items-center">
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.8, delay: 0.3 }}
                  className="relative mx-auto w-full rounded-lg shadow-lg lg:max-w-md overflow-hidden"
                >
                  <img
                    src="/images/campus.jpg"
                    alt="College Campus"
                    className="w-full h-auto rounded-lg"
                  />
                </motion.div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}
