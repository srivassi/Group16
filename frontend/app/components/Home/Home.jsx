"use client";

//imports
import React, { useState, useEffect, useRef } from "react";
import "./Home.css";
import Header from "../Header/Header";
import SideBar from "../SideBar/SideBar";
import Footer from "../Footer/Footer";
import NET from "vanta/dist/vanta.net.min";
import * as THREE from "three";

const Home = () => {
  const [search, setSearch] = useState("");
  const [vantaEffect, setVantaEffect] = useState(null);
  const vantaRef = useRef(null);

  // State for JSON response
  const [searchResult, setSearchResult] = useState(null);

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

  const [hashtags] = useState([
    "#Examples",
    "#Pope Francis",
  ]);

  const filteredHashtags = hashtags.filter((tag) =>
    tag.toLowerCase().includes(search.toLowerCase())
  );

  // Simulated API response
  const mockResponse = {
    keyword: "Pope Francis",
    aggregate_sentiment: 65.4,
    posts: [
      {
        source: "Twitter",
        text: "Pope Francis calls for peace and unity in his latest speech.",
        sentiment: {
          neg: 0.0,
          neu: 0.7,
          pos: 0.3,
          compound: 0.6,
        },
      },
      {
        source: "Twitter",
        text: "Pope Francis addresses climate change and the need for action.",
        sentiment: {
          neg: 0.1,
          neu: 0.6,
          pos: 0.3,
          compound: 0.5,
        },
      },
      {
        source: "Bluesky",
        text: "Pope Francis emphasizes the importance of compassion and empathy.",
        sentiment: {
          neg: 0.0,
          neu: 0.5,
          pos: 0.5,
          compound: 0.7,
        },
      },
      {
        source: "Bluesky",
        text: "Pope Francis speaks about the role of faith in modern society.",
        sentiment: {
          neg: 0.0,
          neu: 0.8,
          pos: 0.2,
          compound: 0.4,
        },
      },
    ],
  };

  // Handle search submission on Enter key
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      setSearchResult(mockResponse); // Replace with actual API call
    }
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
            <p>Aggregate Sentiment: {searchResult.aggregate_sentiment}%</p>
            <ul>
              {searchResult.posts.map((post, index) => (
                <li key={index}>
                  <strong>{post.source}:</strong> {post.text}
                  <br />
                  <em>Sentiment Score: {post.sentiment.compound}</em>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default Home;
