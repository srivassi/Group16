import React from "react";

const Page: React.FC = () => {
  return (
    <div className="flex flex-col items-center text-center min-h-screen bg-gradient-to-b from-white to-gray-100 font-[Poppins]">
      <main className="flex-grow w-full max-w-4xl px-6 py-10">
        <h2 className="text-3xl font-semibold text-[#202A41] mb-6">
          Enter Hashtags
        </h2>
        <p className="text-lg text-[#202A41] mb-8">
          Enter hashtags below to analyze sentiment scores across X and BlueSky.
        </p>

        {/* Input Field for Hashtags */}
        <input
          type="text"
          placeholder="Enter hashtags (e.g., #AI, #Tech, #Finance)"
          className="w-full p-4 border border-gray-300 rounded-lg text-lg focus:outline-none focus:ring-2 focus:ring-[#202A41]"
        />

        {/* Submit Button */}
        <button className="mt-6 bg-[#202A41] text-[#E3E7EA] px-6 py-3 rounded-full font-semibold shadow-md hover:bg-[#404A61] transition">
          Analyze Sentiment
        </button>
      </main>
    </div>
  );
};

export default Page;
