import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Register from './pages/Register';
import Login from './pages/Login';
import DonorDashboard from './pages/DonorDashboard';
import NGODashboard from './pages/NGODashboard';
import VolunteerDashboard from './pages/VolunteerDashboard';
import AdminDashboard from './pages/AdminDashboard';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="app-header">
          <div className="brand-container">
            <svg className="brand-logo" viewBox="0 0 64 64" width="40" height="40" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#22c55e" />
                  <stop offset="100%" stopColor="#15803d" />
                </linearGradient>
              </defs>
              <circle cx="32" cy="32" r="30" fill="url(#logoGrad)" />
              <path d="M 32 10 A 22 22 0 0 1 54 32" fill="none" stroke="#ffffff" strokeWidth="3.5" strokeLinecap="round" opacity="0.95" />
              <polygon points="54,24 59,33 50,33" fill="#ffffff" />
              <path d="M 32 54 A 22 22 0 0 1 10 32" fill="none" stroke="#ffffff" strokeWidth="3.5" strokeLinecap="round" opacity="0.95" />
              <polygon points="10,40 5,31 14,31" fill="#ffffff" />
              <path d="M 32 46 C 32 36 21 28 21 19 C 29 19 37 23 37 33" fill="#86efac" opacity="0.95" />
              <path d="M 32 46 C 32 38 43 32 43 21 C 35 21 29 27 29 35" fill="#4ade80" />
              <circle cx="32" cy="30" r="3" fill="#ffffff" />
            </svg>
            <h1>ReFood Connect</h1>
          </div>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Navigate to="/login" />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/donor" element={<DonorDashboard />} />
            <Route path="/ngo" element={<NGODashboard />} />
            <Route path="/volunteer" element={<VolunteerDashboard />} />
            <Route path="/admin" element={<AdminDashboard />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
