"use client";

// Imports
import React, { useState, useEffect, useRef } from "react";
import "./Home.css";
import Header from "../Header/Header";
import SideBar from "../SideBar/SideBar";
import Footer from "../Footer/Footer";
import NET from "vanta/dist/vanta.net.min";
import * as THREE from "three";
import Draggable from "react-draggable";

const Home = () => {
  const [search, setSearch] = useState("");
  const [vantaEffect, setVantaEffect] = useState(null);
  const vantaRef = useRef(null);
  const chatRef = useRef(null); // Fix for react-draggable

  // State for JSON response
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

  const [hashtags] = useState(["#Examples", "#Pope Francis"]);

  const filteredHashtags = hashtags.filter((tag) =>
    tag.toLowerCase().includes(search.toLowerCase())
  );

  // Handle search submission on Enter key using the getPosts route
  const handleKeyDown = (e) => {
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

  // Handle chat message submission on Enter key using the /api/chat route (only after getPosts)
  const handleChatKeyDown = (e) => {
    if (e.key === "Enter" && searchResult) {
      fetch("http://localhost:5000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ query: chatInput }),
      })
        .then((res) => res.json())
        .then((data) => {
          setChatMessages((prev) => [...prev, { sender: "user", text: chatInput }]);
          setChatMessages((prev) => [...prev, { sender: "bot", text: data.reply }]);
          setChatInput("");
        })
        .catch((error) => console.error("Error with chat:", error));
    }
  };

  // Helper function to choose background color based on sentiment score
  const getBackgroundColor = (score) => {
    if (score > 0.05) return "#d4edda"; // positive: light green
    else if (score < -0.05) return "#f8d7da"; // negative: light red
    else return "#fff3cd"; // neutral: light yellow
  };

  return (
    <div className="main" ref={vantaRef}>
      <Header />
      <SideBar />
      <div className="menuhome">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search hashtags..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={handleKeyDown} // Trigger search on Enter
          />
          <div className="suggestions">
            {filteredHashtags.map((tag, index) => (
              <div key={index} className="suggestion">
                {tag}
              </div>
            ))}
          </div>
        </div>

        {/* Display JSON response after searching */}
        {searchResult && (
          <div className="search-results">
            <h2>Search Results for: {searchResult.keyword}</h2>
            <h2>Aggregate Sentiment: {searchResult.aggregate_sentiment}%</h2>
            <ul>
              {searchResult.posts.map((post, index) => (
                <li
                  key={index}
                  style={{ backgroundColor: getBackgroundColor(post.sentiment.compound) }}
                >
                  <strong>{post.source}:</strong> {post.text}
                  <br />
                  <em>Sentiment Score: {post.sentiment.compound}</em>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Draggable Chat Window (Fix for React 18) */}
        {searchResult && (
          <Draggable nodeRef={chatRef}>
            <div className="chat-window" ref={chatRef}>
              <div
                className="chat-header"
                onClick={() => setChatMinimized(!chatMinimized)}
                style={{ cursor: "grab" }}
              >
                <h3>Chat With Bot {chatMinimized ? "(+)" : "(-)"}</h3>
              </div>
              {!chatMinimized && (
                <>
                  <div className="chat-log">
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
                    onKeyDown={handleChatKeyDown}
                  />
                </>
              )}
            </div>
          </Draggable>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default Home;
