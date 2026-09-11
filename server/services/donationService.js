const { Donation, User } = require('../models');

class DonationService {
  async createDonation(donorId, foodDetails, quantity, expiryTime) {
    return await Donation.create({
      donorId,
      foodDetails,
      quantity,
      expiryTime,
      status: 'Available'
    });
  }

  async getDonationsByRole(user) {
    if (user.role === 'donor') {
      return await Donation.findAll({ where: { donorId: user.id }, include: ['ngo', 'volunteer'] });
    } else if (user.role === 'ngo') {
      // NGOs see available donations + their own requested/accepted ones
      return await Donation.findAll({
        include: ['donor', 'volunteer']
      });
    } else if (user.role === 'volunteer') {
      return await Donation.findAll({
        include: ['donor', 'ngo']
      });
    }
    return [];
  }

  async updateDonationStatus(donationId, updates) {
    const donation = await Donation.findByPk(donationId);
    if (!donation) throw new Error('Donation not found');
    
    return await donation.update(updates);
  }
}

module.exports = new DonationService();
