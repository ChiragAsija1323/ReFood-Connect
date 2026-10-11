const request = require('supertest');
const app = require('../app');
const { sequelize, User, Donation } = require('../models');

let donorToken, ngoToken, volunteerToken;
let donorUser, ngoUser, volunteerUser;
let createdDonationId;

beforeAll(async () => {
  await sequelize.sync({ force: true });

  // 1. Create Donor
  const donorRes = await request(app).post('/api/auth/register').send({
    name: 'Spice Garden Hotel',
    email: 'spice@hotel.com',
    password: 'password123',
    role: 'donor',
  });
  donorToken = donorRes.body.token;
  donorUser = donorRes.body.user;

  // 2. Create NGO
  const ngoRes = await request(app).post('/api/auth/register').send({
    name: 'Hope Food Bank',
    email: 'hope@ngo.org',
    password: 'password123',
    role: 'ngo',
  });
  ngoToken = ngoRes.body.token;
  ngoUser = ngoRes.body.user;

  // 3. Create Volunteer
  const volRes = await request(app).post('/api/auth/register').send({
    name: 'Alex Transport Volunteer',
    email: 'alex@volunteer.org',
    password: 'password123',
    role: 'volunteer',
  });
  volunteerToken = volRes.body.token;
  volunteerUser = volRes.body.user;
});

afterAll(async () => {
  await sequelize.close();
});

describe('Donations End-to-End Workflow Integration Tests', () => {
  test('POST /api/donations - Food Donor creates a surplus food listing (Status: Available)', async () => {
    const res = await request(app)
      .post('/api/donations')
      .set('Authorization', `Bearer ${donorToken}`)
      .send({
        foodDetails: '40 Packets of Biryani & Curd Rice',
        quantity: '40 meals',
        expiryTime: new Date(Date.now() + 6 * 3600 * 1000).toISOString(),
      });

    expect(res.statusCode).toBe(201);
    expect(res.body).toHaveProperty('id');
    expect(res.body.foodDetails).toBe('40 Packets of Biryani & Curd Rice');
    expect(res.body.status).toBe('Available');
    expect(res.body.donorId).toBe(donorUser.id);
    createdDonationId = res.body.id;
  });

  test('GET /api/donations - NGO retrieves available food donation listings', async () => {
    const res = await request(app)
      .get('/api/donations')
      .set('Authorization', `Bearer ${ngoToken}`);

    expect(res.statusCode).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
    expect(res.body.length).toBeGreaterThanOrEqual(1);
    expect(res.body.some(d => d.id === createdDonationId)).toBe(true);
  });

  test('PUT /api/donations/:id - NGO claims/requests the donation (Status transitions to Requested)', async () => {
    const res = await request(app)
      .put(`/api/donations/${createdDonationId}`)
      .set('Authorization', `Bearer ${ngoToken}`)
      .send({ status: 'Requested' });

    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('Requested');
    expect(res.body.ngoId).toBe(ngoUser.id);
  });

  test('PUT /api/donations/:id - Volunteer accepts the transport task (Status transitions to Accepted)', async () => {
    const res = await request(app)
      .put(`/api/donations/${createdDonationId}`)
      .set('Authorization', `Bearer ${volunteerToken}`)
      .send({ status: 'Accepted' });

    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('Accepted');
    expect(res.body.volunteerId).toBe(volunteerUser.id);
  });

  test('PUT /api/donations/:id - Volunteer updates transit to Picked Up', async () => {
    const res = await request(app)
      .put(`/api/donations/${createdDonationId}`)
      .set('Authorization', `Bearer ${volunteerToken}`)
      .send({ status: 'Picked Up' });

    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('Picked Up');
  });

  test('PUT /api/donations/:id - Volunteer confirms final handover to Delivered', async () => {
    const res = await request(app)
      .put(`/api/donations/${createdDonationId}`)
      .set('Authorization', `Bearer ${volunteerToken}`)
      .send({ status: 'Delivered' });

    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('Delivered');
  });

  test('Database Persistence Verification - Querying database directly confirms final Delivered state', async () => {
    const record = await Donation.findByPk(createdDonationId);
    expect(record).not.toBeNull();
    expect(record.status).toBe('Delivered');
    expect(record.donorId).toBe(donorUser.id);
    expect(record.ngoId).toBe(ngoUser.id);
    expect(record.volunteerId).toBe(volunteerUser.id);
  });
});
