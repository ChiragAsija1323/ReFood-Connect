const { Donation, User } = require('../models');

const generateOtp = () => Math.floor(1000 + Math.random() * 9000).toString();

class DonationService {
  async createDonation(donorId, foodDetails, quantity, expiryTime) {
    if (!foodDetails || foodDetails.trim() === '') {
      throw new Error('Food details are required');
    }
    if (!quantity || quantity.trim() === '') {
      throw new Error('Quantity is required');
    }
    if (!expiryTime) {
      throw new Error('Expiry time is required');
    }

    const pickupOtp = generateOtp();

    return await Donation.create({
      donorId,
      foodDetails: foodDetails.trim(),
      quantity: quantity.trim(),
      expiryTime,
      status: 'Available',
      pickupOtp,
    });
  }

  async getDonationsByRole(user) {
    if (user.role === 'donor') {
      return await Donation.findAll({ where: { donorId: user.id }, include: ['ngo', 'volunteer'] });
    } else if (user.role === 'ngo') {
      return await Donation.findAll({
        include: ['donor', 'volunteer']
      });
    } else if (user.role === 'volunteer') {
      return await Donation.findAll({
        include: ['donor', 'ngo']
      });
    } else if (user.role === 'admin') {
      return await Donation.findAll({
        include: ['donor', 'ngo', 'volunteer']
      });
    }
    return [];
  }

  async updateDonationStatus(donationId, updates) {
    const donation = await Donation.findByPk(donationId);
    if (!donation) throw new Error('Donation not found');

    const validStatuses = ['Available', 'Requested', 'Accepted', 'Picked Up', 'Delivered'];
    if (updates.status && !validStatuses.includes(updates.status)) {
      throw new Error(`Invalid status: ${updates.status}`);
    }

    // State machine progression validation
    if (updates.status === 'Requested') {
      if (donation.status !== 'Available') {
        throw new Error(`Cannot request donation with status '${donation.status}'. Must be 'Available'.`);
      }
      // Generate delivery OTP when claimed by NGO
      updates.deliveryOtp = generateOtp();
    } else if (updates.status === 'Accepted') {
      if (donation.status !== 'Requested') {
        throw new Error(`Cannot accept pickup for donation with status '${donation.status}'. Must be 'Requested'.`);
      }
    } else if (updates.status === 'Picked Up') {
      if (donation.status !== 'Accepted') {
        throw new Error(`Cannot mark picked up for donation with status '${donation.status}'. Must be 'Accepted'.`);
      }
      // Digital Handshake: Physical Pickup OTP Verification
      if (donation.pickupOtp) {
        if (!updates.otp || updates.otp.toString().trim() !== donation.pickupOtp) {
          throw new Error('Invalid Pickup OTP. Physical verification failed.');
        }
      }
    } else if (updates.status === 'Delivered') {
      if (donation.status !== 'Picked Up') {
        throw new Error(`Cannot mark delivered for donation with status '${donation.status}'. Must be 'Picked Up'.`);
      }
      // Digital Handshake: Physical Delivery OTP Verification
      if (donation.deliveryOtp) {
        if (!updates.otp || updates.otp.toString().trim() !== donation.deliveryOtp) {
          throw new Error('Invalid Delivery OTP. Physical verification failed.');
        }
      }
    }
    
    const updatePayload = { ...updates };
    delete updatePayload.otp;
    return await donation.update(updatePayload);
  }
}

module.exports = new DonationService();
