import { useState } from "react";
import UploadBox from "../components/UploadBox";
import OncologyResultCard from "../components/OncologyResultCard";
import { oncologyAPI } from "../services/api";
import "./Oncology.css";

export default function Oncology() {
  // 📁 File state
  const [file, setFile] = useState(null);

  // 📊 Result + loading
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // 🧠 Symptoms state (basic for now)
  const [age, setAge] = useState(25);
  const [familyHistory, setFamilyHistory] = useState(null);
  const [lump, setLump] = useState(false);
  const [pain, setPain] = useState(false);
  const [sizeChange, setSizeChange] = useState(false);
  const [nippleDischarge, setNippleDischarge] = useState(false);
  const [skinChange, setSkinChange] = useState(false);
  const [smoking, setSmoking] = useState(false);
  const [alcohol, setAlcohol] = useState(false);
  const [physicalActivity, setPhysicalActivity] = useState("low");

  // 📁 Handle file selection
  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile);
  };

  // 🚀 Submit
  const handleSubmit = async () => {
    if (!file) {
      alert("Please upload an image");
      return;
    }

    const formData = new FormData();

    // 📁 Image
    formData.append("image", file);

    // 🧠 Symptoms (IMPORTANT — must match backend)
    formData.append("age", age);
    formData.append("family_history", familyHistory);
    formData.append("lump", lump);
    formData.append("pain", pain);
    formData.append("size_change", sizeChange);
    formData.append("nipple_discharge", nippleDischarge);
    formData.append("skin_change", skinChange);
    formData.append("smoking", smoking);
    formData.append("alcohol", alcohol);
    formData.append("physical_activity", physicalActivity);

    try {
      setLoading(true);

      const response = await oncologyAPI.fullAssessment(formData);

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Error connecting to backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="oncology-page">
      <h1>Early Detection Saves Lives</h1>

      <div className="oncology-layout">
        {/* LEFT PANEL */}
        <div className="left-panel">
          <UploadBox onFileSelect={handleFileSelect} />

          {/* 🧠 Simple Symptoms UI (minimal but functional) */}
          <div className="symptoms-card">
            <div className="top-inputs">
            {/* Age */}
            <div className="age-field">
              <label>Age</label>
              <input
                type="number"
                value={age}
                onChange={(e) => setAge(Number(e.target.value))}
              />
            </div>

            {/* Family History Question */}
            <div className="question-block">
              <p>Do you have a family history of breast cancer?</p>

              <div className="radio-group">
                <button
                  className={familyHistory === true ? "radio-btn active" : "radio-btn"}
                  onClick={() => setFamilyHistory(true)}
                >
                  Yes
                </button>

                <button
                  className={familyHistory === false ? "radio-btn active" : "radio-btn"}
                  onClick={() => setFamilyHistory(false)}
                >
                  No
                </button>
              </div>
            </div>
          </div>
            <h2>2. Current Symptoms</h2>
            <p>Select any physical symptoms you are experiencing.</p>

            <h4>Common Indicators</h4>

            <div className="symptom-chips">
              <button className={lump ? "chip active" : "chip"} onClick={() => setLump(!lump)}>
                Lump or Thickening
              </button>

              <button className={sizeChange ? "chip active" : "chip"} onClick={() => setSizeChange(!sizeChange)}>
                Change in breast size/shape
              </button>

              <button className={skinChange ? "chip active" : "chip"} onClick={() => setSkinChange(!skinChange)}>
                Skin redness/rash
              </button>

              <button className={nippleDischarge ? "chip active" : "chip"} onClick={() => setNippleDischarge(!nippleDischarge)}>
                Nipple discharge
              </button>

              <button className={pain ? "chip active" : "chip"} onClick={() => setPain(!pain)}>
                Pain or tenderness
              </button>
            </div>

            <div className="additional-section">
              <h4>Additional Context</h4>
              <textarea placeholder="Describe symptoms, duration, family history..."></textarea>
            </div>
          </div>

          <button onClick={handleSubmit} disabled={loading}>
            {loading ? "Analyzing..." : "Start AI Assessment"}
          </button>
        </div>

        {/* RIGHT PANEL */}
        <div className="right-panel">
          {result ? (
            <OncologyResultCard data={result} />
          ) : (
            <div className="placeholder">
              <h3>Awaiting Data</h3>
              <p>
                Upload your clinical imaging and symptoms to begin assessment.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}