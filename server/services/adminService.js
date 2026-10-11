const { User, Donation } = require('../models');

class AdminService {
  async getSystemStats() {
    const userCount = await User.count();
    const donationCount = await Donation.count();

    const donations = await Donation.findAll({
      include: [
        { model: User, as: 'donor', attributes: ['id', 'name', 'email'] },
        { model: User, as: 'ngo', attributes: ['id', 'name', 'email'] },
        { model: User, as: 'volunteer', attributes: ['id', 'name', 'email'] },
      ],
      order: [['createdAt', 'DESC']],
    });

    const users = await User.findAll({
      attributes: ['id', 'name', 'email', 'role', 'createdAt'],
      order: [['createdAt', 'DESC']],
    });

    return {
      stats: {
        totalUsers: userCount,
        totalDonations: donationCount,
        activeDonations: donations.filter(d => ['Available', 'Requested', 'Accepted', 'Picked Up'].includes(d.status)).length,
        deliveredDonations: donations.filter(d => d.status === 'Delivered').length,
      },
      donations,
      users,
    };
  }
}

module.exports = new AdminService();
