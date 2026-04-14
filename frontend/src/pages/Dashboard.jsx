import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Dashboard.css";

const Dashboard = () => {
  const navigate = useNavigate(); // ✅ FIXED (inside component)

  // Default fallback name
  const [userName, setUserName] = useState("there");

  useEffect(() => {
    const userStr = localStorage.getItem("user");

    if (userStr) {
      try {
        const user = JSON.parse(userStr);

        if (user.preferred_name) {
          setUserName(user.preferred_name);
        } else if (user.full_name) {
          setUserName(user.full_name.split(" ")[0]);
        } else if (user.email) {
          setUserName(user.email.split("@")[0]);
        }
      } catch (e) {
        console.error("Could not parse user data", e);
      }
    }
  }, []);

  return (
    <div className="dashboard-page">
      
      {/* Hero Section */}
      <div className="dash-hero">
        <div className="dash-hero-content">
          <div className="hero-badge">
            <i className="ph ph-sparkle"></i> Your Daily Health Summary
          </div>

          <h1 className="dash-hero-title">
            Hello, <span className="highlight-name">{userName}</span>
          </h1>

          <p className="dash-hero-sub">
            Take control of your health journey today. Track your cycle,
            log changes, and get personalized insights all in one place.
          </p>

          <div className="dash-hero-actions">
            <button
              className="btn-primary"
              onClick={() => navigate("/period-tracker")}
            >
              Log Symptoms
            </button>

            <button
              className="btn-secondary"
              onClick={() => navigate("/ai-health")}
            >
              Talk to AI Assistant
            </button>
          </div>
        </div>
      </div>

      {/* Cards */}
      <div className="dash-grid">
        
        <div className="dash-card">
          <div
            className="dash-card-icon"
            style={{ color: "#E6A23C", background: "#FDF6EC" }}
          >
            <i className="ph ph-pulse"></i>
          </div>
          <h3>PCOS Detector</h3>
          <p>
            Analyze symptoms and ultrasound images with our AI model for
            early detection and management.
          </p>
          <Link to="/pcos-detector" className="dash-card-link">
            Start Analysis <i className="ph ph-arrow-right"></i>
          </Link>
        </div>

        <div className="dash-card">
          <div
            className="dash-card-icon"
            style={{ color: "#D17895", background: "#FFEAF0" }}
          >
            <i className="ph ph-medal"></i>
          </div>
          <h3>Breast Care </h3>
          <p>
            Upload imaging and log physical symptoms for breast cancer risk
            assessment and monitoring.
          </p>
          <Link to="/breast-cancer" className="dash-card-link">
            Start Assessment <i className="ph ph-arrow-right"></i>
          </Link>
        </div>

        <div className="dash-card">
          <div
            className="dash-card-icon"
            style={{ color: "#D17895", background: "#FFEAF0" }}
          >
            <i className="ph ph-calendar-heart"></i>
          </div>
          <h3>Cycle Tracker</h3>
          <p>
            Monitor your period, ovulation, and daily symptoms to understand
            your body's rhythm.
          </p>
          <Link to="/period-tracker" className="dash-card-link">
            View Calendar <i className="ph ph-arrow-right"></i>
          </Link>
        </div>

        <div className="dash-card">
          <div
            className="dash-card-icon"
            style={{ color: "#D17895", background: "#FFEAF0" }}
          >
            <i className="ph ph-chat-circle"></i>
          </div>
          <h3>AI Health Assistant</h3>
          <p>
            Have questions about your symptoms or reproductive health?
            Chat with our specialized AI.
          </p>
          <Link to="/ai-health" className="dash-card-link">
            Start Chat <i className="ph ph-arrow-right"></i>
          </Link>
        </div>

      </div>
    </div>
  );
};

export default Dashboard;