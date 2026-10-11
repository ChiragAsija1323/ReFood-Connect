const donationService = require('../services/donationService');

exports.createDonation = async (req, res) => {
  try {
    if (req.user.role !== 'donor' && req.user.role !== 'admin') {
      return res.status(403).json({ error: 'Only donors can create donations' });
    }
    const { foodDetails, quantity, expiryTime } = req.body;
    const donorId = req.user.id;
    const donation = await donationService.createDonation(donorId, foodDetails, quantity, expiryTime);
    res.status(201).json(donation);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

exports.getDonations = async (req, res) => {
  try {
    const donations = await donationService.getDonationsByRole(req.user);
    res.status(200).json(donations);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

exports.updateDonation = async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;

    if (updates.status === 'Requested' && req.user.role !== 'ngo' && req.user.role !== 'admin') {
      return res.status(403).json({ error: 'Only NGOs can request donations' });
    }

    if (['Accepted', 'Picked Up', 'Delivered'].includes(updates.status) && req.user.role !== 'volunteer' && req.user.role !== 'admin') {
      return res.status(403).json({ error: 'Only volunteers can accept or update delivery tasks' });
    }
    
    // Auto-assign user ids based on role and status change
    if (updates.status === 'Requested' && req.user.role === 'ngo') {
      updates.ngoId = req.user.id;
    }
    if (updates.status === 'Accepted' && req.user.role === 'volunteer') {
      updates.volunteerId = req.user.id;
    }

    const donation = await donationService.updateDonationStatus(id, updates);
    res.status(200).json(donation);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};
