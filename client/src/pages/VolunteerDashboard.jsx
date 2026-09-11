import { useState, useEffect } from 'react';
import axios from '../api/axios';
import { useNavigate } from 'react-router-dom';

const VolunteerDashboard = () => {
  const [tasks, setTasks] = useState([]);
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user'));

  const fetchTasks = async () => {
    const { data } = await axios.get('/donations');
    setTasks(data);
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleStatusUpdate = async (id, status) => {
    await axios.put(`/donations/${id}`, { status });
    fetchTasks();
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
              {t.status === 'Accepted' && <button onClick={() => handleStatusUpdate(t.id, 'Picked Up')}>Mark as Picked Up</button>}
              {t.status === 'Picked Up' && <button onClick={() => handleStatusUpdate(t.id, 'Delivered')}>Mark as Delivered</button>}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
};
export default VolunteerDashboard;
