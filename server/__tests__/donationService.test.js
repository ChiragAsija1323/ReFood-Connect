const { sequelize, User, Donation } = require('../models');
const donationService = require('../services/donationService');

let donor, ngo, volunteer, admin;

beforeAll(async () => {
  await sequelize.sync({ force: true });
  donor = await User.create({ name: 'Unit Donor', email: 'unit_donor@test.com', password: 'hash', role: 'donor' });
  ngo = await User.create({ name: 'Unit NGO', email: 'unit_ngo@test.com', password: 'hash', role: 'ngo' });
  volunteer = await User.create({ name: 'Unit Vol', email: 'unit_vol@test.com', password: 'hash', role: 'volunteer' });
  admin = await User.create({ name: 'Unit Admin', email: 'unit_admin@test.com', password: 'hash', role: 'admin' });
});

afterAll(async () => {
  await sequelize.close();
});

describe('DonationService Direct Unit Tests (Mutation Killers)', () => {
  test('createDonation rejects null or whitespace-only foodDetails', async () => {
    await expect(donationService.createDonation(donor.id, null, '10', new Date())).rejects.toThrow('Food details are required');
    await expect(donationService.createDonation(donor.id, '', '10', new Date())).rejects.toThrow('Food details are required');
    await expect(donationService.createDonation(donor.id, '   ', '10', new Date())).rejects.toThrow('Food details are required');
  });

  test('createDonation rejects null or whitespace-only quantity', async () => {
    await expect(donationService.createDonation(donor.id, 'Food', null, new Date())).rejects.toThrow('Quantity is required');
    await expect(donationService.createDonation(donor.id, 'Food', '', new Date())).rejects.toThrow('Quantity is required');
    await expect(donationService.createDonation(donor.id, 'Food', '   ', new Date())).rejects.toThrow('Quantity is required');
  });

  test('createDonation rejects missing expiryTime', async () => {
    await expect(donationService.createDonation(donor.id, 'Food', '10', null)).rejects.toThrow('Expiry time is required');
    await expect(donationService.createDonation(donor.id, 'Food', '10', undefined)).rejects.toThrow('Expiry time is required');
  });

  test('createDonation trims input strings properly', async () => {
    const d = await donationService.createDonation(donor.id, '  Pulao  ', '  20 packs  ', new Date());
    expect(d.foodDetails).toBe('Pulao');
    expect(d.quantity).toBe('20 packs');
  });

  test('getDonationsByRole handles volunteer, admin and unknown roles', async () => {
    const volList = await donationService.getDonationsByRole(volunteer);
    expect(Array.isArray(volList)).toBe(true);

    const adminList = await donationService.getDonationsByRole(admin);
    expect(Array.isArray(adminList)).toBe(true);

    const unknownList = await donationService.getDonationsByRole({ role: 'unknown' });
    expect(unknownList).toEqual([]);
  });

  test('updateDonationStatus throws if donation does not exist', async () => {
    await expect(donationService.updateDonationStatus(99999, { status: 'Requested' })).rejects.toThrow('Donation not found');
  });

  test('updateDonationStatus rejects invalid status values', async () => {
    const d = await donationService.createDonation(donor.id, 'Apples', '5kg', new Date());
    await expect(donationService.updateDonationStatus(d.id, { status: 'BogusStatus' })).rejects.toThrow('Invalid status: BogusStatus');
  });

  test('updateDonationStatus enforces exact state machine progression error messages', async () => {
    const d = await donationService.createDonation(donor.id, 'Rice', '10kg', new Date());
    // Current is Available: cannot accept, pick up, or deliver
    await expect(donationService.updateDonationStatus(d.id, { status: 'Accepted' })).rejects.toThrow("Cannot accept pickup for donation with status 'Available'. Must be 'Requested'.");
    await expect(donationService.updateDonationStatus(d.id, { status: 'Picked Up' })).rejects.toThrow("Cannot mark picked up for donation with status 'Available'. Must be 'Accepted'.");
    await expect(donationService.updateDonationStatus(d.id, { status: 'Delivered' })).rejects.toThrow("Cannot mark delivered for donation with status 'Available'. Must be 'Picked Up'.");

    // Transition to Requested
    await donationService.updateDonationStatus(d.id, { status: 'Requested', ngoId: ngo.id });
    await expect(donationService.updateDonationStatus(d.id, { status: 'Requested' })).rejects.toThrow("Cannot request donation with status 'Requested'. Must be 'Available'.");
    await expect(donationService.updateDonationStatus(d.id, { status: 'Picked Up' })).rejects.toThrow("Cannot mark picked up for donation with status 'Requested'. Must be 'Accepted'.");

    // Transition to Accepted
    await donationService.updateDonationStatus(d.id, { status: 'Accepted', volunteerId: volunteer.id });
    await expect(donationService.updateDonationStatus(d.id, { status: 'Delivered' })).rejects.toThrow("Cannot mark delivered for donation with status 'Accepted'. Must be 'Picked Up'.");

    // Transition to Picked Up
    await donationService.updateDonationStatus(d.id, { status: 'Picked Up' });

    // Transition to Delivered
    const finalDonation = await donationService.updateDonationStatus(d.id, { status: 'Delivered' });
    expect(finalDonation.status).toBe('Delivered');
  });
});
