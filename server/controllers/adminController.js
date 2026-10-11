const adminService = require('../services/adminService');

exports.getDashboardData = async (req, res) => {
  try {
    if (req.user.role !== 'admin') {
      return res.status(403).json({ error: 'Forbidden: Administrator access required' });
    }

    const data = await adminService.getSystemStats();
    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
