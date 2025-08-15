import React, { useState, useEffect } from 'react';
import { Search, GraduationCap, Target, BookOpen, TrendingUp, MapPin, Database, Globe } from 'lucide-react';

export default function CollegePredictor() {
  const [userRank, setUserRank] = useState('');
  const [examType, setExamType] = useState('JEE Main');
  const [category, setCategory] = useState('General');
  const [loading, setLoading] = useState(false);
  const [filteredColleges, setFilteredColleges] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedState, setSelectedState] = useState('');
  const [selectedCollegeType, setSelectedCollegeType] = useState('');
  const [allColleges, setAllColleges] = useState([]);
  const [stats, setStats] = useState(null);

  // Load comprehensive college data
  useEffect(() => {
    const loadCollegeData = async () => {
      try {
        const response = await fetch('/data/all_colleges.json');
        const data = await response.json();
        setAllColleges(data.colleges || []);
        
        // Calculate statistics
        const collegeStats = {
          total: data.colleges?.length || 0,
          byType: {},
          byState: {},
          bySource: {}
        };
        
        data.colleges?.forEach((college: any) => {
          // Count by type
          collegeStats.byType[college.type] = (collegeStats.byType[college.type] || 0) + 1;
          // Count by state
          collegeStats.byState[college.state] = (collegeStats.byState[college.state] || 0) + 1;
          // Count by source
          collegeStats.bySource[college.source] = (collegeStats.bySource[college.source] || 0) + 1;
        });
        
        setStats(collegeStats);
      } catch (error) {
        console.error('Error loading college data:', error);
        // Fallback to sample data
        setAllColleges([
          {
            name: "Indian Institute of Technology Bombay",
            type: "IIT",
            state: "Maharashtra",
            cutoff_jee_main: 100,
            cutoff_jee_advanced: 50,
            cutoff_neet: null,
            fees: "₹200000",
            seats: 120,
            source: "PDF_Extraction",
            exam_type: "JEE Advanced"
          }
        ]);
      }
    };
    
    loadCollegeData();
  }, []);

  const states = ["Maharashtra", "Karnataka", "Tamil Nadu", "Delhi", "Uttar Pradesh", "West Bengal", "Gujarat", "Rajasthan", "Madhya Pradesh", "Bihar", "Odisha", "Telangana", "Andhra Pradesh", "Kerala", "Punjab", "Haryana", "Jharkhand", "Chhattisgarh", "Assam", "Jammu and Kashmir", "Himachal Pradesh", "Uttarakhand", "Goa", "Puducherry", "Tripura", "Sikkim", "Manipur", "Mizoram", "Nagaland", "Arunachal Pradesh", "Meghalaya"];
  const types = ["IIT", "NIT", "AIIMS", "University", "Private"];

  const handlePredict = () => {
    if (!userRank || allColleges.length === 0) return;
    
    setLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      const rank = parseInt(userRank);
      const filtered = allColleges.filter((college: any) => {
        let cutoff = 0;
        if (examType === 'JEE Main') cutoff = college.cutoff_jee_main;
        else if (examType === 'JEE Advanced') cutoff = college.cutoff_jee_advanced;
        else if (examType === 'NEET') cutoff = college.cutoff_neet;
        
        return cutoff && rank <= cutoff * 1.5;
      });
      
      setFilteredColleges(filtered);
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-white p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">College Predictor</h1>
          <p className="text-gray-600 mb-6 max-w-xl mx-auto">
            Select your exam, enter your rank/score, and choose your category to predict eligible colleges.
          </p>
        </div>

        {/* Input Form */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Select Exam</label>
              <select
                value={examType}
                onChange={(e) => setExamType(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-600"
              >
                <option value="JEE Main">JEE Main/Advanced</option>
                <option value="NEET">NEET</option>
                <option value="IELTS">IELTS</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Your Rank/Score</label>
              <input
                type="number"
                value={userRank}
                onChange={(e) => setUserRank(e.target.value)}
                placeholder="Enter your rank or score"
                className="w-full rounded-lg border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-600"
              />
            </div>
          </div>

          {/* Category Buttons */}
          <div className="flex space-x-4 mb-6">
            {['General', 'OBC', 'SC', 'ST'].map((cat) => (
              <button
                key={cat}
                onClick={() => setCategory(cat)}
                className={`flex-1 py-2 rounded-lg border text-center font-semibold transition-colors duration-200 ${
                  category === cat
                    ? 'bg-blue-600 text-white border-blue-600'
                    : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          <button
            onClick={handlePredict}
            disabled={loading || allColleges.length === 0}
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition-shadow duration-200 disabled:opacity-50"
          >
            {loading ? 'Predicting...' : 'Predict Colleges'}
          </button>
        </div>

          {/* Filters */}
          {!loading && filteredColleges.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Search College
                </label>
                <div className="relative">
                  <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                  <input
                    type="text"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder="Search by name..."
                    className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  State
                </label>
                <select
                  value={selectedState}
                  onChange={(e) => setSelectedState(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All States</option>
                  {states.map(state => (
                    <option key={state} value={state}>{state}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  College Type
                </label>
                <select
                  value={selectedCollegeType}
                  onChange={(e) => setSelectedCollegeType(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Types</option>
                  {types.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>
            </div>
          )}
        </div>

        {/* Results */}
        {!loading && (
          <div className="bg-white rounded-2xl shadow-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-800">Eligible Colleges ({filteredColleges.length})</h2>
              <div className="text-sm text-gray-600">
                Showing results for rank {userRank} in {examType} ({category})
              </div>
            </div>

            {filteredColleges.length === 0 ? (
              <div className="text-center py-12">
                <BookOpen className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <p className="text-gray-600 text-lg">No colleges found for rank {userRank}.</p>
                <p className="text-gray-500 mt-2">Try a higher rank or different category.</p>
                <p className="text-sm text-blue-600 mt-4">
                  💡 Our database contains {allColleges.length} colleges from PDF and Careers360 sources
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filteredColleges.map((college: any, index: number) => {
                  let cutoff = 0;
                  if (examType === 'JEE Main') cutoff = college.cutoff_jee_main;
                  else if (examType === 'JEE Advanced') cutoff = college.cutoff_jee_advanced;
                  else if (examType === 'NEET') cutoff = college.cutoff_neet;

                  return (
                    <div key={index} className="border border-gray-200 rounded-xl p-4 hover:shadow-lg transition-shadow bg-white college-card">
                      <div className="flex justify-between items-start mb-3">
                        <h3 className="text-base font-semibold text-gray-900 flex-1">{college.name}</h3>
                        <div className="flex flex-col gap-1 ml-3">
                          <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
                            college.type === 'IIT' ? 'bg-yellow-100 text-yellow-800' :
                            college.type === 'NIT' ? 'bg-green-100 text-green-800' :
                            college.type === 'AIIMS' ? 'bg-red-100 text-red-800' :
                            college.type === 'University' ? 'bg-blue-100 text-blue-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {college.type}
                          </span>
                          <span className="bg-purple-100 text-purple-800 text-[10px] px-2 py-0.5 rounded text-center">
                            {college.source}
                          </span>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-3 text-xs text-gray-600">
                        <div>
                          <span className="font-medium">Cutoff Rank:</span> {cutoff?.toLocaleString() || 'N/A'}
                        </div>
                        <div>
                          <span className="font-medium">State:</span> {college.state}
                        </div>
                        <div>
                          <span className="font-medium">Fees:</span> {college.fees}
                        </div>
                        <div>
                          <span className="font-medium">Seats:</span> {college.seats}
                        </div>
                      </div>
                      
                      <div className="mt-2 text-[11px] text-gray-500">
                        Source: {college.source} | Exam: {college.exam_type}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
