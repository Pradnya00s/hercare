import "./OncologyResultCard.css";

export default function OncologyResultCard({ data }) {
  if (!data) return null;

  const { ml_result, confidence, final_risk } = data;

  const riskClass = final_risk?.toLowerCase();

  return (
    <div className="oncology-result">

      <div className="result-header">
        <div className="icon">🛡️</div>
        <h3>Assessment Result</h3>
      </div>

      <div className="result-main">
        <h1 className={`result-label ${riskClass}`}>
          {ml_result || "—"}
        </h1>

        <p className="confidence">
          Confidence: {confidence ? `${confidence}%` : "--"}
        </p>

        <div className={`risk-pill ${riskClass}`}>
          {final_risk} Risk
        </div>
      </div>

      <div className="result-info">
        <p>
          This AI assessment combines imaging analysis and symptom data
          to estimate potential risk. This is not a medical diagnosis.
        </p>
      </div>

    </div>
  );
}