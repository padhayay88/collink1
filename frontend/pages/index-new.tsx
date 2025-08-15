import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { GraduationCap, Search, BookOpen, TrendingUp, MapPin, User, LogOut, Menu, X } from 'lucide-react';

export default function LandingPage() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [formData, setFormData] = useState({
    examType: '',
    rank: '',
    preferences: ''
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handlePredict = () => {
    if (formData.examType === '' || !formData.rank) {
      alert('Please select an exam type and enter your rank');
      return;
    }

    setIsLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      setIsLoading(false);
      alert('Prediction complete! Results are shown below.');
    }, 1500);
  };

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'Predict', href: '/predict' },
    { name: 'Colleges', href: '/colleges' },
    { name: 'Search', href: '/search' },
  ];

  return (
    <>
      <Head>
        <title>CollegeCompass - Smart College Counseling Platform</title>
        <meta name="description" content="Get personalized college recommendations based on your exam ranks, preferences, and latest cutoff data." />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex justify-between items-center">
              <div className="flex items-center">
                <div className="mr-4">
                  <GraduationCap className="w-10 h-10 text-blue-600" />
                </div>
                <h1 className="text-2xl font-bold text-gray-900">CollegeCompass</h1>
              </div>
              
              <nav className="hidden md:flex space-x-8">
                {navigation.map((item) => (
                  <Link key={item.name} href={item.href} className="text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                    {item.name}
                  </Link>
                ))}
              </nav>

              <div className="md:hidden">
                <button onClick={() => setIsMenuOpen(!isMenuOpen)}>
                  {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                </button>
              </div>
            </div>

            {/* Mobile Menu */}
            {isMenuOpen && (
              <div className="md:hidden mt-4">
                <div className="flex flex-col space-y-2">
                  {navigation.map((item) => (
                    <Link key={item.name} href={item.href} className="text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                      {item.name}
                    </Link>
                  ))}
                </div>
              </div>
            )}
          </div>
        </header>

        <main>
          {/* Hero Section */}
          <section className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-16">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="md:flex items-center justify-between">
                <div className="md:w-1/2 mb-10 md:mb-0">
                  <h2 className="text-4xl font-bold mb-4">Your Smart College Counseling Platform</h2>
                  <p className="text-lg mb-6">Get personalized college recommendations based on your exam ranks, preferences, and latest cutoff data.</p>
                  <div className="flex space-x-4">
                    <Link href="/predict" className="bg-white text-blue-600 px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition duration-300">
                      Try Predictor
                    </Link>
                    <button className="border-2 border-white text-white px-6 py-3 rounded-lg font-medium hover:bg-white hover:text-blue-600 transition duration-300">
                      Learn More
                    </button>
                  </div>
                </div>
                <div className="md:w-1/2">
                  <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8">
                    <div className="text-center">
                      <GraduationCap className="w-24 h-24 mx-auto mb-4 text-white" />
                      <p className="text-white/80">Smart college matching powered by AI</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Features Grid */}
          <section className="py-16">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">Platform Features</h2>
                <p className="text-lg text-gray-600 max-w-3xl mx-auto">All the tools you need to make informed college decisions</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {/* Feature 1: Prediction */}
                <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition duration-300">
                  <div className="p-6">
                    <div className="flex items-center mb-4">
                      <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center mr-3">
                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900">Predict colleges from rank</h3>
                    </div>
                    <p className="text-gray-600 mb-4">Get accurate college recommendations based on your entrance exam rank and preferences.</p>
                    <div className="bg-green-50 px-4 py-2 rounded-lg">
                      <p className="text-sm text-green-600">Status: <span className="font-medium">✅ Almost done</span></p>
                    </div>
                  </div>
                </div>

                {/* Feature 2: Exam Support */}
                <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition duration-300">
                  <div className="p-6">
                    <div className="flex items-center mb-4">
                      <div className="w-8 h-8 rounded-full bg-yellow-500 flex items-center justify-center mr-3">
                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900">Support JEE, NEET, IELTS</h3>
                    </div>
                    <p className="text-gray-600 mb-4">Comprehensive support for multiple entrance exams with specialized predictors for each.</p>
                    <div className="bg-yellow-50 px-4 py-2 rounded-lg">
                      <p className="text-sm text-yellow-600">Status: <span className="font-medium">🟡 Backend routers needed</span></p>
                    </div>
                  </div>
                </div>

                {/* Feature 3: College Overview */}
                <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition duration-300">
                  <div className="p-6">
                    <div className="flex items-center mb-4">
                      <div className="w-8 h-8 rounded-full bg-yellow-500 flex items-center justify-center mr-3">
                        <BookOpen className="w-4 h-4 text-white" />
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900">Show college overview</h3>
                    </div>
                    <p className="text-gray-600 mb-4">Detailed profiles for each college including infrastructure, faculty, and placement statistics.</p>
                    <div className="bg-yellow-50 px-4 py-2 rounded-lg">
                      <p className="text-sm text-yellow-600">Status: <span className="font-medium">🟡 Add in JSON</span></p>
                    </div>
                  </div>
                </div>

                {/* Feature 4: Search */}
                <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition duration-300">
                  <div className="p-6">
                    <div className="flex items-center mb-4">
                      <div className="w-8 h-8 rounded-full bg-yellow-500 flex items-center justify-center mr-3">
                        <Search className="w-4 h-4 text-white" />
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900">Search for any college</h3>
                    </div>
                    <p className="text-gray-600 mb-4">Powerful search functionality to find specific colleges by name, location, or courses.</p>
                    <div className="bg-yellow-50 px-4 py-2 rounded-lg">
                      <p className="text-sm text-yellow-600">Status: <span className="font-medium">🟡 Build /search route</span></p>
                    </div>
                  </div>
                </div>

                {/* Feature 5: Scraper */}
                <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition duration-300">
                  <div className="p-6">
                    <div className="flex items-center mb-4">
                      <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center mr-3">
                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900">Scraper for fresh cutoff data</h3>
                    </div>
                    <p className="text-gray-600 mb-4">Automatically updated cutoff ranks and admission data for the most accurate predictions.</p>
                    <div className="bg-green-50 px-4 py-2 rounded-lg">
                      <p className="text-sm text-green-600">Status: <span className="font-medium">✅ Almost ready</span></p>
                    </div>
                  </div>
                </div>

                {/* Feature 6: Deployed */}
                <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition duration-300">
                  <div className="p-6">
                    <div className="flex items-center mb-4">
                      <div className="w-8 h-8 rounded-full bg-gray-500 flex items-center justify-center mr-3">
                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900">Deployed live</h3>
                    </div>
                    <p className="text-gray-600 mb-4">Our platform will be available online for all students to access</p>
                    <div className="bg-gray-50 px-4 py-2 rounded-lg">
                      <p className="text-sm text-gray-600">Status: <span className="font-medium">🔲 Later step</span></p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Demo Section */}
          <section className="bg-gray-100 py-16">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="md:flex items-center">
                <div className="md:w-1/2 mb-10 md:mb-0">
                  <h2 className="text-3xl font-bold text-gray-900 mb-4">Try Our College Predictor</h2>
                  <p className="text-gray-600 mb-6">Our algorithm uses the latest cutoff data to give you personalized college recommendations based on your exam rank and preferences.</p>
                  
                  <div className="bg-white rounded-lg p-6 shadow-md">
                    <div className="mb-4">
                      <label className="block text-gray-700 text-sm font-medium mb-2">Exam Type</label>
                      <select 
                        name="examType"
                        value={formData.examType}
                        onChange={handleInputChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="">Select an exam</option>
                        <option value="JEE Main">JEE Main</option>
                        <option value="JEE Advanced">JEE Advanced</option>
                        <option value="NEET">NEET</option>
                        <option value="IELTS">IELTS</option>
                      </select>
                    </div>
                    <div className="mb-4">
                      <label className="block text-gray-700 text-sm font-medium mb-2">Your Rank</label>
                      <input 
                        type="number" 
                        name="rank"
                        value={formData.rank}
                        onChange={handleInputChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500" 
                        placeholder="Enter your rank"
                      />
                    </div>
                    <div className="mb-4">
                      <label className="block text-gray-700 text-sm font-medium mb-2">Preferences</label>
                      <select 
                        name="preferences"
                        value={formData.preferences}
                        onChange={handleInputChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="">Select preferred criteria</option>
                        <option value="Location">Location</option>
                        <option value="Course">Course</option>
                        <option value="Infrastructure">Infrastructure</option>
                        <option value="Placements">Placements</option>
                      </select>
                    </div>
                    <button 
                      onClick={handlePredict}
                      disabled={isLoading}
                      className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                    >
                      {isLoading ? 'Predicting...' : 'Predict Colleges'}
                    </button>
                  </div>
                </div>
                <div className="md:w-1/2 md:pl-12">
                  <div className="bg-white p-6 rounded-lg shadow-md">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Sample Prediction Results</h3>
                    <div className="space-y-4">
                      <div className="border-l-4 border-blue-500 pl-4 py-2">
                        <div className="flex justify-between items-center">
                          <h4 className="font-medium">Indian Institute of Technology Bombay</h4>
                          <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">90% Match</span>
                        </div>
                        <p className="text-sm text-gray-600">Computer Science Engineering</p>
                      </div>
                      <div className="border-l-4 border-blue-500 pl-4 py-2">
                        <div className="flex justify-between items-center">
                          <h4 className="font-medium">Delhi Technological University</h4>
                          <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">85% Match</span>
                        </div>
                        <p className="text-sm text-gray-600">Information Technology</p>
                      </div>
                      <div className="border-l-4 border-blue-500 pl-4 py-2">
                        <div className="flex justify-between items-center">
                          <h4 className="font-medium">Vellore Institute of Technology</h4>
                          <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">78% Match</span>
                        </div>
                        <p className="text-sm text-gray-600">Electronics and Communication</p>
                      </div>
                    </div>
                    <div className="mt-6 text-center">
                      <Link href="/predict" className="text-blue-600 hover:text-blue-800 font-medium">
                        View All Recommendations →
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Call to Action */}
          <section className="bg-indigo-600 text-white py-16">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
              <h2 className="text-3xl font-bold mb-6">Ready to find your perfect college match?</h2>
              <p className="text-xl mb-8 max-w-3xl mx-auto">Join thousands of students who've made smarter college choices with our platform.</p>
              <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4">
                <Link href="/predict" className="bg-white text-indigo-600 px-8 py-3 rounded-lg font-medium hover:bg-gray-100 transition duration-300">
                  Get Started Now
                </Link>
                <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-medium hover:bg-white hover:text-indigo-600 transition duration-300">
                  Learn How It Works
                </button>
              </div>
            </div>
          </section>
        </main>

        {/* Footer */}
        <footer className="bg-gray-900 text-white pt-12 pb-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <div>
                <h3 className="text-xl font-bold mb-4">CollegeCompass</h3>
                <p className="text-gray-400">Helping students make informed college decisions since 2023.</p>
              </div>
              <div>
                <h4 className="text-lg font-semibold mb-4">Features</h4>
                <ul className="space-y-2">
                  <li><Link href="/predict" className="text-gray-400 hover:text-white transition">College Predictor</Link></li>
                  <li><Link href="/colleges" className="text-gray-400 hover:text-white transition">Exam Support</Link></li>
                  <li><Link href="/search" className="text-gray-400 hover:text-white transition">College Reviews</Link></li>
                </ul>
              </div>
              <div>
                <h4 className="text-lg font-semibold mb-4">Resources</h4>
                <ul className="space-y-2">
                  <li><a href="#" className="text-gray-400 hover:text-white transition">Blog</a></li>
                  <li><a href="#" className="text-gray-400 hover:text-white transition">FAQs</a></li>
                  <li><a href="#" className="text-gray-400 hover:text-white transition">Contact Us</a></li>
                </ul>
              </div>
              <div>
                <h4 className="text-lg font-semibold mb-4">Stay Connected</h4>
                <p className="text-gray-400 text-sm mb-4">Subscribe to our newsletter for updates</p>
                <div className="mt-2 flex">
                  <input type="email" placeholder="Your email" className="px-4 py-2 rounded-l-lg text-gray-900 w-full" />
                  <button className="bg-indigo-600 px-4 py-2 rounded-r-lg">→</button>
                </div>
              </div>
            </div>
            <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
              <p>© 2023 CollegeCompass. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
}
