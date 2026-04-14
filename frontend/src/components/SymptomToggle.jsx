import "./SymptomToggle.css";

export default function SymptomToggle({ symptoms, setSymptoms, onContinue }) {

  const toggle = (key) => {
    setSymptoms({
      ...symptoms,
      [key]: symptoms[key] ? 0 : 1,
    });
  };

  return (
    <div className="symptom-card">

      <h3>Symptom Assessment</h3>
      <p className="symptom-sub">
        Select all symptoms you currently experience.
      </p>

      <div className="symptom-grid">

        <div className="symptom-item">
          <span>Irregular periods</span>
          <label className="switch">
            <input
              type="checkbox"
              checked={symptoms.cycleri}
              onChange={() => toggle("cycleri")}
            />
            <span className="slider"></span>
          </label>
        </div>

        <div className="symptom-item">
          <span>Excess facial/body hair</span>
          <label className="switch">
            <input
              type="checkbox"
              checked={symptoms.hair_growthyn}
              onChange={() => toggle("hair_growthyn")}
            />
            <span className="slider"></span>
          </label>
        </div>

        <div className="symptom-item">
          <span>Severe acne</span>
          <label className="switch">
            <input
              type="checkbox"
              checked={symptoms.pimplesyn}
              onChange={() => toggle("pimplesyn")}
            />
            <span className="slider"></span>
          </label>
        </div>

        <div className="symptom-item">
          <span>Unexplained weight gain</span>
          <label className="switch">
            <input
              type="checkbox"
              checked={symptoms.weight_gainyn}
              onChange={() => toggle("weight_gainyn")}
            />
            <span className="slider"></span>
          </label>
        </div>

        <div className="symptom-item">
          <span>Thinning hair / hair loss</span>
          <label className="switch">
            <input
              type="checkbox"
              checked={symptoms.hair_lossyn}
              onChange={() => toggle("hair_lossyn")}
            />
            <span className="slider"></span>
          </label>
        </div>

        <div className="symptom-item">
          <span>Darkening of skin</span>
          <label className="switch">
            <input
              type="checkbox"
              checked={symptoms.skin_darkening_yn}
              onChange={() => toggle("skin_darkening_yn")}
            />
            <span className="slider"></span>
          </label>
        </div>

        <div className="symptom-item">
          <span>Frequent fast food</span>
          <label className="switch">
            <input
              type="checkbox"
              checked={symptoms.fast_food_yn}
              onChange={() => toggle("fast_food_yn")}
            />
            <span className="slider"></span>
          </label>
        </div>

        <div className="symptom-item">
          <span>Regular exercise</span>
          <label className="switch">
            <input
              type="checkbox"
              checked={symptoms.regexerciseyn}
              onChange={() => toggle("regexerciseyn")}
            />
            <span className="slider"></span>
          </label>
        </div>

      </div>

      {/* Replace your current button with this: */}
      <div className="continue-btn-container">
          <button className="continue-btn" onClick={onContinue}>
              Continue to Upload
          </button>
      </div>
    </div>
  );
}