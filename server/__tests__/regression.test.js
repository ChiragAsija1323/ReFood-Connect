const request = require('supertest');
const app = require('../app');
const { sequelize, User, Donation } = require('../models');

let donorToken, ngoToken, volunteerToken, adminToken;
let testDonationId;

beforeAll(async () => {
  await sequelize.sync({ force: true });

  const donorRes = await request(app).post('/api/auth/register').send({
    name: 'Reg Donor',
    email: 'reg_donor@test.com',
    password: 'password123',
    role: 'donor',
  });
  donorToken = donorRes.body.token;

  const ngoRes = await request(app).post('/api/auth/register').send({
    name: 'Reg NGO',
    email: 'reg_ngo@test.com',
    password: 'password123',
    role: 'ngo',
  });
  ngoToken = ngoRes.body.token;

  const volRes = await request(app).post('/api/auth/register').send({
    name: 'Reg Volunteer',
    email: 'reg_vol@test.com',
    password: 'password123',
    role: 'volunteer',
  });
  volunteerToken = volRes.body.token;

  const adminRes = await request(app).post('/api/auth/register').send({
    name: 'Reg Admin',
    email: 'reg_admin@test.com',
    password: 'password123',
    role: 'admin',
  });
  adminToken = adminRes.body.token;

  // Create an initial donation
  const donRes = await request(app)
    .post('/api/donations')
    .set('Authorization', `Bearer ${donorToken}`)
    .send({
      foodDetails: 'Test Surplus Meal',
      quantity: '15 boxes',
      expiryTime: new Date(Date.now() + 4 * 3600 * 1000).toISOString(),
    });
  testDonationId = donRes.body.id;
});

afterAll(async () => {
  await sequelize.close();
});

describe('Regression & Security Test Suite', () => {
  test('Regression 1: Non-admin users cannot access admin dashboard (RBAC Guard)', async () => {
    const res = await request(app)
      .get('/api/admin/dashboard')
      .set('Authorization', `Bearer ${donorToken}`);

    expect(res.statusCode).toBe(403);
    expect(res.body.error).toMatch(/Administrator access required/i);
  });

  test('Regression 2: Admin user successfully retrieves complete system statistics', async () => {
    const res = await request(app)
      .get('/api/admin/dashboard')
      .set('Authorization', `Bearer ${adminToken}`);

    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('stats');
    expect(res.body.stats.totalUsers).toBeGreaterThanOrEqual(4);
    expect(res.body.stats.totalDonations).toBeGreaterThanOrEqual(1);
    expect(Array.isArray(res.body.donations)).toBe(true);
    expect(Array.isArray(res.body.users)).toBe(true);
  });

  test('Regression 3: Food creation requires non-empty foodDetails and quantity', async () => {
    const res = await request(app)
      .post('/api/donations')
      .set('Authorization', `Bearer ${donorToken}`)
      .send({
        foodDetails: '   ',
        quantity: '',
        expiryTime: new Date().toISOString(),
      });

    expect(res.statusCode).toBe(400);
    expect(res.body).toHaveProperty('error');
  });

  test('Regression 4: Non-donor cannot create food donations', async () => {
    const res = await request(app)
      .post('/api/donations')
      .set('Authorization', `Bearer ${ngoToken}`)
      .send({
        foodDetails: 'Unauthorized attempt',
        quantity: '10 meals',
        expiryTime: new Date().toISOString(),
      });

    expect(res.statusCode).toBe(403);
  });

  test('Regression 5: State Machine prevents skipping phases (Available cannot jump to Delivered)', async () => {
    const res = await request(app)
      .put(`/api/donations/${testDonationId}`)
      .set('Authorization', `Bearer ${volunteerToken}`)
      .send({ status: 'Delivered' });

    expect(res.statusCode).toBe(400);
    expect(res.body.error).toMatch(/Cannot mark delivered/i);
  });

  test('Regression 6: State Machine prevents invalid status string', async () => {
    const res = await request(app)
      .put(`/api/donations/${testDonationId}`)
      .set('Authorization', `Bearer ${volunteerToken}`)
      .send({ status: 'InvalidStatusXYZ' });

    expect(res.statusCode).toBe(400);
    expect(res.body.error).toMatch(/Invalid status/i);
  });

  test('Regression 7: Unauthenticated requests are rejected with 401', async () => {
    const res = await request(app).get('/api/donations');
    expect(res.statusCode).toBe(401);
  });
});
