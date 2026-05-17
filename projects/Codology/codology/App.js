import React, { useState, useEffect } from 'react';


import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, Button } from 'react-native';

// react navigator
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

// Screen Components
import LoginScreen from './screens/LoginScreen';
import HomeScreen from './screens/HomeScreen';


import AsyncStorage from '@react-native-async-storage/async-storage';
import HighScoreScreen from './screens/HighScoreScreen';



// screen navigation init stack
const Stack = createNativeStackNavigator();


function App() {

  const handleSignOut = async (navigation) => {
    try {
      // You'll need to handle the sign-out logic here (e.g., call your auth.signOut())
      await AsyncStorage.removeItem('userToken'); // Remove token from AsyncStorage
      navigation.replace("Login"); // Navigate to login screen
    } catch (error) {
      alert(error.message);
    }
  };


  return (
    <NavigationContainer>

      {/* creates a stack of screens to navigate through */}
      <Stack.Navigator>

        {/* LOGIN PAGE */}
        < Stack.Screen name="Login" options={{ headerShown: false }} component={LoginScreen} />

        {/* HOMESCREEN PAGE  */}
        <Stack.Screen name="Home" component={HomeScreen}
          options={({ navigation }) => ({
            headerStyle: { backgroundColor: 'darkslateblue' },
            headerRight: () => (
              <Button title="Sign Out" color="#000000"
                onPress={() => handleSignOut(navigation)}
              />
            ),
            headerLeft: () => (
              <Button title="HighScores" color="#000000"
                onPress={() => console.log("stats!")} />
            ),
          })}
        />

        {/* HIGH SCORES PAGE */}
        < Stack.Screen name="HighScores" options={{ headerShown: false }} component={HighScoreScreen} />

      </Stack.Navigator>

    </NavigationContainer>
  );
}






const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
export default App;