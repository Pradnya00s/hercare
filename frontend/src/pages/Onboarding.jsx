import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Onboarding.css";

const Onboarding = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    preferredName: "",
    age: "",
    weight: "",
    height: "",
    cycleLength: "28",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("access_token");
    
    // Map camelCase to snake_case for Django backend
    const payload = {
      preferred_name: formData.preferredName,
      age: formData.age,
      weight: formData.weight,
      height: formData.height,
      cycle_length: formData.cycleLength
    };

    try {
      await axios.post(
        "http://127.0.0.1:8000/api/auth/profile/setup/", 
        payload, 
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      // Update local storage so the Dashboard reflects changes immediately
      const user = JSON.parse(localStorage.getItem("user")) || {};

      user.name = formData.preferredName;
      user.age = formData.age;
      user.weight = formData.weight;
      user.height = formData.height;
      user.cycle_length = formData.cycleLength;

      user.profileCompleted = true;

      localStorage.setItem("user", JSON.stringify(user));

      navigate("/dashboard");
    } catch (err) {
      console.error("Setup failed", err);
      alert("Something went wrong. Please check your connection.");
    }
  };

  return (
    <div className="onboarding-page">
      <div className="onboarding-card">
        <div className="onboarding-header">
          <div className="step-badge">Personalization</div>
          <h1>Let's personalize HerCare</h1>
          <p>Tell us a bit about yourself so we can tailor your health insights.</p>
        </div>

        <form className="onboarding-form" onSubmit={handleSubmit}>
          <div className="form-group full-width">
            <label>What should we call you?</label>
            <input
              type="text"
              name="preferredName"
              placeholder="e.g. Pradnya"
              value={formData.preferredName}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Age</label>
              <input
                type="number"
                name="age"
                placeholder="25"
                value={formData.age}
                onChange={handleChange}
              />
            </div>
            
            <div className="form-group">
              <label>Cycle Length</label>
              <div className="input-with-suffix">
                <input
                  type="number"
                  name="cycleLength"
                  value={formData.cycleLength}
                  onChange={handleChange}
                />
                <span className="suffix">days</span>
              </div>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Weight</label>
              <div className="input-with-suffix">
                <input
                  type="number"
                  name="weight"
                  placeholder="65"
                  value={formData.weight}
                  onChange={handleChange}
                />
                <span className="suffix">kg</span>
              </div>
            </div>

            <div className="form-group">
              <label>Height</label>
              <div className="input-with-suffix">
                <input
                  type="number"
                  name="height"
                  placeholder="165"
                  value={formData.height}
                  onChange={handleChange}
                />
                <span className="suffix">cm</span>
              </div>
            </div>
          </div>

          <button type="submit" className="onboarding-submit">
            Complete Setup <i className="ph ph-arrow-right"></i>
          </button>
          
          <button type="button" className="btn-skip" onClick={() => navigate("/dashboard")}>
            Skip for now
          </button>
        </form>
      </div>
    </div>
  );
};

export default Onboarding;