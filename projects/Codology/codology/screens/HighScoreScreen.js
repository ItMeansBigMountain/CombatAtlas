import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View, Image } from 'react-native';
import { useNavigation } from '@react-navigation/core';


import AsyncStorage from '@react-native-async-storage/async-storage';



const API_URL = 'http://192.168.1.94:5000';





const HighScoreScreen = () => {


    const navigation = useNavigation();


    // on render, check if user is logged in or not
    useEffect(() => {
        const onRender = () => fetchHS()
        onRender();
    }, []);



    // EDIT FOR HIGH SCORES DISPLAY
    const fetchHS = () => {
        fetch(`${API_URL}/highscores`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            // body: JSON.stringify(payload),
        })
            .then(async res => {
                try {
                    const jsonRes = await res.json();
                    if (res.status !== 200) {
                        console.log(jsonRes.message);
                    } else {
                        console.log(jsonRes.message);
                    }
                } catch (err) {
                    console.log(err);
                };
            })
            .catch(err => {
                console.log(err);
            });
    };




    return (
        <div>HighScoreScreen</div>
    )
}





export default HighScoreScreen