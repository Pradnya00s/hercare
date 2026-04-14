import { Link } from "react-router-dom";
import "./Home.css";

const Home = () => {
  return (
    <div className="home">

      {/* HERO */}
      <section className="hero-section">
        <div className="hero-content">

          <div className="hero-badge">
            <i className="ph ph-sparkle"></i> Empowering Women's Health Through AI
          </div>

          <h1 className="hero-title">
            Your Body's Most <span className="hero-highlight">Intelligent</span><br />
            Companion
          </h1>

          <p className="hero-description">
            HerCare brings together advanced AI detection, smart tracking,<br />
            and personalized guidance to give you complete clarity over your<br />
            reproductive health.
          </p>

          <div className="hero-buttons">
            <Link to="/pcos-detector" className="btn-primary">
              Begin Your Journey <i className="ph ph-arrow-right"></i>
            </Link>

            <Link to="/features" className="btn-secondary">
              Explore Features
            </Link>
          </div>

        </div>
      </section>

      {/* FEATURES */}
      <section className="features-section">

        <h2 className="section-title">Comprehensive Care Ecosystem</h2>

        <p className="section-subtitle">
          Everything you need to understand, track, and optimize your health in
          one beautiful, secure place.
        </p>

        <div className="features-grid">

          <div className="feature-card">
            <div className="feature-icon icon-pink">
              <i className="ph ph-pulse"></i>
            </div>
            <h3>PCOS Detection</h3>
            <p>AI-powered analysis combining symptom tracking and ultrasound imaging to detect early signs of PCOS.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon icon-rose">
              <i className="ph ph-stethoscope"></i>
            </div>
            <h3>Breast Cancer Screening</h3>
            <p>Advanced assessment tool utilizing symptom logs and scan data for proactive breast health monitoring.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon icon-purple">
              <i className="ph ph-calendar-blank"></i>
            </div>
            <h3>Smart Period Tracker</h3>
            <p>Intelligent cycle tracking that learns your body's patterns and predicts your unique hormonal phases.</p>
          </div>

          <div className="feature-card">
            <div className="feature-icon icon-lavender">
              <i className="ph ph-chat-circle"></i>
            </div>
            <h3>AI Health Companion</h3>
            <p>24/7 personalized health assistant to answer your questions and provide empathetic guidance.</p>
          </div>

        </div>
      </section>

    </div>
  );
};

export default Home;