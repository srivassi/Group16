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
    "#Magnus Carlson",
    
  ]);

  const filteredHashtags = hashtags.filter((tag) =>
    tag.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="main" ref={vantaRef}>
      <Header />
      <SideBar />
      <div className="menu">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search hashtags..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <div className="suggestions">
            {filteredHashtags.map((tag, index) => (
              <div key={index} className="suggestion">
                {tag}
              </div>
            ))}
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Home;
