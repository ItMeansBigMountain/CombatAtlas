import React, { useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View, Image } from 'react-native';
import { useNavigation } from '@react-navigation/core';

// FETCH URL CALLS
import axios from 'axios';


// IN MEMORY DATA 
import AsyncStorage from '@react-native-async-storage/async-storage';



const API_URL = 'https://codology-api.vercel.app/api';



const HomeScreen = () => {
    const [questionIndex, setQuestionIndex] = useState(0);
    const [score, setScore] = useState(0);
    const [selectedOption, setSelectedOption] = useState(null);
    const [isGameStarted, setIsGameStarted] = useState(false);
    const [timer, setTimer] = useState(0);

    const navigation = useNavigation();


    const questions = [
        {
            image: require('../assets/icon.png'),
            options: ['JavaScript', 'Python', 'Ruby', 'Java'],
            correctAnswer: 0,
        },
        {
            image: require('../assets/icon.png'),
            options: ['JavaScript', 'Python', 'Ruby', 'Java'],
            correctAnswer: 1,
        },
        {
            image: require('../assets/icon.png'),
            options: ['JavaScript', 'Python', 'Ruby', 'Java'],
            correctAnswer: 2,
        },
        {
            image: require('../assets/icon.png'),
            options: ['JavaScript', 'Python', 'Ruby', 'Java'],
            correctAnswer: 3,
        },
        // ... more questions
    ];

    const startGame = () => {
        setIsGameStarted(true);
        // Start the timer
        setInterval(() => {
            setTimer((prevTime) => prevTime + 1);
        }, 1000);
    };


    const endGame = async (score, time) => {
        try {
            const highScoreData = {
                username: "sosai", // Replace with actual username
                score: score,
                time: time
            };

            const response = await axios.post(`${API_URL}/add-highscore`, highScoreData);

            if (response.status === 200) {
                console.log("High score successfully posted.");
            }
        } catch (error) {
            console.log("Error posting high score:", error);
        }
    };


    const handleAnswerSelection = (selectedAnswerIndex) => {
        setSelectedOption(selectedAnswerIndex);

        const question = questions[questionIndex];
        if (selectedAnswerIndex === question.correctAnswer) {
            setScore(score + 1); // Increase score for correct answer
            alert('Correct!');
        } else {
            alert('Incorrect!');
        }

        // Move to the next question or end the game if it was the last question
        if (questionIndex < questions.length - 1) {
            setQuestionIndex(questionIndex + 1);
        } else {
            endGame(score, timer);
        }
    };

    const question = questions[questionIndex];

    return (
        <View style={styles.container}>
            {!isGameStarted ? (
                <TouchableOpacity style={styles.startButton} onPress={startGame}>
                    <Text style={styles.buttonText}>Start Game!</Text>
                </TouchableOpacity>
            ) : (
                <>
                    <Text style={styles.timer}>Time: {timer} seconds</Text>
                    <Image source={question.image} style={styles.image} />
                    <View style={styles.optionsContainer}>
                        {question.options.map((option, index) => (
                            <TouchableOpacity
                                key={index}
                                style={[
                                    styles.button,
                                    selectedOption === index && styles.buttonSelected,
                                ]}
                                onPress={() => handleAnswerSelection(index)}>
                                <Text style={styles.buttonText}>{option}</Text>
                            </TouchableOpacity>
                        ))}
                    </View>
                </>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
    startButton: {
        backgroundColor: 'darkslateblue',
        borderRadius: 25,
        paddingVertical: 15,
        paddingHorizontal: 20,
        alignItems: 'center',
        justifyContent: 'center',
    },
    timer: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    image: {
        width: '70%',
        height: '70%',
        resizeMode: 'cover',
    },
    optionsContainer: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        width: '100%',
    },
    button: {
        width: '20%',
        backgroundColor: '#333',
        borderRadius: 25,
        paddingVertical: 10,
        paddingHorizontal: 5,
        alignItems: 'center',
        justifyContent: 'center',
    },
    buttonSelected: {
        backgroundColor: '#1e90ff',
    },
    buttonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: '400',
    },
});

export default HomeScreen;
