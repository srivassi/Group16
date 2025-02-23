// app/components/About.jsx
import React from 'react';

function About() {
  return (
    <div className="min-h-screen bg-white flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">About SentiMetrics</h1>
        <p className="text-lg text-gray-700">
          This is the about page for SentiMetrics.
        </p>
        {/* Add more content here */}
      </div>
    </div>
  );
}

export default About;