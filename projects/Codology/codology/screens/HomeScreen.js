import React, { useEffect, useMemo, useRef, useState } from 'react';
import {
    ActivityIndicator,
    Image,
    Pressable,
    StyleSheet,
    Text,
    TextInput,
    View,
} from 'react-native';
import { useNavigation } from '@react-navigation/core';
import axios from 'axios';

const API_URL = 'https://codology-api.vercel.app/api';

const questions = [
    {
        image: require('../assets/icon.png'),
        prompt: 'Which programming language does this question represent?',
        options: ['JavaScript', 'Python', 'Ruby', 'Java'],
        correctAnswer: 0,
    },
    {
        image: require('../assets/icon.png'),
        prompt: 'Which coding language is commonly used for AI and data science?',
        options: ['Swift', 'Python', 'PHP', 'Kotlin'],
        correctAnswer: 1,
    },
    {
        image: require('../assets/icon.png'),
        prompt: 'Which language is famous for Rails?',
        options: ['C#', 'Go', 'Ruby', 'TypeScript'],
        correctAnswer: 2,
    },
    {
        image: require('../assets/icon.png'),
        prompt: 'Which language runs on the JVM and is often taught in CS classes?',
        options: ['Rust', 'Elixir', 'Lua', 'Java'],
        correctAnswer: 3,
    },
];

