const sequelize = require('../config/database');
const User = require('./User');
const Donation = require('./Donation');

module.exports = {
  sequelize,
  User,
  Donation
};
