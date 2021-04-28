import * as React from 'react';
import {FlatList, StyleSheet} from 'react-native';

import { View } from '../components/Themed';
import {Title, Button, Card, Paragraph, Subheading, ActivityIndicator, Text} from 'react-native-paper';
import { ScrollView } from 'react-native-gesture-handler';
import {BottomTabNavigationProp} from "@react-navigation/bottom-tabs";
import {BottomTabParamList} from "../types";
import {useContext} from "react";
import {UserContext} from "../contexts/UserContext";
import axios from "axios";


export default function SchedulerScreen({ navigation } :
  { navigation : BottomTabNavigationProp<BottomTabParamList, 'Scheduler'> }) {

  const [loggedIn, setLoggedIn] = React.useState<boolean>(false);
  const [schedules, setSchedules] = React.useState(null);
  const [errorMsg, setErrorMsg] = React.useState<null | string>(null);

  const userInfo = useContext(UserContext)

  const GRAPHQL_URL = 'http://127.0.0.1:5000/graphql';

  const SCHEDULES_QUERY = `query Schedule($courses: [String!]!){
    schedule(courses: $courses) {
      schedules {
        sections {
          sectionId
          startDate
          meetings {
            start
            end
            daysOfTheWeek
          }
        }
      }
    }
  }`;

  async function getSchedules(courses) {
    const config = {
      headers: {
        Authorization: `Bearer ${userInfo.token}`,
      },
    };
    const response = await axios.post(GRAPHQL_URL,
      { query: SCHEDULES_QUERY, variables: { courses } }, config);
    setSchedules(response.data.data.schedule.schedules);
  }

  React.useEffect(() => {
    const token = userInfo.token;
    console.log(userInfo)
    if (token === null || token === '') {
        setLoggedIn(false);
      } else {
        setLoggedIn(true);
        console.log(userInfo.courses.map(course => course.courseId))
        getSchedules(userInfo.courses.map(course => course.courseId)).then(
          (response) => {},
          (error) => { setErrorMsg(error.message); },
        );
    }
  }, [navigation, userInfo]);

  if (!loggedIn) {
     return (
      <View style={styles.container}>
        <Title>Log in to view schedules. </Title>
      </View>
    );
  }

  if (errorMsg !== null) {
    return <View style={styles.container}>{errorMsg}</View>;
  }

  if (schedules === null) {
    return (
      <View style={styles.container}>
        <ActivityIndicator animating />
      </View>
    );
  }

  function renderSchedules(props) {
    const schedule = props.item;
    return (
      <Card style={{marginVertical: 5}}>
        <Card.Content>
          <View style={{ flexDirection: 'row', alignItems: 'center'}}>
            <Button style={{ width: '25%'}} mode="text" onPress={() => navigation.push('ScheduleViewScreen', { schedule: schedule})}>
              View
            </Button>
            <Button style={{ width: '10%'}} icon="star" mode="text" onPress={() => console.log()}>
            </Button>
            <Paragraph style={{ width: '50%' }}>
              {schedule.sections.map(section => section.sectionId.toString().concat(", "))}
            </Paragraph>
            <Subheading style={{ color: 'green', width: '15%' }}>
                95
            </Subheading>
          </View>
        </Card.Content>
      </Card>
    );
  }

  return (
    <View style={styles.container}>
      <Button style={[styles.button, {marginTop: 10}]} icon="book" mode="contained" onPress={() => navigation.navigate('Courses')}>
        Courses
      </Button>
      <Button style={styles.button} icon="alert-octagon" mode="contained" onPress={() => navigation.navigate('Restrictions')}>
        Restrictions
      </Button>
      <Button style={styles.button} icon="swap-vertical-bold" mode="contained" onPress={() => navigation.navigate('Factors')}>
        Factors' Importance
      </Button>

      <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 10, width: '95%'}}>
        <Title>Schedules</Title>
      </View>

      <ScrollView style={{width: '95%'}}>
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
    alignItems: 'center'
  },
  button: {
    margin: 2,
    width: '95%'
  },
});
