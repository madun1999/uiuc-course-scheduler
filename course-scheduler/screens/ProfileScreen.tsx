import * as React from 'react';
import { StyleSheet } from 'react-native';
import {ActivityIndicator, Button, Title} from 'react-native-paper';
import { View } from '../components/Themed';
import UserProfile from '../api/UserProfile';
import { getUserProfile } from '../api/query';
import {BottomTabNavigationProp} from "@react-navigation/bottom-tabs";
import {BottomTabParamList} from "../types";
import {useContext} from "react";
import {UserContext} from '../contexts/UserContext'

// screen parameter type
type ProfileScreenNavigationProp = BottomTabNavigationProp<BottomTabParamList, 'Login'>;
type ProfileScreenProps = {
  navigation: ProfileScreenNavigationProp,
};

export default function ProfileScreen({ navigation } : ProfileScreenProps) {
  const [user, setUser] = React.useState<UserProfile | null>(null) // user to be displayed
  const [error, setError] = React.useState<string | null>(null) // error to be displayed
  const [loggedIn, setLoggedIn] = React.useState<boolean>(false) // error to be displayed

  const userInfo = useContext(UserContext)
  React.useEffect(() => {
    const token = userInfo.token;
    if (token === null || token === '') {
        setLoggedIn(false);
      } else {
        console.log(token)
        setLoggedIn(true);
        getUserProfile(token).then(setUser).catch((e : Error) => setError(e.message));
    }
  }, [navigation, userInfo.token]);

  // not logged in
  if (!loggedIn) {
     return (
      <View style={styles.container}>
        <Button style={styles.button} icon="account-arrow-left" mode="contained"
                onPress={() => {navigation.push("LoginScreen")}}>Log in</Button>
      </View>
    );
  }

  // There is an error
  if (error !== null) {
    return (
      <View style={styles.container}>
        <Title>{error}</Title>
        <Title>Maybe you didn't log in.</Title>
        <Button style={styles.button} icon="account-arrow-left" mode="contained"
                onPress={() => {navigation.push("LoginScreen")}}>Log in</Button>
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
      <Title>User: {user.email}</Title>
      <Button style={styles.button} icon="account-arrow-right" mode="contained"
              onPress={() => {userInfo.changeToken(""); setUser(null);}}
      >Log Out</Button>
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
