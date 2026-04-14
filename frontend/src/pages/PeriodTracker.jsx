import React, { useEffect, useState } from "react";
import "./PeriodTracker.css";
import { periodTrackerAPI } from "../services/api";

const PeriodTracker = () => {
  const [selectedFlow, setSelectedFlow] = useState(null);
  const [selectedMood, setSelectedMood] = useState([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [prediction, setPrediction] = useState(null);
  const [phaseData, setPhaseData] = useState(null);
  const [irregularity, setIrregularity] = useState(null);

  const today = new Date();
  const [currentMonth, setCurrentMonth] = useState(today.getMonth());
  const [currentYear, setCurrentYear] = useState(today.getFullYear());
  const [selectedDate, setSelectedDate] = useState(new Date());
  

  // ---------- HELPERS ----------
  
  const getDaysInMonth = (year, month) =>
    new Date(year, month + 1, 0).getDate();

  const getFirstDayOfMonth = (year, month) =>
    new Date(year, month, 1).getDay();

  const formatDate = (date) =>{
    const d = new Date(date);
    d.setHours(0, 0, 0, 0);
    return d.toLocaleDateString("en-CA"); // YYYY-MM-DD
  };

  const normalizedPredictionDates = React.useMemo(() => {
    return prediction?.next_period_dates?.map(d => formatDate(d)) || [];
  }, [prediction]);
    

  // ---------- CALENDAR ----------
  
  const generateCalendar = () => {
    const daysInMonth = getDaysInMonth(currentYear, currentMonth);
    const firstDay = getFirstDayOfMonth(currentYear, currentMonth);

    const days = [];

    for (let i = 0; i < firstDay; i++) days.push(null);
    const todayDate = new Date();
    todayDate.setHours(0,0,0,0);

    for (let day = 1; day <= daysInMonth; day++) {
      const dateObj = new Date(currentYear, currentMonth, day);
      const dateStr = formatDate(dateObj);
      

      const isFuture = dateObj > todayDate;

      let type = "normal";

      // 🔴 Period
      if (history.some(h => formatDate(h.entry_date) === dateStr)) {
        type = "period";
      }

      // 🔵 Ovulation
      if (prediction?.ovulation_date === dateStr) {
        type = "ovulation";
      }

      // 🟢 Fertile
      if (
        prediction?.fertile_window &&
        dateStr >= prediction.fertile_window.start &&
        dateStr <= prediction.fertile_window.end
      ) {
        type = "fertile";
      }

      
      // 🔴 Predicted Period (robust)
      if (type === "normal") {
        if (normalizedPredictionDates.includes(dateStr)) {
          type = "predicted";
        } else if (prediction?.next_period_date) {
          const start = new Date(prediction.next_period_date);

          for (let i = 0; i < 5; i++) {
            const d = new Date(start);
            d.setDate(start.getDate() + i);

            if (formatDate(d) === dateStr) {
              type = "predicted";
            }
          }
        }
      }

      const isSelected = formatDate(selectedDate) === dateStr;

      days.push({ day, type, dateObj, isSelected, isFuture });
    }

    return days;
  };

  const calendarDays = React.useMemo(() => generateCalendar(), [
    currentMonth,
    currentYear,
    history,
    prediction,
    selectedDate
  ]);

  const changeMonth = (dir) => {
    let m = currentMonth + dir;
    let y = currentYear;

    if (m < 0) { m = 11; y--; }
    if (m > 11) { m = 0; y++; }

    setCurrentMonth(m);
    setCurrentYear(y);
  };

  const toggleMood = (mood) => {
    setSelectedMood(prev =>
      prev.includes(mood)
        ? prev.filter(m => m !== mood)
        : [...prev, mood]
    );
  };

  const toggleSymptoms = (symptom) => {
    setSelectedSymptoms(prev =>
      prev.includes(symptom)
        ? prev.filter(s => s !== symptom)
        : [...prev, symptom]
    );
  };


  // ---------- FETCH ----------
  useEffect(() => {
    const fetchPrediction = async () => {
      try {
        const res = await periodTrackerAPI.getPrediction();
        setPrediction(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchPrediction();
  }, []);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await periodTrackerAPI.getHistory();
        setHistory(res.data || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  useEffect(() => {
    const fetchPhase = async () => {
      try {
        const res = await periodTrackerAPI.getPhase();
        setPhaseData(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchPhase();
  }, []);

  useEffect(() => {
    const fetchIrregularity = async () => {
      try {
        const res = await periodTrackerAPI.getIrregularity();
        setIrregularity(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchIrregularity();
  }, []);

  // ---------- SAVE ----------
  const handleSave = async () => {
  if (!selectedFlow && selectedMood.length === 0 && selectedSymptoms.length === 0) {
    return alert("Please log something");
  }

  try {
    const payload = {
      entry_date: formatDate(selectedDate),
      flow_level: selectedFlow,
      mood: selectedMood,
      symptoms: selectedSymptoms,
    };

    const res = await periodTrackerAPI.logEntry(payload);
    const saved = res.data || payload;
    

    setHistory(prev => {
      const filtered = prev.filter(
        h => formatDate(h.entry_date) !== saved.entry_date
      );
      return [saved, ...filtered];
    });

    // ✅ ADD THIS
    const phaseRes = await periodTrackerAPI.getPhase();
    setPhaseData(phaseRes.data);

    setSelectedFlow(null);
    setSelectedMood([]);
    setSelectedSymptoms([]);

  } catch (err) {
    console.error(err);
  }
};

  //---------- DELETE ENTRY ----------
  const handleDelete = async (id) => {
    if (!window.confirm("Delete this entry?")) return;

    try {
      await periodTrackerAPI.deleteEntry(id);

      // remove from UI instantly
      setHistory(prev => prev.filter(h => h.id !== id));

      // reset UI if selected date was deleted
      const selectedStr = formatDate(selectedDate);
      const deleted = history.find(h => h.id === id);

      if (deleted?.entry_date === selectedStr) {
        setSelectedFlow(null);
        setSelectedMood([]);
      }

    } catch (err) {
      console.error(err);
    }
  };

  
  return (
  <div className="page-container">

    {/* Header */}
    <div className="page-header">
      <div className="header-icon tracker-icon">
        <i className="ph ph-calendar-blank"></i>
      </div>
      <div>
        <h1>Cycle & Symptom Tracker</h1>
        <p>Monitor your rhythm, log daily symptoms, and understand your body better.</p>
      </div>
    </div>

    <div className="two-column-layout">

      {/* LEFT SIDE */}
      <div className="left-column">

        {/* CALENDAR CARD */}
        <div className="calendar-card">

          <div className="calendar-header">
            <i onClick={() => changeMonth(-1)} className="ph ph-caret-left"></i>

            <span>
              {new Date(currentYear, currentMonth).toLocaleString("default", {
                month: "long",
                year: "numeric",
              })}
            </span>

            <i onClick={() => changeMonth(1)} className="ph ph-caret-right"></i>
          </div>

          <div className="calendar-body">

            {/* CALENDAR GRID */}
            <div className="calendar-grid">

              {["Su","Mo","Tu","We","Th","Fr","Sa"].map(d => (
                <span key={d} className="day-name">{d}</span>
              ))}

              {calendarDays.map((d, i) =>
                d ? (
                  <span
                    key={i}
                    onClick={() => {
                      if (d.isFuture) return;

                      setSelectedDate(d.dateObj);

                      const existing = history.find(
                        h => formatDate(h.entry_date) === formatDate(d.dateObj)
                      );

                      if (existing) {
                        setSelectedFlow(existing.flow_level);
                        setSelectedMood(
                          Array.isArray(existing.mood)
                            ? existing.mood
                            : (existing.mood || "").split(", ").filter(Boolean));
                        setSelectedSymptoms(
                          Array.isArray(existing.symptoms)
                            ? existing.symptoms
                            : (existing.symptoms || "").split(", ").filter(Boolean));
                      } else {
                        setSelectedFlow(null);
                        setSelectedMood([]);
                        setSelectedSymptoms([]);
                      }
                    }}
                    className={`calendar-day ${d.type} ${d.isSelected ? "selected-day" : ""} ${d.isFuture ? "future-day" : ""}`}
                  >
                    {d.day}
                  </span>
                ) : <span key={i}></span>
              )}

            </div>

            {/* LEGEND */}
            <div className="calendar-legend">
              <h4>Cycle Legend</h4>

              <div className="legend-item">
                <span className="dot period"></span> Period (Bleeding)
              </div>

              <div className="legend-item">
                <span className="dot fertile"></span> Fertile Window
              </div>

              <div className="legend-item">
                <span className="dot ovulation"></span> Ovulation Day
              </div>

              <div className="legend-item">
                <span className="dot predicted"></span> Predicted Next Period
              </div>
            </div>

            {/* STATUS */}
            {phaseData && (
              <div className="current-status">
                <h3>{phaseData.phase}</h3>
                <p>{phaseData.message}</p>
              </div>
            )}

          </div>
        </div>

        {/* LOGGING CARD */}
        <div className="log-card">

          <div className="log-header">
            <div>
              <h2>Log for {formatDate(selectedDate)}</h2>
              <p>Cycle Day {phaseData?.day_in_cycle !== undefined ? phaseData.day_in_cycle : "--"}</p>
              {history.some(h => formatDate(h.entry_date) === formatDate(selectedDate)) && (
                <span style={{
                  fontSize: "12px",
                  color: "#5a6df0",
                  fontWeight: "500"
                }}>
                  Editing existing entry
                </span>
              )}
            </div>

            <button className="save-btn" onClick={handleSave}>
              Save Log
            </button>
          </div>

          {/* FLOW */}
          <div className="log-section">
            <h4>FLOW / SPOTTING</h4>

            <div className="pill-group">
              {["None","Spotting","Light","Medium","Heavy"].map(f => (
                <button
                  key={f}
                  className={`pill ${selectedFlow === f ? "active" : ""}`}
                  onClick={() => setSelectedFlow(f)}
                >
                  {f}
                </button>
              ))}
            </div>
          </div>

          {/* PHYSICAL */}
          <div className="log-section">
            <h4>PHYSICAL SYMPTOMS</h4>

            <div className="pill-group">
              {["Cramps","Bloating","Headache","Fatigue","Tender Breasts","Acne"].map(m => (
                <button
                  key={m}
                  onClick={() => toggleSymptoms(m)}
                  className={`pill ${selectedSymptoms.includes(m) ? "highlight" : ""}`}
                >
                  {m}
                </button>
              ))}
            </div>
          </div>

          {/* MOOD */}
          <div className="log-section">
            <h4>MOOD & ENERGY</h4>

            <div className="pill-group">
              {["Calm","Happy","Anxious","Irritable","Sad","Energized"].map(m => (
                <button
                  key={m}
                  className={`pill ${selectedMood.includes(m) ? "mood-active" : ""}`}
                  onClick={() => toggleMood(m)}
                >
                  {m}
                </button>
              ))}
            </div>
          </div>

        </div>

      </div>

      {/* RIGHT SIDE */}
      <div className="right-column">

        {/* AI INSIGHTS */}
        <div className="insight-card">
          <h3>AI Insights</h3>

          {irregularity && (
            <>
              <div className="insight-item">
                <span className="insight-number">1</span>
                <div>
                  <h4>Cycle Analysis</h4>
                  <p>
                    {irregularity.ml_based?.is_irregular
                      ? "Your cycle shows irregular patterns."
                      : "Your cycle appears stable and regular."}
                  </p>
                </div>
              </div>

              {irregularity.rule_based?.issues?.length > 0 && (
                <div className="insight-item">
                  <span className="insight-number">2</span>
                  <div>
                    <h4>Observations</h4>
                    <ul>
                      {irregularity.rule_based.issues.map((issue, i) => (
                        <li key={i}>{issue}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* HISTORY */}
        <div className="history-card">
          <h3>Recent History</h3>

          {loading ? (
            <p>Loading...</p>
          ) : (
            history.slice(0, 4).map(h => {
                const moodArray = Array.isArray(h.mood)
                  ? h.mood
                  : (h.mood || "").split(", ").filter(Boolean);

                const symptomArray = Array.isArray(h.symptoms)
                  ? h.symptoms
                  : (h.symptoms || "").split(", ").filter(Boolean);

                return (
                  <div key={h.id} className="history-item">
                    <div className="history-date">
                      {new Date(h.entry_date).getDate()}
                    </div>
                    <div className="history-text">
                      <span className="history-title">{h.flow_level}</span>
                      <span className="history-sub">
                        {[...moodArray, ...symptomArray].join(", ") || "No details"}
                      </span>
                    </div>
                    <button
                      className="delete-btn"
                      onClick={() => handleDelete(h.id)}>
                      ✕
                    </button>
                  </div>
                );
              })
          )}
        </div>

      </div>

    </div>
  </div>
);
};

export default PeriodTracker;