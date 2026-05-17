const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('Codology', 'root', 'YOUR_DB_PASSWORD', {
    dialect: 'mysql',
    host: 'localhost', 
});

module.exports = sequelize;
