import { Routes, Route } from "react-router-dom";
import "./App.css"; 

// Shared Components
import Navbar from "./components/Navbar";
import Footer from './components/Footer';

// Pages
import Home from "./pages/Home";
import Auth from "./pages/Auth"; 
import Dashboard from "./pages/Dashboard";
import PCOSDetector from "./pages/PCOSDetector";
import PeriodTracker from "./pages/PeriodTracker"; 
import AIHealth from "./pages/AIHealth";           
import Onboarding from "./pages/Onboarding";
import Profile from "./pages/Profile";
import Oncology from "./pages/Oncology";


export default function App() {
  return (
    <>
      <Navbar />
      
      <main style={{ minHeight: '80vh' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Auth />} />
          <Route path="/register" element={<Auth />} />
          <Route path="/onboarding" element={<Onboarding />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/pcos-detector" element={<PCOSDetector />} />
          <Route path="/period-tracker" element={<PeriodTracker />} />
          <Route path="/breast-cancer" element={<Oncology />} />
          <Route path="/ai-health" element={<AIHealth />} />
          <Route path="/profile" element={<Profile />} />

        </Routes>
      </main>

      <Footer />
    </>
  );
}