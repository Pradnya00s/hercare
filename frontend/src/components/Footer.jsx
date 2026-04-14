import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-brand">
          <div className="logo">
            <i className="ph ph-heart logo-icon"></i>
            <span>HerCare</span>
          </div>
          <p>Advanced AI care for your reproductive health journey.</p>
        </div>
        
        <div className="footer-links">
          <div className="link-group">
            <h4>Ecosystem</h4>
            <a href="/pcos-detector">PCOS Care</a>
            <a href="/breast-cancer">Oncology</a>
            <a href="/period-tracker">Cycle Tracker</a>
          </div>
          <div className="link-group">
            <h4>Support</h4>
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
            <a href="#">Help Center</a>
          </div>
        </div>
      </div>
      <div className="footer-bottom">
        <p>© 2026 HerCare AI. Built with care.</p>
      </div>
    </footer>
  );
};

export default Footer;