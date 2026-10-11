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
            <img src="/logo.png" alt="ReFood Connect Logo" className="brand-logo-img" />
            <div className="brand-titles">
              <h1>ReFood Connect</h1>
              <span className="brand-tagline">Smart Food Waste Redistribution Platform</span>
            </div>
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
