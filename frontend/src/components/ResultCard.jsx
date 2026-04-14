import "./ResultCard.css";

export default function ResultCard({ probability }) {

  let riskLevel = "Low";
  let recommendation = "Maintain a healthy lifestyle and monitor symptoms.";

  if (probability >= 0.7) {
    riskLevel = "High";
    recommendation =
      "Consult a gynecologist for further evaluation and possible diagnostic tests.";
  } else if (probability >= 0.4) {
    riskLevel = "Moderate";
    recommendation =
      "Consider consulting a healthcare professional if symptoms persist.";
  }

  return (
    <div className="result-container">

      <h2>PCOS Risk Assessment</h2>

      <div className="probability-circle">
        {(probability * 100).toFixed(1)}%
      </div>

      <div className={`risk-badge ${riskLevel.toLowerCase()}`}>
        {riskLevel} Risk
      </div>

      <p className="result-description">
        This prediction is generated using an AI model trained on clinical
        symptom data and ultrasound analysis.
      </p>

      <div className="recommendation-box">
        <strong>Recommendation</strong>
        <p>{recommendation}</p>
      </div>

    </div>
  );
}