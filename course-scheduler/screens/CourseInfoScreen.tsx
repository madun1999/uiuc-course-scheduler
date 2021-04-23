import * as React from 'react';
import {FlatList, StyleSheet} from 'react-native';

import { View } from '../components/Themed';
import {Title, Paragraph, DataTable, ActivityIndicator, Card, Text, Switch, Button, Subheading} from 'react-native-paper';
import { ScrollView } from 'react-native-gesture-handler';
import { BottomTabNavigationProp } from "@react-navigation/bottom-tabs";
import { CourseInfoParamList } from "../types";
import {useContext, useEffect} from "react";
import {UserContext} from '../contexts/UserContext'
import {getUserProfile} from "../api/query";
import axios from "axios";

export default function CourseInfoScreen({ navigation, route } :
  { navigation : BottomTabNavigationProp<CourseInfoParamList, 'CourseInfoScreen'> }) {

  const [loggedIn, setLoggedIn] = React.useState<boolean>(false);
  const [course, setCourse] = React.useState(null);
  const [errorMsg, setErrorMsg] = React.useState<null | string>(null);

  const userInfo = useContext(UserContext)

  const GRAPHQL_URL = 'http://127.0.0.1:5000/graphql';

  const COURSE_QUERY = `query Course($courseId: String!) {
    course(courseId: $courseId) {
      courseDetail {
        title
        description
        credit_hours
        sections {
          sectionId
          sectionNumber
          sectionTitle
          sectionText
          partOfTerm
          enrollmentStatus
          startDate
          EndDate
          meetings {
            meetingType
            start
            end
            daysOfTheWeek
            buildingName
            roomNumber
            instructors {
              firstName
              lastName
            }
          }
        }
      }
    }
  }`;

  async function getCourse(courseId) {
    const config = {
      headers: {
        Authorization: `Bearer ${userInfo.token}`,
      },
    };
    const response = await axios.post(GRAPHQL_URL,
      { query: COURSE_QUERY, variables: { courseId } }, config);
    setCourse(response.data.data.course.courseDetail);
  }

  React.useEffect(() => {
    const token = userInfo.token;
    console.log(userInfo)
    if (token === null || token === '') {
        setLoggedIn(false);
      } else {
        setLoggedIn(true);
        getCourse(route.params?.courseId).then(
          (response) => {},
          (error) => { setErrorMsg(error.message); },
        );
    }
  }, [navigation, userInfo]);

  if (!loggedIn) {
     return (
      <View style={styles.container}>
        <Title>Log in to add courses. </Title>
      </View>
    );
  }

  if (errorMsg !== null) {
    return <View style={styles.container}>{errorMsg}</View>;
  }

  if (course === null) {
    return (
      <View style={styles.container}>
        <ActivityIndicator animating />
      </View>
    );
  }

  function renderSections(props) {
    const section = props.item;
    const meetings = section.meetings[0]
    // const instructors = meetings.instructors[0]
    return (
      <Card style={{marginVertical: 5}}>
        <Card.Content>
          <Text>Section ID: {section.sectionId}</Text>
          <Text>Section Number: {section.sectionNumber}</Text>
          <Text>Section Title: {section.sectionTitle === null ? "" : section.sectionTitle}</Text>
          <Paragraph>Section Info: {section.sectionText === null ? "" : section.sectionText}</Paragraph>
          <Text>Part of Term: {section.partOfTerm === null ? "" : section.partOfTerm}</Text>
          <Text>Enrollment Status: {section.enrollmentStatus === null ? "" : section.enrollmentStatus}</Text>
          <Text>Start Date: {section.startDate === null ? "" : section.startDate}</Text>
          <Text>End Date : {section.EndDate === null ? "" : section.EndDate}</Text>
          <Text>Meeting Type: {meetings.meetingType === null ? "" : meetings.meetingType}</Text>
          <Text>Start: {meetings.start === null ? "" : meetings.start}</Text>
          <Text>End: {meetings.end === null ? "" : meetings.end}</Text>
          <Text>Days Of The Week: {meetings.daysOfTheWeek === null ? "" : meetings.daysOfTheWeek}</Text>
          <Text>Location: {meetings.buildingName === null ? "" : meetings.buildingName }</Text>
          <Text>Room: {meetings.roomNumber === null ? "" : meetings.roomNumber}</Text>
          {/*<Text>Instructor: {instructors.lastName === null ? "" : instructors.lastName}, {instructors.firstName === null ? "" : instructors.firstName }</Text>*/}
        </Card.Content>
      </Card>
    );
  }

  return (

    <View style={styles.container}>
    <Title style={{width: '95%'}}>{route.params?.courseId} {course.title}</Title>
    <Text>{course.credit_hours}</Text>
    <Paragraph style={{width: '95%'}}>{course.description}</Paragraph>

    <ScrollView style={{width: '95%'}}>
        <FlatList
          data={course.sections}
          renderItem={renderSections}
          keyExtractor={ (item) => item.sectionId }
        />
    </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
  },
});