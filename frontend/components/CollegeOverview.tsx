import React from 'react';

export default function CollegeOverview({ selectedCollege }) {
  if (!selectedCollege) {
    return (
      <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-4">College Overview</h2>
        <p className="text-gray-700">Select a college to view details</p>
        <button className="mt-2 px-3 py-1 bg-blue-200 text-blue-800 rounded-full text-sm">Select from results</button>
        <p className="mt-4 text-gray-600 text-sm">
          Detailed information about colleges including admission process, facilities, faculty, placement records, and more will appear here once you select a college from search results or predictions.
        </p>
        <div className="mt-6 flex justify-between text-gray-700 font-semibold">
          <div>
            <p>Pros</p>
            <ul className="list-disc list-inside text-green-600">
              <li>Select a college to view pros</li>
            </ul>
          </div>
          <div>
            <p>Cons</p>
            <ul className="list-disc list-inside text-red-600">
              <li>Select a college to view cons</li>
            </ul>
          </div>
        </div>
        <h3 className="mt-6 font-semibold">Cutoff Trends (Last 3 Years)</h3>
        {/* Cutoff trends chart or data can be added here */}
      </div>
    );
  }

  // Render details if selectedCollege is provided (can be extended)
  return (
    <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-lg p-6">
      <h2 className="text-2xl font-bold mb-4">College Overview</h2>
      <div className="flex gap-6">
        <img src={selectedCollege.image || '/images/college-placeholder.jpg'} alt={selectedCollege.name} className="w-48 h-48 object-cover rounded-lg" />
        <div>
          <h3 className="text-xl font-semibold mb-2">{selectedCollege.name}</h3>
          <p className="text-gray-700 mb-4">{selectedCollege.description || 'No description available.'}</p>
          <div className="flex justify-between text-gray-700 font-semibold">
            <div>
              <p>Pros</p>
              <ul className="list-disc list-inside text-green-600">
                {(selectedCollege.pros && selectedCollege.pros.length > 0) ? selectedCollege.pros.map((pro, idx) => <li key={idx}>{pro}</li>) : <li>No pros listed.</li>}
              </ul>
            </div>
            <div>
              <p>Cons</p>
              <ul className="list-disc list-inside text-red-600">
                {(selectedCollege.cons && selectedCollege.cons.length > 0) ? selectedCollege.cons.map((con, idx) => <li key={idx}>{con}</li>) : <li>No cons listed.</li>}
              </ul>
            </div>
          </div>
          <h3 className="mt-6 font-semibold">Cutoff Trends (Last 3 Years)</h3>
          {/* Cutoff trends chart or data can be added here */}
        </div>
      </div>
    </div>
  );
}
