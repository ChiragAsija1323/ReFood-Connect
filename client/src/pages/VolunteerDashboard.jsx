import { useState, useEffect } from 'react';
import axios from '../api/axios';
import { useNavigate } from 'react-router-dom';

const VolunteerDashboard = () => {
  const [tasks, setTasks] = useState([]);
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user')) || {};

  const fetchTasks = async () => {
    try {
      const { data } = await axios.get('/donations');
      setTasks(data);
    } catch (err) {
      console.error('Failed to fetch tasks', err);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleStatusUpdate = async (id, status) => {
    try {
      let otp = null;
      if (status === 'Picked Up') {
        otp = window.prompt('🔐 Enter 4-digit Pickup OTP from Donor:');
        if (otp === null) return;
        if (!otp.trim()) {
          alert('Pickup OTP cannot be empty.');
          return;
        }
      } else if (status === 'Delivered') {
        otp = window.prompt('🔐 Enter 4-digit Delivery OTP from NGO:');
        if (otp === null) return;
        if (!otp.trim()) {
          alert('Delivery OTP cannot be empty.');
          return;
        }
      }

      await axios.put(`/donations/${id}`, { status, otp: otp ? otp.trim() : undefined });
      fetchTasks();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to update task status');
    }
  };

  const logout = () => {
    localStorage.clear();
    navigate('/login');
  };

  return (
    <div className="dashboard">
      <header>
        <h2>Volunteer Dashboard</h2>
        <button onClick={logout}>Logout</button>
      </header>

      <section className="tasks-list">
        <h3>Available Pickups</h3>
        <ul>
          {tasks.filter(t => t.status === 'Requested').map(t => (
            <li key={t.id}>
              <strong>{t.foodDetails}</strong> - {t.quantity}
              <br/> Status: <span className="status">{t.status}</span>
              <br/> From Donor: {t.donor?.name} | To NGO: {t.ngo?.name}
              <br/> <button onClick={() => handleStatusUpdate(t.id, 'Accepted')}>Accept Pickup</button>
            </li>
          ))}
        </ul>
      </section>

      <section className="tasks-list">
        <h3>My Deliveries</h3>
        <ul>
          {tasks.filter(t => t.volunteerId === user.id).map(t => (
            <li key={t.id}>
              <strong>{t.foodDetails}</strong> - {t.quantity}
              <br/> Status: <span className="status">{t.status}</span>
              <br/>
              {t.status === 'Accepted' && (
                <div style={{ marginTop: '10px' }}>
                  <button onClick={() => handleStatusUpdate(t.id, 'Picked Up')}>
                    Mark as Picked Up (Requires OTP)
                  </button>
                  <div className="otp-hint" style={{ marginTop: '4px' }}>
                    * Ask donor for their 4-digit Pickup OTP during physical handover
                  </div>
                </div>
              )}
              {t.status === 'Picked Up' && (
                <div style={{ marginTop: '10px' }}>
                  <button onClick={() => handleStatusUpdate(t.id, 'Delivered')}>
                    Mark as Delivered (Requires OTP)
                  </button>
                  <div className="otp-hint" style={{ marginTop: '4px' }}>
                    * Ask NGO representative for their 4-digit Delivery OTP upon delivery
                  </div>
                </div>
              )}
              {t.status === 'Delivered' && (
                <div style={{ marginTop: '6px', color: '#16a34a', fontWeight: 'bold' }}>
                  ✓ Successfully Delivered & Verified
                </div>
              )}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
};
export default VolunteerDashboard;
