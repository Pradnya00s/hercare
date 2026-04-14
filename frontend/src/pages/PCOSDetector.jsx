import React, { useState } from "react";
import axios from "axios";
import SymptomToggle from "../components/SymptomToggle";
import UploadBox from "../components/UploadBox";
import ResultCard from "../components/ResultCard";
import "./PCOSDetector.css";

const PCOSDetector = () => {
  const [step, setStep] = useState(1);

  const [symptoms, setSymptoms] = useState({
    irregular_periods: false,
    weight_gain: false,
    acne: false,
    hair_loss: false,
    fatigue: false,
    mood_changes: false,
  });

  const [ultrasoundFile, setUltrasoundFile] = useState(null);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleNext = () => setStep(2);

  const handleAnalyze = async () => {
    const token = localStorage.getItem("access_token");
    const user = JSON.parse(localStorage.getItem("user") || "{}");

    // 🚫 Basic validation
    if (!user.age || !user.weight || !user.height || !user.cycle_length) {
      alert("Please complete your profile details first");
      return;
    }

    try {
      setLoading(true);

      // -------------------------------
      // 🟢 STEP 1: SYMPTOM MODEL
      // -------------------------------
      const symptomPayload = {
        age_yrs: Number(user.age),
        weight_kg: Number(user.weight),
        heightcm: Number(user.height),
        cycleri: symptoms.irregular_periods ? 1 : 0,
        cycle_lengthdays: Number(user.cycle_length),
        pregnantyn: 0,
        no_of_abortions: 0,
        weight_gainyn: symptoms.weight_gain ? 1 : 0,
        hair_growthyn: 0,
        skin_darkening_yn: 0,
        hair_lossyn: symptoms.hair_loss ? 1 : 0,
        pimplesyn: symptoms.acne ? 1 : 0,
        fast_food_yn: 0,
        regexerciseyn: 0,
      };

      const symptomRes = await axios.post(
        "http://127.0.0.1:8000/api/pcos/form-predict/",
        symptomPayload,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log("Symptom response:", symptomRes.data);

      const symptomProb =
        symptomRes.data.pcos_probability / 100; // convert to 0–1

      // -------------------------------
      // 🟢 STEP 2: ULTRASOUND MODEL
      // -------------------------------
      let ultrasoundProb = 0;

      if (ultrasoundFile) {
        const formData = new FormData();
        formData.append("ultrasound_image", ultrasoundFile);

        const ultrasoundRes = await axios.post(
          "http://127.0.0.1:8000/api/ultrasound/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        console.log("Ultrasound response:", ultrasoundRes.data);

        ultrasoundProb = ultrasoundRes.data.probability;
      }

      // -------------------------------
      // 🟢 STEP 3: COMBINED MODEL
      // -------------------------------
      const combinedRes = await axios.post(
        "http://127.0.0.1:8000/api/combined-prediction/",
        {
          symptom_probability: symptomProb,
          ultrasound_probability: ultrasoundProb,
        }
      );

      console.log("Final combined result:", combinedRes.data);

      setResult(combinedRes.data.final_probability);
      setStep(3);

    } catch (err) {
      console.error("Prediction error:", err);
      alert("Prediction failed. Check backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      {/* HEADER */}
      <div className="page-header">
        <div className="header-icon pulse-icon">
          <i className="ph ph-pulse"></i>
        </div>
        <div>
          <h1>PCOS Detector</h1>
          <p>AI-assisted analysis of symptoms and ultrasound data</p>
        </div>
      </div>

      <div className="two-column-layout">
        
        {/* LEFT SIDE */}
        <div className="main-content-column">

          {step === 1 && (
            <SymptomToggle
              symptoms={symptoms}
              setSymptoms={setSymptoms}
              onContinue={handleNext}
            />
          )}

          {step === 2 && (
            <div className="assessment-card">
              <h3>Upload Ultrasound</h3>
              <p className="assessment-sub">
                Provide medical imaging for AI analysis.
              </p>

              <UploadBox onFileSelect={setUltrasoundFile} />

              {ultrasoundFile && (
                <div className="file-info-badge">
                  <i className="ph ph-check-circle"></i>{" "}
                  {ultrasoundFile.name}
                </div>
              )}

              <div className="action-row">
                <button
                  className="btn-outline"
                  onClick={() => setStep(1)}
                >
                  Back
                </button>

                <button
                  className="btn-primary"
                  onClick={handleAnalyze}
                  disabled={loading}
                >
                  {loading ? "Analyzing..." : "Perform Assessment"}
                </button>
              </div>
            </div>
          )}

          {step === 3 && (
            <>
              {loading ? (
                <p>Analyzing...</p>
              ) : result !== null ? (
                <ResultCard probability={result} />
              ) : (
                <p>No result available</p>
              )}
            </>
          )}
        </div>

        {/* RIGHT SIDE */}
        <div className="side-column">
          <div className="info-card">
            <h3>About This Tool</h3>
            <p>
              Our PCOS detection model combines clinical symptom analysis
              with ultrasound imaging for improved accuracy.
            </p>
            <div className="info-note">
              <p>
                Note: This is an AI screening tool, not a diagnostic device.
                Always consult healthcare professionals.
              </p>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default PCOSDetector;