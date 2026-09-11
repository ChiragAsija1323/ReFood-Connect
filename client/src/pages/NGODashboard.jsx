import { useState, useEffect } from 'react';
import axios from '../api/axios';
import { useNavigate } from 'react-router-dom';

const NGODashboard = () => {
  const [donations, setDonations] = useState([]);
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user'));

  const fetchDonations = async () => {
    const { data } = await axios.get('/donations');
    setDonations(data);
  };

  useEffect(() => {
    fetchDonations();
  }, []);

  const handleRequest = async (id) => {
    await axios.put(`/donations/${id}`, { status: 'Requested' });
    fetchDonations();
  };

  const logout = () => {
    localStorage.clear();
    navigate('/login');
  };

  return (
    <div className="dashboard">
      <header>
        <h2>NGO Dashboard</h2>
        <button onClick={logout}>Logout</button>
      </header>

      <section className="donations-list">
        <h3>Available Donations</h3>
        <ul>
          {donations.filter(d => d.status === 'Available').map(d => (
            <li key={d.id}>
              <strong>{d.foodDetails}</strong> - {d.quantity}
              <br/> Status: <span className="status">{d.status}</span>
              <br/> <button onClick={() => handleRequest(d.id)}>Request Donation</button>
            </li>
          ))}
        </ul>
      </section>

      <section className="donations-list">
        <h3>My Requests</h3>
        <ul>
          {donations.filter(d => d.ngoId === user.id).map(d => (
            <li key={d.id}>
              <strong>{d.foodDetails}</strong> - {d.quantity}
              <br/> Status: <span className="status">{d.status}</span>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
};
export default NGODashboard;
