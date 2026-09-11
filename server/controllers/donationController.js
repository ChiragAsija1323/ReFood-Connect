const donationService = require('../services/donationService');

exports.createDonation = async (req, res) => {
  try {
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
    const updates = req.body; // e.g., { status: 'Requested', ngoId: req.user.id }
    
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
