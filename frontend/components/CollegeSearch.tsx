
import React, { useState } from 'react';

export default function CollegeSearch({ onSearch }) {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = () => {
    if (onSearch) {
      onSearch(searchTerm);
    }
  };

  return (
    <div className="mb-8 max-w-4xl mx-auto bg-white rounded-2xl shadow-lg p-6">
      <h2 className="text-2xl font-bold mb-4">College Search</h2>
      <div className="flex">
        <input
          type="text"
          placeholder="Search for colleges..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-grow rounded-l-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-600"
        />
        <button
          onClick={handleSearch}
          className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-r-lg font-semibold hover:shadow-lg transition-shadow duration-200"
        >
          Search
        </button>
      </div>
      <h3 className="text-lg font-semibold mt-6">Featured Colleges</h3>
      {/* Featured colleges list can be added here */}
    </div>
  );
}
