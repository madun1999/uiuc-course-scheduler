import * as React from 'react';
import { StyleSheet, Button } from 'react-native';
import { ActivityIndicator } from 'react-native-paper';
import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';
import UserProfile from '../api/UserProfile';
import { getUserProfile } from '../api/query';
import AsyncStorage from '@react-native-async-storage/async-storage'
import { useIsFocused } from "@react-navigation/native";
import {BottomTabNavigationProp} from "@react-navigation/bottom-tabs";
import {BottomTabParamList} from "../types";

// screen parameter type
type ProfileScreenNavigationProp = BottomTabNavigationProp<BottomTabParamList, 'Login'>;
type ProfileScreenProps = {
  navigation: ProfileScreenNavigationProp,
};

export default function ProfileScreen({ navigation } : ProfileScreenProps) {
  const [user, setUser] = React.useState<UserProfile | null>(null) // user to be displayed
  const [error, setError] = React.useState<string | null>(null) // error to be displayed
  const [loggedIn, setLoggedIn] = React.useState<boolean>(false) // error to be displayed

  React.useEffect(() => {
    AsyncStorage.getItem('googleAuthToken').then((token) => 
      {
        if (token === null) {
          setLoggedIn(false);
        } else {
          setLoggedIn(true);
          getUserProfile(token).then(setUser).catch((e : Error) => setError(e.message));
        }
      }
    );
  }, [navigation]);

  // There is an error
  if (error !== null) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>{error}</Text>
        <Text style={styles.title}>Maybe you didn't log in.</Text>
      </View>
    );
  }

  // not logged in
  if (!loggedIn) {
     return (
      <View style={styles.container}>
        <Button
          title="Log in"
          onPress={() => {navigation.push("LoginScreen")}}
        />
      </View>
    );
  }

  // User is loading
  if (user === null) {
    return (
      <View style={styles.container}>
        <ActivityIndicator animating />
      </View>
    );
  }

  // User is loaded
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Email: {user.email}</Text>
      <Button
        title="Logout" 
        onPress={() => {AsyncStorage.removeItem('googleAuthToken').then(() => setLoggedIn(false))}}
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
