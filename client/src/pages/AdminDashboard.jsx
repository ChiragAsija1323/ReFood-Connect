import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

const AdminDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const res = await api.get('/admin/dashboard');
      setData(res.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch administrator data');
      if (err.response?.status === 401 || err.response?.status === 403) {
        setTimeout(() => navigate('/login'), 2000);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'Available':
        return 'badge-available';
      case 'Requested':
        return 'badge-requested';
      case 'Accepted':
        return 'badge-accepted';
      case 'Picked Up':
        return 'badge-transit';
      case 'Delivered':
        return 'badge-delivered';
      default:
        return 'badge-default';
    }
  };

  if (loading) {
    return <div className="dashboard-container"><p className="loading-text">Loading Administrator Dashboard...</p></div>;
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <div>
          <h2>System Administration Portal</h2>
          <p className="dashboard-subtitle">Platform Governance & Real-Time Redistribution Analytics</p>
        </div>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {data && (
        <>
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-label">Total Users</span>
              <span className="stat-value">{data.stats?.totalUsers || 0}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Total Donations</span>
              <span className="stat-value">{data.stats?.totalDonations || 0}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Active Redistribution</span>
              <span className="stat-value">{data.stats?.activeDonations || 0}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Successfully Delivered</span>
              <span className="stat-value stat-delivered">{data.stats?.deliveredDonations || 0}</span>
            </div>
          </div>

          <section className="section-block">
            <div className="section-header">
              <h3>All Food Donations</h3>
              <button onClick={fetchDashboardData} className="refresh-btn">Refresh</button>
            </div>
            <div className="table-responsive">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Donor</th>
                    <th>Food Details</th>
                    <th>Quantity</th>
                    <th>Expiry Time</th>
                    <th>Status</th>
                    <th>OTP Handshake</th>
                    <th>Assigned NGO</th>
                    <th>Assigned Volunteer</th>
                  </tr>
                </thead>
                <tbody>
                  {data.donations && data.donations.length > 0 ? (
                    data.donations.map((d) => (
                      <tr key={d.id}>
                        <td>#{d.id}</td>
                        <td>{d.donor?.name || 'Unknown'}</td>
                        <td><strong>{d.foodDetails}</strong></td>
                        <td>{d.quantity}</td>
                        <td>{new Date(d.expiryTime).toLocaleString()}</td>
                        <td>
                          <span className={`status-badge ${getStatusBadgeClass(d.status)}`}>
                            {d.status}
                          </span>
                        </td>
                        <td>
                          <span style={{ fontSize: '12px', fontFamily: 'monospace', color: '#475569' }}>
                            P: <strong style={{ color: '#1d4ed8' }}>{d.pickupOtp || '-'}</strong> | D: <strong style={{ color: '#16a34a' }}>{d.deliveryOtp || '-'}</strong>
                          </span>
                        </td>
                        <td>{d.ngo?.name || '-'}</td>
                        <td>{d.volunteer?.name || '-'}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="9" style={{ textAlign: 'center' }}>No donation records found.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>

          <section className="section-block">
            <div className="section-header">
              <h3>Registered Platform Users</h3>
            </div>
            <div className="table-responsive">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Full Name</th>
                    <th>Email Address</th>
                    <th>System Role</th>
                    <th>Joined Date</th>
                  </tr>
                </thead>
                <tbody>
                  {data.users && data.users.length > 0 ? (
                    data.users.map((u) => (
                      <tr key={u.id}>
                        <td>#{u.id}</td>
                        <td>{u.name}</td>
                        <td>{u.email}</td>
                        <td>
                          <span className={`role-badge role-${u.role}`}>
                            {u.role.toUpperCase()}
                          </span>
                        </td>
                        <td>{new Date(u.createdAt).toLocaleDateString()}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="5" style={{ textAlign: 'center' }}>No registered users found.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>
        </>
      )}
    </div>
  );
};

export default AdminDashboard;
