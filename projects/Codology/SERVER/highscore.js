// highscore.js
const { DataTypes } = require('sequelize');
const sequelize = require('./database');
const User = require('./user.js')




// HIGHSCORES SQL MODEL 
const Highscore = sequelize.define('highscores', {
    username: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    score: {
        type: DataTypes.INTEGER,
        allowNull: false,
    },
    time: {
        type: DataTypes.INTEGER,
        allowNull: false,
    },
    timestamp: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW,
    },
});



const addHighScore = async (req, res, next) => {
    try {
        // CHECK IF USER IN DATABASE
        const dbUser = await User.findOne({
            where: {
                username: req.body.username,
            }
        });
        if (!dbUser) {
            return res.status(404).json({ message: "user not found" });
        }

        // CREATE HIGHSCORES IN DATABASE
        await Highscore.create({
            username: req.body.username,
            score: req.body.score,
            time: req.body.time,
            timestamp: req.body.timestamp,
        });
        // RETURN SUCCESS!
        return res.status(200).json({ message: "successful post" });



    // FAILURE CATCH
    } catch (error) {
        console.error('Error:', error);
        return res.status(500).json({ message: "internal server error" });
    }
}



const displayHighScores = (req, res, next) => {
    return res.status(200).json({ message: Highscore.findAll() });
}






module.exports = { Highscore, addHighScore, displayHighScores };
