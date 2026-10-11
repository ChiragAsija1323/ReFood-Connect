const request = require('supertest');
const app = require('../app');
const { sequelize } = require('../models');

beforeAll(async () => {
  await sequelize.sync({ force: true });
});

afterAll(async () => {
  await sequelize.close();
});

describe('Authentication & Authorization Integration Tests', () => {
  const testDonor = {
    name: 'Green Leaf Restaurant',
    email: 'donor@greenleaf.com',
    password: 'securePassword123',
    role: 'donor',
  };

  test('POST /api/auth/register - Successfully registers a new Food Donor', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .send(testDonor);

    expect(res.statusCode).toBe(201);
    expect(res.body).toHaveProperty('user');
    expect(res.body.user.email).toBe(testDonor.email);
    expect(res.body.user.role).toBe('donor');
    expect(res.body).toHaveProperty('token');
  });

  test('POST /api/auth/register - Rejects registration with duplicate email', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .send(testDonor);

    expect(res.statusCode).toBe(400);
    expect(res.body).toHaveProperty('error');
  });

  test('POST /api/auth/login - Successfully authenticates registered user and returns JWT token', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({
        email: testDonor.email,
        password: testDonor.password,
      });

    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('token');
    expect(res.body.user.email).toBe(testDonor.email);
  });

  test('POST /api/auth/login - Rejects invalid password with 401 Unauthorized', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({
        email: testDonor.email,
        password: 'WrongPassword999',
      });

    expect(res.statusCode).toBe(401);
    expect(res.body).toHaveProperty('error');
  });

  test('POST /api/auth/login - Rejects non-existent email with 404/401', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'nonexistent@nowhere.com',
        password: 'anyPassword',
      });

    expect([401, 404]).toContain(res.statusCode);
  });
});
