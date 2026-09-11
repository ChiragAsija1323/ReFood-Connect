import { useState, useEffect } from 'react';
import axios from '../api/axios';
import { useNavigate } from 'react-router-dom';

const DonorDashboard = () => {
  const [donations, setDonations] = useState([]);
  const [foodDetails, setFoodDetails] = useState('');
  const [quantity, setQuantity] = useState('');
  const [expiryTime, setExpiryTime] = useState('');
  const navigate = useNavigate();

  const fetchDonations = async () => {
    const { data } = await axios.get('/donations');
    setDonations(data);
  };

  useEffect(() => {
    fetchDonations();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    await axios.post('/donations', { foodDetails, quantity, expiryTime });
    setFoodDetails(''); setQuantity(''); setExpiryTime('');
    fetchDonations();
  };

  const logout = () => {
    localStorage.clear();
    navigate('/login');
  };

  return (
    <div className="dashboard">
      <header>
        <h2>Donor Dashboard</h2>
        <button onClick={logout}>Logout</button>
      </header>

      <section className="create-donation">
        <h3>Create Donation</h3>
        <form onSubmit={handleCreate}>
          <input type="text" placeholder="Food Details (e.g. Vegetable Biryani)" value={foodDetails} onChange={e=>setFoodDetails(e.target.value)} required />
          <input type="text" placeholder="Quantity (e.g. 20 meals)" value={quantity} onChange={e=>setQuantity(e.target.value)} required />
          <input type="datetime-local" value={expiryTime} onChange={e=>setExpiryTime(e.target.value)} required />
          <button type="submit">Donate Food</button>
        </form>
      </section>

      <section className="donations-list">
        <h3>My Donations</h3>
        <ul>
          {donations.map(d => (
            <li key={d.id}>
              <strong>{d.foodDetails}</strong> - {d.quantity}
              <br/> Status: <span className="status">{d.status}</span>
              <br/> Expiry: {new Date(d.expiryTime).toLocaleString()}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
};
export default DonorDashboard;
