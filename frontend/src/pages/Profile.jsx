import "./Profile.css";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

export default function Profile() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user"));

  useEffect(() => {
    if (!user) {
      navigate("/login");
    }
  }, [user, navigate]);

  if (!user) return null;

  const healthData =
    JSON.parse(localStorage.getItem("healthData")) || null;

  const hasData =
    healthData &&
    (healthData.logs?.length > 0 ||
      healthData.symptomsLogged > 0 ||
      healthData.cycleConsistency);

  return (
    <div className="profile-container">
      
      {/* LEFT SIDE */}
      <div className="profile-left">

        {/* PROFILE CARD */}
        <div className="profile-card">
          <div className="avatar">
            <i className="ph ph-user"></i>
          </div>

          <h2>{user.name || user.preferred_name}</h2>

          <p className="subtitle">
            Your personal wellness space for cycle care & insights
          </p>

          <div className="tags">
            <span className="tag pink">
              Next period: {user.nextPeriod || "--"}
            </span>
            <span className="tag orange">
              PCOS risk: {user.pcosRisk || "--"}
            </span>
          </div>
        </div>

        {/* STATS */}
        <div className="stats">
          <div className="stat-card">
            <p><i className="ph ph-chart-bar"></i> Cycle Consistency</p>
            <h3>
              {hasData ? `${healthData.cycleConsistency}%` : "--"}
            </h3>
          </div>

          <div className="stat-card">
            <p><i className="ph ph-heartbeat"></i> Symptoms Logged</p>
            <h3>
              {hasData ? healthData.symptomsLogged : "--"}
            </h3>
          </div>
        </div>

      </div>

      {/* RIGHT SIDE */}
      <div className="profile-right">

        {/* PERSONAL DETAILS */}
        <div className="card">
          <h3>Personal details</h3>

          <div className="grid">
            <div>
              <p>Full name</p>
              <span>{user.name || user.preferred_name}</span>
            </div>

            <div>
              <p>Age</p>
              <span>{user.age} years</span>
            </div>

            <div className="full">
              <p>Email</p>
              <span>{user.email}</span>
            </div>
          </div>
        </div>

        {/* TRACKED DATA */}
        <div className="card">
          <h3>Tracked and logged data</h3>

          {!hasData ? (
            <p className="empty">
              <i className="ph ph-flower"></i> No data logged yet
            </p>
          ) : (
            <div className="grid">
              <div>
                <p>Average cycle</p>
                <span>{healthData.avgCycle} days</span>
              </div>

              <div>
                <p>Common symptoms</p>
                <span>
                  {healthData.commonSymptoms?.join(", ")}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* ACTIVITY */}
        <div className="card">
          <h3>Recent logs and activity</h3>

          {!hasData ? (
            <p className="empty">
              <i className="ph ph-clock"></i> No activity yet
            </p>
          ) : (
            <div className="activity-list">
              {healthData.logs.map((log, i) => (
                <div key={i} className="activity-item">
                  <strong>{log.title}</strong>
                  <span>{log.time}</span>
                  <p>{log.desc}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* SNAPSHOT */}
        <div className="card">
          <h3>Health snapshot</h3>

          {!hasData ? (
            <p className="empty">
              <i className="ph ph-info"></i> No data available
            </p>
          ) : (
            <p>Last period: {healthData.lastPeriod}</p>
          )}
        </div>

      </div>
    </div>
  );
}