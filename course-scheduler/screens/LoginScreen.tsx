import * as React from 'react';
import { StyleSheet, Button } from 'react-native';
import * as WebBrowser from 'expo-web-browser';
import * as Google from 'expo-auth-session/providers/google';
import { Text, View } from '../components/Themed';
import AsyncStorage from '@react-native-async-storage/async-storage'

WebBrowser.maybeCompleteAuthSession();

export default function LoginScreen({ navigation }) {
  const [request, response, promptAsync] = Google.useAuthRequest({
    responseType: "id_token",
    expoClientId: process.env.GOOGLE_APP_CLIENT_ID,
    iosClientId: process.env.GOOGLE_APP_CLIENT_ID,
    androidClientId: process.env.GOOGLE_APP_CLIENT_ID,
    webClientId: process.env.GOOGLE_WEB_CLIENT_ID,
  });
  React.useEffect(() => {
    if (response?.type === 'success') {
      const { params } = response;
      const accessToken = params?.id_token;
      console.log(response)
      console.log("google signed in: " + accessToken)
      AsyncStorage.setItem('googleAuthToken', accessToken === undefined ? "" : accessToken).then(() => {console.log(accessToken); navigation.navigate("Profile")});
    }
  }, [response])
  
  return (
    <View style={styles.container}>
      <Text style={styles.title}> UIUC {"\n"} Course {"\n"} Scheduler </Text>
      <Button
        disabled={!request}
        title="Google Sign In" 
        onPress={() => {
          promptAsync();
          }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
});
