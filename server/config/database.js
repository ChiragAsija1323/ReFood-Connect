const { Sequelize } = require('sequelize');
require('dotenv').config();

let sequelize;

if (process.env.NODE_ENV === 'test') {
  sequelize = new Sequelize('sqlite::memory:', {
    logging: false,
  });
} else {
  sequelize = new Sequelize(
    process.env.DB_NAME || 'refood_connect',
    process.env.DB_USER || 'root',
    process.env.DB_PASSWORD || '',
    {
      host: process.env.DB_HOST || 'localhost',
      dialect: 'mysql',
      port: process.env.DB_PORT || 3306,
      logging: false,
    }
  );
}

module.exports = sequelize;