const HomeScreen = () => {
    const navigation = useNavigation();
    const timerRef = useRef(null);
    const [questionIndex, setQuestionIndex] = useState(0);
    const [score, setScore] = useState(0);
    const [selectedOption, setSelectedOption] = useState(null);
    const [isGameStarted, setIsGameStarted] = useState(false);
    const [isGameOver, setIsGameOver] = useState(false);
    const [timer, setTimer] = useState(0);
    const [playerName, setPlayerName] = useState('');
    const [submitMessage, setSubmitMessage] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const finalScore = useMemo(() => score, [score]);

    useEffect(() => {
        return () => {
            if (timerRef.current) clearInterval(timerRef.current);
        };
    }, []);

    const startGame = () => {
        setQuestionIndex(0);
        setScore(0);
        setSelectedOption(null);
        setTimer(0);
        setPlayerName('');
        setSubmitMessage('');
        setIsGameOver(false);
        setIsGameStarted(true);

        if (timerRef.current) clearInterval(timerRef.current);
        timerRef.current = setInterval(() => {
            setTimer((prevTime) => prevTime + 1);
        }, 1000);
    };

    const finishGame = (nextScore) => {
        if (timerRef.current) clearInterval(timerRef.current);
        setScore(nextScore);
        setIsGameOver(true);
        setIsGameStarted(false);
        setSelectedOption(null);
    };

    const handleAnswerSelection = (selectedAnswerIndex) => {
        if (selectedOption !== null) return;

        const question = questions[questionIndex];
        const wasCorrect = selectedAnswerIndex === question.correctAnswer;
        const nextScore = wasCorrect ? score + 1 : score;

        setSelectedOption(selectedAnswerIndex);
        setScore(nextScore);

        setTimeout(() => {
            if (questionIndex < questions.length - 1) {
                setQuestionIndex(questionIndex + 1);
                setSelectedOption(null);
            } else {
                finishGame(nextScore);
            }
        }, 550);
    };

    const submitHighScore = async () => {
        const cleanName = playerName.trim();
        if (!cleanName) {
            setSubmitMessage('Type your name to join the leaderboard.');
            return;
        }

        setIsSubmitting(true);
        setSubmitMessage('');
        try {
            await axios.post(`${API_URL}/add-highscore`, {
                username: cleanName,
                score: finalScore,
                time: timer,
            });
            navigation.navigate('HighScores');
        } catch (error) {
            console.log('Error posting high score:', error);
            setSubmitMessage('Could not post your score. Try again.');
        } finally {
            setIsSubmitting(false);
        }
    };

    const question = questions[questionIndex];

    if (isGameOver) {
        return (
            <View style={styles.container}>
                <View style={styles.card}>
                    <Text style={styles.title}>Game Over</Text>
                    <Text style={styles.resultText}>Score: {finalScore} / {questions.length}</Text>
                    <Text style={styles.resultText}>Time: {timer} seconds</Text>
                    <Text style={styles.helperText}>Enter your name to post this run to the leaderboard.</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="Your name"
                        value={playerName}
                        onChangeText={setPlayerName}
                        maxLength={24}
                        autoCapitalize="words"
                    />
                    {submitMessage ? <Text style={styles.message}>{submitMessage}</Text> : null}
                    <Pressable
                        style={[styles.primaryButton, isSubmitting && styles.disabledButton]}
                        onPress={submitHighScore}
                        disabled={isSubmitting}
                    >
                        {isSubmitting ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Submit to Leaderboard</Text>}
                    </Pressable>
                    <Pressable style={styles.secondaryButton} onPress={startGame}>
                        <Text style={styles.secondaryButtonText}>Play Again</Text>
                    </Pressable>
                </View>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            {!isGameStarted ? (
                <View style={styles.card}>
                    <Text style={styles.title}>Codology</Text>
                    <Text style={styles.helperText}>Guess the coding language, race the clock, then add your name to the leaderboard.</Text>
                    <Pressable style={styles.primaryButton} onPress={startGame}>
                        <Text style={styles.buttonText}>Start Game</Text>
                    </Pressable>
                    <Pressable style={styles.secondaryButton} onPress={() => navigation.navigate('HighScores')}>
                        <Text style={styles.secondaryButtonText}>View Leaderboard</Text>
                    </Pressable>
                </View>
            ) : (
                <View style={styles.gameCard}>
                    <Text style={styles.timer}>Time: {timer} seconds</Text>
                    <Text style={styles.score}>Score: {score}</Text>
                    <Text style={styles.prompt}>{question.prompt}</Text>
                    <Image source={question.image} style={styles.image} />
                    <View style={styles.optionsContainer}>
                        {question.options.map((option, index) => {
                            const isSelected = selectedOption === index;
                            const isCorrect = selectedOption !== null && index === question.correctAnswer;
                            return (
                                <Pressable
                                    key={option}
                                    style={[
                                        styles.optionButton,
                                        isSelected && styles.buttonSelected,
                                        isCorrect && styles.buttonCorrect,
                                    ]}
                                    onPress={() => handleAnswerSelection(index)}
                                >
                                    <Text style={styles.buttonText}>{option}</Text>
                                </Pressable>
                            );
                        })}
                    </View>
                </View>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        padding: 20,
        backgroundColor: '#f4f1ff',
    },
    card: {
        width: '100%',
        maxWidth: 520,
        backgroundColor: '#ffffff',
        borderRadius: 24,
        padding: 24,
        alignItems: 'center',
        shadowColor: '#000',
        shadowOpacity: 0.12,
        shadowRadius: 12,
    },
    gameCard: {
        width: '100%',
        maxWidth: 760,
        backgroundColor: '#ffffff',
        borderRadius: 24,
        padding: 24,
        alignItems: 'center',
    },
    title: {
        color: 'darkslateblue',
        fontSize: 34,
        fontWeight: '800',
        marginBottom: 12,
    },
    helperText: {
        color: '#3d375c',
        fontSize: 17,
        textAlign: 'center',
        lineHeight: 24,
        marginBottom: 18,
    },
    timer: {
        fontSize: 18,
        fontWeight: '700',
        marginBottom: 4,
    },
    score: {
        fontSize: 18,
        fontWeight: '700',
        marginBottom: 16,
    },
    prompt: {
        fontSize: 22,
        fontWeight: '700',
        textAlign: 'center',
        marginBottom: 16,
        color: '#241a4a',
    },
    image: {
        width: 180,
        height: 180,
        resizeMode: 'contain',
        marginBottom: 22,
    },
    optionsContainer: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        justifyContent: 'center',
        gap: 12,
        width: '100%',
    },
    optionButton: {
        minWidth: 145,
        backgroundColor: '#333',
        borderRadius: 20,
        paddingVertical: 14,
        paddingHorizontal: 18,
        alignItems: 'center',
        justifyContent: 'center',
    },
    buttonSelected: {
        backgroundColor: '#b64242',
    },
    buttonCorrect: {
        backgroundColor: '#18884f',
    },
    primaryButton: {
        width: '100%',
        backgroundColor: 'darkslateblue',
        borderRadius: 25,
        paddingVertical: 15,
        paddingHorizontal: 20,
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 8,
    },
    secondaryButton: {
        width: '100%',
        borderColor: 'darkslateblue',
        borderWidth: 2,
        borderRadius: 25,
        paddingVertical: 13,
        paddingHorizontal: 20,
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 12,
    },
    disabledButton: {
        opacity: 0.6,
    },
    buttonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: '700',
    },
    secondaryButtonText: {
        color: 'darkslateblue',
        fontSize: 16,
        fontWeight: '700',
    },
    resultText: {
        fontSize: 20,
        fontWeight: '700',
        marginBottom: 8,
    },
    input: {
        width: '100%',
        borderColor: '#c9c1ed',
        borderWidth: 2,
        borderRadius: 16,
        paddingVertical: 12,
        paddingHorizontal: 14,
        fontSize: 18,
        marginBottom: 8,
    },
    message: {
        color: '#b64242',
        fontWeight: '700',
        marginBottom: 6,
    },
});

export default HomeScreen;
