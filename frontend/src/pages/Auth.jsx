import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./Auth.css";

const Auth = () => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");

  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      if (isLogin) {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/auth/login/",
          {
            email: email,
            password: password,
          }
        );

        const data = response.data;

        // Save tokens
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);

        // Fetch FULL profile
        const profileRes = await axios.get(
          "http://127.0.0.1:8000/api/auth/profile/",
          {
            headers: {
              Authorization: `Bearer ${data.access_token}`,
            },
          }
        );

        const fullUser = profileRes.data;

        // 🔥 FLATTEN USER + PROFILE
        const cleanUser = {
        ...fullUser.user,
        ...fullUser.profile
        };

        // Save clean user
        localStorage.setItem("user", JSON.stringify(cleanUser));

        // Update navbar
        window.dispatchEvent(new Event("auth-change"));

        // Redirect logic (NOW WORKS)
        if (!cleanUser.height) {
          navigate("/onboarding");
        } else {
          navigate("/dashboard");
        }
      } else {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/auth/register/",
          {
            full_name: fullName,
            email: email,
            password: password,
            password_confirm: passwordConfirm,
          }
        );

        alert("Registration successful! You can now login.");
        setIsLogin(true);
      }
    } catch (err) {
      console.error("Auth Error:", err);

      setError(
        err.response?.data?.detail ||
          err.response?.data?.error ||
          "An unexpected error occurred. Check the console."
      );
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-icon">
          <i className="ph ph-heart"></i>
        </div>

        <div className="auth-header">
          <h1>Welcome to HerCare</h1>
          <p>Your personal healthcare companion</p>
        </div>

        <div className="auth-toggle">
          <button
            className={`toggle-btn ${isLogin ? "active" : ""}`}
            onClick={() => setIsLogin(true)}
            type="button"
          >
            Login
          </button>

          <button
            className={`toggle-btn ${!isLogin ? "active" : ""}`}
            onClick={() => setIsLogin(false)}
            type="button"
          >
            Register
          </button>
        </div>

        {error && (
          <div
            style={{
              backgroundColor: "#FFEBEE",
              color: "#B71C1C",
              padding: "12px",
              borderRadius: "10px",
              marginBottom: "1rem",
              fontSize: "0.9rem",
              textAlign: "center",
            }}
          >
            {error}
          </div>
        )}

        <form className="auth-form" onSubmit={handleSubmit}>
          {!isLogin && (
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                placeholder="Emma Watson"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
              />
            </div>
          )}

          <div className="form-group">
            <label>Email Address</label>
            <input
              type="email"
              placeholder="hello@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <div className="label-row">
              <label>Password</label>
              {isLogin && (
                <a href="#" className="forgot-link">
                  Forgot password?
                </a>
              )}
            </div>

            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label>Confirm Password</label>
              <input
                type="password"
                placeholder="••••••••"
                value={passwordConfirm}
                onChange={(e) => setPasswordConfirm(e.target.value)}
                required
              />
            </div>
          )}

          <button type="submit" className="auth-submit-btn">
            {isLogin ? "Sign In" : "Create Account"}
          </button>
        </form>

        <div className="auth-footer">
          <i className="ph ph-sparkle"></i> Private & Secure
        </div>
      </div>
    </div>
  );
};

export default Auth;