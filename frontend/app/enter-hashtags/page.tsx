"use client";
import React, { useState } from "react";
import "./page.css";

const Page: React.FC = () => {
  const [search, setSearch] = useState("");
  const [searchResult, setSearchResult] = useState<any>(null);
  const [chatInput, setChatInput] = useState("");
  const [chatMessages, setChatMessages] = useState<any[]>([]);
  const [chatMinimized, setChatMinimized] = useState(false);

  const handleSearch = () => {
    fetch("http://localhost:5000/api/getPosts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ keyword: search || "Pope Francis" }),
    })
      .then((res) => res.json())
      .then((data) => setSearchResult(data))
      .catch((error) => console.error("Error fetching posts:", error));
  };

  const handleSearchKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") handleSearch();
  };

  const handleChatKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && searchResult) {
      fetch("http://localhost:5000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ query: chatInput }),
      })
        .then((res) => res.json())
        .then((data) => {
          setChatMessages((prev) => [
            ...prev,
            { sender: "user", text: chatInput },
          ]);
          setChatMessages((prev) => [
            ...prev,
            { sender: "bot", text: data.reply },
          ]);
          setChatInput("");
        })
        .catch((error) => console.error("Error with chat:", error));
    }
  };

  const getBackgroundColor = (score: number) => {
    if (score > 0.05) return "#d4edda";
    else if (score < -0.05) return "#f8d7da";
    else return "#fff3cd";
  };

  return (
    <div className="flex flex-col items-center text-center min-h-screen bg-gradient-to-b from-white to-gray-100 font-[Poppins]">
      <main className="flex-grow w-full max-w-4xl px-6 py-10">
        <h2 className="text-3xl font-semibold text-[#202A41] mb-6">
          Enter Hashtags
        </h2>
        <p className="text-lg text-[#202A41] mb-8">
          Enter hashtags below to analyze sentiment scores across X and BlueSky.
        </p>
        {/* Input Field for Hashtags with integrated functionality */}
        <input
          type="text"
          placeholder="Enter hashtags (e.g., #AI, #Tech, #Finance)"
          className="w-full p-4 border border-gray-300 rounded-lg text-lg focus:outline-none focus:ring-2 focus:ring-[#202A41] mb-4"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={handleSearchKeyDown}
        />
        {/* Submit Button */}
        <button
          className="mt-6 bg-[#202A41] text-[#E3E7EA] px-6 py-3 rounded-full font-semibold shadow-md hover:bg-[#404A61] transition"
          onClick={handleSearch}
        >
          Analyze Sentiment
        </button>

        {/* Render Search Results */}
        {searchResult && (
          <div className="mt-8 text-left">
            <h2 className="text-xl font-semibold text-[#202A41]">
              Search Results for: {searchResult.keyword}
            </h2>
            <h2 className="text-lg text-[#202A41]">
              Aggregate Sentiment: {searchResult.aggregate_sentiment}%
            </h2>
            <div className="mt-4 grid grid-cols-2 gap-4">
              {searchResult.posts.map((post: any, index: number) => (
                <div
                  key={index}
                  style={{ backgroundColor: getBackgroundColor(post.sentiment.compound) }}
                  className="p-4 rounded"
                >
                  <strong>{post.source}:</strong> {post.text}
                  <br />
                  <em>Sentiment Score: {post.sentiment.compound}</em>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Chat Window */}
        {searchResult && (
          <div className="chat-window fixed bottom-4 right-4 bg-white p-4 rounded shadow-md w-80">
            <div
              className="chat-header cursor-pointer mb-2"
              onClick={() => setChatMinimized(!chatMinimized)}
            >
              <h3 className="text-lg font-semibold">
                Chat With Bot {chatMinimized ? "(+)" : "(-)"}
              </h3>
            </div>
            {!chatMinimized && (
              <>
                <div className="chat-log h-40 overflow-y-auto border p-2 mb-2">
                  {chatMessages.length === 0 ? (
                    <p>No conversation yet.</p>
                  ) : (
                    chatMessages.map((msg, index) => (
                      <div key={index} className={`chat-message ${msg.sender}`}>
                        <strong>
                          {msg.sender === "user" ? "You" : "Bot"}:
                        </strong>{" "}
                        {msg.text}
                      </div>
                    ))
                  )}
                </div>
                <input
                  type="text"
                  placeholder="Enter your message..."
                  className="w-full p-2 border rounded"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={handleChatKeyDown}
                />
              </>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default Page;
