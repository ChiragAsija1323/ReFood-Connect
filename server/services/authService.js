const { User } = require('../models');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

class AuthService {
  async register(name, email, password, role) {
    const existingUser = await User.findOne({ where: { email } });
    if (existingUser) {
      throw new Error('User already exists');
    }
    const hashedPassword = await bcrypt.hash(password, 10);
    const user = await User.create({
      name,
      email,
      password: hashedPassword,
      role
    });
    const secret = process.env.JWT_SECRET || 'refood_connect_jwt_secret_key_2026';
    const token = jwt.sign(
      { id: user.id, role: user.role, name: user.name },
      secret,
      { expiresIn: '1d' }
    );
    return { user, token };
  }

  async login(email, password) {
    const user = await User.findOne({ where: { email } });
    if (!user) {
      throw new Error('Invalid email or password');
    }
    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) {
      throw new Error('Invalid email or password');
    }
    const secret = process.env.JWT_SECRET || 'refood_connect_jwt_secret_key_2026';
    const token = jwt.sign(
      { id: user.id, role: user.role, name: user.name },
      secret,
      { expiresIn: '1d' }
    );
    return {
      token,
      user: { id: user.id, name: user.name, email: user.email, role: user.role }
    };
  }
}

module.exports = new AuthService();
