import * as React from 'react';
import { StyleSheet, Button } from 'react-native';
import { ActivityIndicator } from 'react-native-paper';
import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';
import UserProfile from '../api/UserProfile';
import { getUserProfile, logout } from '../api/query';
import AsyncStorage from '@react-native-async-storage/async-storage'
import { useIsFocused } from "@react-navigation/native";

export default function ProfileScreen({ navigation }) {
  const [user, setUser] = React.useState<UserProfile | null>(null)
  const [error, setError] = React.useState<string | null>(null)
  const isFocused = useIsFocused();

  React.useEffect(() => {
    AsyncStorage.getItem('googleAuthToken').then((token) => 
      {console.log("profile screen: " + token); getUserProfile(token === null ? '' : token).then(setUser).catch((e : Error) => setError(e.message))}
    );
  }, []);

  if (error !== null) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>{error}</Text>
        <Text style={styles.title}>Maybe you didn't log in.</Text>
      </View>
    );
  }

  if (user === null) {
    return (
      <View style={styles.container}>
        <ActivityIndicator animating />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Email: {user.email}</Text>
      <Button
        title="Logout" 
        onPress={() => {AsyncStorage.removeItem('googleAuthToken'); navigation.navigate("Login")}}
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
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
});
