const { Sequelize } = require('sequelize');
const mysql2 = require('mysql2');

const databaseUrl = process.env.DATABASE_URL || process.env.MYSQL_URL;

const sequelize = databaseUrl
    ? new Sequelize(databaseUrl, {
        dialect: 'mysql',
        dialectModule: mysql2,
        logging: false,
    })
    : new Sequelize(
        process.env.MYSQL_DATABASE || 'Codology',
        process.env.MYSQL_USER || 'root',
        process.env.MYSQL_PASSWORD || 'YOUR_DB_PASSWORD',
        {
            dialect: 'mysql',
            dialectModule: mysql2,
            host: process.env.MYSQL_HOST || 'localhost',
            logging: false,
        }
    );

module.exports = sequelize;
