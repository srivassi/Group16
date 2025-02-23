import React from "react";
import Link from "next/link";

const Page: React.FC = () => {
  return (
    <div className="bg-gradient-to-b from-white to-gray-100 min-h-screen flex flex-col items-center text-center font-[Poppins]">
      {/* Header Section */}
      <header className="relative w-full bg-white p-6 shadow-md flex flex-col items-center">
        <div className="absolute top-0 left-0 w-20 h-20 bg-gradient-to-r from-gray-300 to-gray-100 rounded-br-lg"></div>
        <div className="absolute top-0 right-0 w-24 h-12 bg-gray-300 rounded-bl-lg"></div>
        <h1 className="text-4xl font-semibold text-[#202A41] mt-4 cursor-pointer"><Link href="/">SentiMetrics</Link></h1>
        <p className="text-sm text-[#202A41] mt-2 border-b-2 border-purple-500 pb-1 mb-4">
          A HackIreland Project powered by Tines
        </p>
        <Link href='/page' className='mt-4 bg-[#202A41] text-[#E3E7EA] px-6 py-3 rounded-full font-semibold shadow-md hover:bg-[#404A61] transition inline-block text-center'>
          Get Started
        </Link>
      </header>

      {/* Analytics Section - Above the Fold */}
      <section className="w-full h-[60vh] flex flex-col justify-center items-center gap-6 px-12">
        <div className="grid grid-cols-2 gap-1 w-full items-center px-10">
          <img src="/analytics.png" alt="Analytics Icon" className="w-64 h-auto ml-32" />
          <div className="bg-[#ABBCC9] p-8 rounded-xl flex items-center justify-center text-[#202A41] text-lg h-36 w-[80%]">
            SentiMetrics automates brand value analysis based on public opinion by showing you the overall Sentiment Score for any discussions that interest you across X and BlueSky.
          </div>
        </div>
      </section>

      {/* Tines Section - Below the Fold */}
      <section className="w-full h-[50vh] flex flex-col justify-center items-center gap-4 px-12">
        <div className="grid grid-cols-2 gap-4 w-full items-center px-16">
          <div className="bg-[#ABBCC9] p-8 rounded-xl flex items-center justify-center text-[#202A41] text-lg h-36 w-[70%] ml-16">
            This project aligns with Tines' philosophy of Automation, Simplicity and Efficiency by maximising human productivity and utilising Generative AI chatbots to further future productivity.
          </div>
          <img src="/tines-logo.png" alt="Tines Logo" className="w-[120%] h-auto ml-24" />
        </div>
      </section>
    </div>
  );
};

export default Page;
