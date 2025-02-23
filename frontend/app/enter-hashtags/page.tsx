"use client";

import React, { useState, useEffect, useRef } from "react";
import Header from "./components/Header/Header";
import SideBar from "./components/SideBar/SideBar";
import Footer from "./components/Footer/Footer";
const NET = require("vanta/dist/vanta.net.min") as any;
import * as THREE from "three";
import Draggable from "react-draggable";

const Page: React.FC = () => {
  const [search, setSearch] = useState("");
  const [vantaEffect, setVantaEffect] = useState(null);
  const vantaRef = useRef(null);
  const chatRef = useRef(null);

  const [searchResult, setSearchResult] = useState(null);
  const [chatInput, setChatInput] = useState("");
  const [chatMessages, setChatMessages] = useState([]);
  const [chatMinimized, setChatMinimized] = useState(false);

  useEffect(() => {
    if (!vantaEffect) {
      setVantaEffect(
        NET({
          el: vantaRef.current,
          THREE,
          mouseControls: true,
          touchControls: true,
          gyroControls: false,
          minHeight: 200.0,
          minWidth: 200.0,
          scale: 1.0,
          scaleMobile: 1.0,
          color: 0xff3f81,
          backgroundColor: 0x23153c,
        })
      );
    }
    return () => {
      if (vantaEffect) vantaEffect.destroy();
    };
  }, [vantaEffect]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      fetch("http://localhost:5000/api/getPosts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ keyword: search || "Pope Francis" }),
      })
        .then((res) => res.json())
        .then((data) => setSearchResult(data))
        .catch((error) => console.error("Error fetching posts:", error));
    }
  };

  return (
    <div ref={vantaRef} className="flex flex-col min-h-screen text-center">
      <Header />
      <SideBar />
      <main className="flex-grow w-full max-w-4xl px-6 py-10 mx-auto">
        <h2 className="text-3xl font-semibold text-[#202A41] mb-6">
          Enter Hashtags
        </h2>
        <input
          type="text"
          placeholder="Enter hashtags (e.g., #AI, #Tech, #Finance)"
          className="w-full p-4 border border-gray-300 rounded-lg text-lg focus:outline-none focus:ring-2 focus:ring-[#202A41]"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={handleKeyDown}
        />
      </main>

      {searchResult && (
        <div className="search-results bg-white p-4 rounded-lg shadow-md">
          <h2 className="text-xl font-bold">Search Results for: {searchResult.keyword}</h2>
          <ul>
            {searchResult.posts.map((post: any, index: number) => (
              <li key={index} className="border-b py-2">
                <strong>{post.source}:</strong> {post.text}
              </li>
            ))}
          </ul>
        </div>
      )}

      {searchResult && (
        <Draggable nodeRef={chatRef}>
          <div ref={chatRef} className="fixed bottom-4 right-4 bg-white shadow-lg p-4 rounded-lg w-80">
            <div className="cursor-pointer" onClick={() => setChatMinimized(!chatMinimized)}>
              <h3 className="text-lg font-semibold">Chat With Bot {chatMinimized ? "(+)" : "(-)"}</h3>
            </div>
            {!chatMinimized && (
              <>
                <div className="chat-log h-40 overflow-y-auto border-t pt-2">
                  {chatMessages.length === 0 ? (
                    <p>No conversation yet.</p>
                  ) : (
                    chatMessages.map((msg, index) => (
                      <div key={index} className={`chat-message ${msg.sender}`}>
                        <strong>{msg.sender === "user" ? "You" : "Bot"}:</strong> {msg.text}
                      </div>
                    ))
                  )}
                </div>
                <input
                  type="text"
                  placeholder="Enter your message..."
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  className="w-full p-2 border rounded mt-2"
                />
              </>
            )}
          </div>
        </Draggable>
      )}
      <Footer />
    </div>
  );
};

export default Page;
