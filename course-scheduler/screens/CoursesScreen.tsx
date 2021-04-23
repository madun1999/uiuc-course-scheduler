import * as React from 'react';
import {FlatList, StyleSheet} from 'react-native';

import {Text, View} from '../components/Themed';
import {Title, Button, Card, Subheading, Switch, TextInput, ActivityIndicator} from 'react-native-paper';
import { ScrollView } from 'react-native-gesture-handler';

import {BottomTabNavigationProp} from "@react-navigation/bottom-tabs";
import {BottomTabParamList} from "../types";
import UserProfile from "../api/UserProfile";
import {getUserProfile} from "../api/query";
import axios, {AxiosResponse} from "axios";

import {useContext, useEffect} from "react";
import {UserContext} from '../contexts/UserContext'

export default function CoursesScreen({ navigation } :
  { navigation : BottomTabNavigationProp<BottomTabParamList, 'Courses'> }) {
  const [subjectText, setSubjectText] = React.useState('');
  const [courseText, setCourseText] = React.useState('');

  const [isSwitchOn, setIsSwitchOn] = React.useState(false);
  const onToggleSwitch = () => setIsSwitchOn(!isSwitchOn);

  const [loggedIn, setLoggedIn] = React.useState<boolean>(false) // error to be displayed

  const userInfo = useContext(UserContext)
  React.useEffect(() => {
    const token = userInfo.token;
    if (token === null || token === '') {
        setLoggedIn(false);
      } else {
        setLoggedIn(true);
    }
  }, [navigation, userInfo]);

  if (!loggedIn) {
     return (
      <View style={styles.container}>
        <Title>Log in to add courses. </Title>
      </View>
    );
  }


  // const GRAPHQL_URL = 'http://127.0.0.1:5000/graphql';
  //
  // const SUBJECT_QUERY = `query {
  // subjects {
  //     success
  //     error
  //     result {
  //       subjectId
  //       name
  //     }
  //   }
  // }`;
  // const COURSE_QUERY = `query {
  //   courses(subject: $subject) {
  //     courseNum
  //   }
  // }`;

  // async function getSubject(subject) {
  //   const config = {
  //     headers: {
  //       Authorization: `bearer ${userInfo.token}`,
  //     },
  //   };
  //   const response = await axios.post(GRAPHQL_URL,
  //     { query: SUBJECT_QUERY }, config);
  //
  // }
  //
  // async function getCourse(subject, course) {
  //   const config = {
  //     headers: {
  //       Authorization: `bearer ${userInfo.token}`,
  //     },
  //   };
  //   const response = await axios.post(GRAPHQL_URL,
  //     { query: SUBJECT_QUERY, variables: { subject } }, config);
  //
  // }

  function renderCourse(props) {
    const course = props.item;
    return (
      <Card style={{marginVertical: 5}}>
        <Card.Content>
          <View style={{ flexDirection: 'row', alignItems: 'center'}}>
            <Switch style={{ width: '10%'}} value={isSwitchOn} onValueChange={onToggleSwitch} />
            <Button style={{ width: '45%'}} mode="text"
                    onPress={() => navigation.push('CourseInfoScreen', { courseId: course.courseId})}>
              View More
            </Button>
            <Subheading style={{ width: '35%' }}>
              {course.courseId}
            </Subheading>
            <Button style={{ width: '10%'}} icon="delete" mode="text"
                    onPress={() => userInfo.deleteCourse(course.courseId)}>
            </Button>
          </View>
        </Card.Content>
      </Card>
    );
  }

  return (
    <View style={styles.container}>
      <TextInput
        style={{ width: '95%', marginVertical: 3}}
        label="Subject"
        value={subjectText}
        onChangeText={ text => setSubjectText(text) }
      />
      <TextInput
        style={{ width: '95%', marginBottom: 3}}
        label="Course"
        value={courseText}
        onChangeText={ text => setCourseText(text) }
      />

      <Button style={{ width: '95%' }} icon="plus-thick" mode="contained"
              onPress={() => userInfo.addCourse({courseId: subjectText.concat(courseText), mandatory: false})}>
        Add Courses
      </Button>

      <Title style={{ textAlign: 'left', width: '95%'}}>Courses</Title>
      <Subheading style={{ textAlign: 'left', width: '95%', marginTop: 5}}>mandatory?</Subheading>

      <ScrollView style={{width: '95%'}}>
          <FlatList
            data={userInfo.courses}
            renderItem={renderCourse}
            keyExtractor={ (item) => item.courseId }
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
