const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');
const User = require('./User');

const Donation = sequelize.define('Donation', {
  id: {
    type: DataTypes.INTEGER,
    autoIncrement: true,
    primaryKey: true,
  },
  donorId: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: {
      model: User,
      key: 'id',
    },
  },
  ngoId: {
    type: DataTypes.INTEGER,
    allowNull: true,
    references: {
      model: User,
      key: 'id',
    },
  },
  volunteerId: {
    type: DataTypes.INTEGER,
    allowNull: true,
    references: {
      model: User,
      key: 'id',
    },
  },
  foodDetails: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  quantity: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  expiryTime: {
    type: DataTypes.DATE,
    allowNull: false,
  },
  status: {
    type: DataTypes.ENUM('Available', 'Requested', 'Accepted', 'Picked Up', 'Delivered'),
    defaultValue: 'Available',
  },
});

User.hasMany(Donation, { foreignKey: 'donorId', as: 'donations' });
Donation.belongsTo(User, { as: 'donor', foreignKey: 'donorId' });

User.hasMany(Donation, { foreignKey: 'ngoId', as: 'requests' });
Donation.belongsTo(User, { as: 'ngo', foreignKey: 'ngoId' });

User.hasMany(Donation, { foreignKey: 'volunteerId', as: 'tasks' });
Donation.belongsTo(User, { as: 'volunteer', foreignKey: 'volunteerId' });

module.exports = Donation;
