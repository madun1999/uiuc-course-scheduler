import * as React from 'react';
import {FlatList, StyleSheet} from 'react-native';
import {ActivityIndicator, Button, Card, Paragraph, Subheading, Title} from 'react-native-paper';
import { View } from '../components/Themed';
import UserProfile from '../api/UserProfile';
import { getUserProfile } from '../api/query';
import {BottomTabNavigationProp} from "@react-navigation/bottom-tabs";
import {BottomTabParamList} from "../types";
import {useContext} from "react";
import {UserContext} from '../contexts/UserContext'
import axios from "axios";
import {ScrollView} from "react-native-gesture-handler";

// screen parameter type
type ProfileScreenNavigationProp = BottomTabNavigationProp<BottomTabParamList, 'Login'>;
type ProfileScreenProps = {
  navigation: ProfileScreenNavigationProp,
};

  const GRAPHQL_URL = 'http://127.0.0.1:5000/graphql';

  const SCHEDULES_QUERY = `query {
    user {
      staredSchedules {
        sectionId
        startDate
        meetings {
          start
          end
          daysOfTheWeek
        }
      }
    }
  }`;

export default function ProfileScreen({ navigation } : ProfileScreenProps) {
  const [user, setUser] = React.useState<UserProfile | null>(null) // user to be displayed
  const [error, setError] = React.useState<string | null>(null) // error to be displayed
  const [loggedIn, setLoggedIn] = React.useState<boolean>(false) // error to be displayed
  const [schedules, setSchedules] = React.useState(null);

  const userInfo = useContext(UserContext)
  React.useEffect(() => {
    const token = userInfo.token;
    if (token === null || token === '') {
      setLoggedIn(false);
    } else {
      console.log(token)
      setLoggedIn(true);
      getUserProfile(token).then(setUser).catch((e: Error) => setError(e.message));
    }
  }, [navigation, userInfo.token, schedules]);

  // not logged in
  if (!loggedIn) {
    return (
      <View style={styles.container}>
        <Title>UIUC Course Scheduler</Title>
        <Button style={styles.button} icon="account-arrow-left" mode="contained"
                onPress={() => {
                  navigation.push("LoginScreen")
                }}>Log in</Button>
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
                onPress={() => {
                  navigation.push("LoginScreen")
                }}>Log in</Button>
      </View>
    );
  }

  // User is loading
  if (user === null) {
    return (
      <View style={styles.container}>
        <ActivityIndicator animating/>
      </View>
    );
  }


  async function getSchedules() {
    const config = {
      headers: {
        Authorization: `Bearer ${userInfo.token}`,
      },
    };
    const response = await axios.post(GRAPHQL_URL,
      { query: SCHEDULES_QUERY }, config);
    setSchedules(response.data.data.user.staredSchedules);
  }

  function renderSchedules(props) {
    const schedule = props.item;
    return (
      <Card style={{marginVertical: 5}}>
        <Card.Content>
          <View style={{flexDirection: 'row', alignItems: 'center'}}>
            <Button style={{width: '25%'}} mode="text"
                    onPress={() => navigation.push('ScheduleViewScreen', {schedule: {sections: schedule}})}>
              View
            </Button>
            {/*<Button style={{ width: '10%'}} icon="star" mode="text" onPress={() => {*/}
            {/*  setStars(schedule.sections.map(section => section.sectionId))*/}
            {/*}}>*/}
            {/*</Button>*/}
            <Paragraph style={{width: '50%'}}>
              {schedule.map(section => section.sectionId.toString().concat(", "))}
            </Paragraph>
            {/*<Subheading style={{color: 'green', width: '15%'}}>*/}
            {/*  95*/}
            {/*</Subheading>*/}
          </View>
        </Card.Content>
      </Card>
    );
  }

  // User is loaded
  return (
    <View style={styles.container}>
      <Title>User: {user.email}</Title>
      <Button style={styles.button} icon="account-arrow-right" mode="contained"
              onPress={() => {
                userInfo.changeToken("");
                setUser(null);
              }}
      >Log Out</Button>
      <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 10, width: '95%'}}>
        <Title style={{width: '40%'}}>Saved Schedules</Title>
        <Button style={{width: '40%'}} mode="contained" icon="refresh" onPress={
          () => {
            getSchedules().then(
              (response) => {},
              (error) => { setError(error.message); },
            )
          }}>
          Refresh</Button>
      </View>
      <ScrollView style={{width: '95%', marginTop: 5}}>
        <FlatList
          data={schedules}
          renderItem={renderSchedules}
        />
      </ScrollView>
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
    margin: 20,
    width: '60%'
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
});
