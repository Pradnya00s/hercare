import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }

    // Update navbar on login/logout
    const handleAuthChange = () => {
      const updatedUser = localStorage.getItem("user");
      setUser(updatedUser ? JSON.parse(updatedUser) : null);
    };

    window.addEventListener("auth-change", handleAuthChange);
    return () => window.removeEventListener("auth-change", handleAuthChange);
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    window.dispatchEvent(new Event("auth-change"));
    navigate("/login");
  };

  return (
    <nav className="navbar">
      {/* LEFT LOGO */}
      <div className="nav-left">
        <Link to="/" className="logo">
          <i className="ph ph-heart" style={{ fontSize: "35px" }}></i>
          <span>HerCare</span>
        </Link>
      </div>

      {/* CENTER NAV LINKS */}
      <div className="nav-center">
        <Link to={user ? "/dashboard" : "/"}>Dashboard</Link>
        <Link to="/profile">Profile</Link>
        <Link to="/period-tracker">Cycle Tracker</Link>
        <Link to="/pcos-detector">PCOS Care</Link>
        <Link to="/breast-cancer">Oncology</Link>
        <Link to="/ai-health">AI Assistant</Link>
      </div>

      {/* RIGHT SIDE */}
      <div className="nav-right">
        {!user ? (
          <>
            <Link to="/login" className="login-link">
              Log in
            </Link>
            <Link to="/register" className="signup-btn">
              Sign up
            </Link>
          </>
        ) : (
          <>
            <button className="icon-btn">
              <i className="ph ph-user"></i>
            </button>

            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;