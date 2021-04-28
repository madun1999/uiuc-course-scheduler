/** Login Screen */
import * as React from 'react';
import { StyleSheet } from 'react-native';
import * as WebBrowser from 'expo-web-browser';
import * as Google from 'expo-auth-session/providers/google';
import { View } from '../components/Themed';
import AsyncStorage from '@react-native-async-storage/async-storage'
import {BottomTabParamList} from "../types";
import {BottomTabNavigationProp} from "@react-navigation/bottom-tabs";
import {Button, Title} from 'react-native-paper';
import {useContext} from "react";
import {UserContext} from "../contexts/UserContext";

// screen parameter type
type LoginScreenNavigationProp = BottomTabNavigationProp<BottomTabParamList, 'Login'>;
type LoginScreenProps = {
  navigation: LoginScreenNavigationProp,
};

// Return to this page when login web browser is closed
WebBrowser.maybeCompleteAuthSession();

export default function LoginScreen({ navigation } : LoginScreenProps) {
  // Google login
  const user = useContext(UserContext)
  const [request, response, promptAsync] = Google.useAuthRequest({
    responseType: "id_token",
    expoClientId: process.env.GOOGLE_APP_CLIENT_ID,
    iosClientId: process.env.GOOGLE_APP_CLIENT_ID,
    androidClientId: process.env.GOOGLE_APP_CLIENT_ID,
    webClientId: '399183208162-br9tdb9ob4figvn6jr3cds1s60lgpook.apps.googleusercontent.com',
  });
  React.useEffect(() => {
    if (response?.type === 'success') {
      const { params } = response;
      const accessToken = params?.id_token;
      user.changeToken(accessToken === undefined ? "GotNoToken" : accessToken);
      navigation.navigate("ProfileScreen");
    }
  }, [response])
  
  return (
    <View style={styles.container}>
      <Title>UIUC Course Scheduler</Title>
      <Button
        style={styles.button}
        icon="google"
        mode="contained"
        disabled={!request}
        onPress={() => {promptAsync();}}
      >Google Sign In</Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  button: {
    marginTop: 20,
    width: '60%'
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
});
