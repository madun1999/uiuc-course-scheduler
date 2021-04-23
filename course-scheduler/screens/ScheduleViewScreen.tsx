import * as React from 'react';
import { StyleSheet } from 'react-native';

import { Calendar } from 'react-native-big-calendar'
import { BottomTabNavigationProp } from "@react-navigation/bottom-tabs";
import { SchedulerParamList } from "../types";
import { Text } from "react-native-paper";

// const events = [
//     {
//       title: 'CS 242',
//       start: new Date(2021, 3, 14, 11, 0),
//       end: new Date(2021, 3, 14, 12, 50),
//     }, {
//       title: 'CS 446',
//       start: new Date(2021, 3, 15, 12, 0),
//       end: new Date(2021, 3, 15, 13, 50),
//     },
//   ]

export default function SchedulerScreen({ navigation, route } :
  { navigation : BottomTabNavigationProp<SchedulerParamList, 'ScheduleViewScreen'> }) {
  const events = route.params?.schedule.sections.map(
    section => {return({
      title: section.sectionId,
      start: new Date(
          parseInt(section.startDate.slice(0, 4)),
          parseInt(section.startDate.slice(5, 7)),
          parseInt(section.startDate.slice(8, 10)),
          parseInt(section.meetings[0].start.slice(0, 2)),
          parseInt(section.meetings[0].start.slice(3, 5))
      ),
      end: new Date(
        parseInt(section.startDate.slice(0, 4)),
        parseInt(section.startDate.slice(5, 7)),
        parseInt(section.startDate.slice(8, 10)),
        parseInt(section.meetings[0].end.slice(0, 2)),
        parseInt(section.meetings[0].end.slice(3, 5))
      )
    });}
  )

  const temp = route.params?.schedule.sections[0]

  if (temp === null) {
    <Text>No courses added.</Text>
  }

  return (
    <Calendar events={events} height={1200}
              date={new Date(
          parseInt(temp.startDate.slice(0, 4)),
          parseInt(temp.startDate.slice(5, 7)),
          parseInt(temp.startDate.slice(8, 10)),
          parseInt(temp.meetings[0].start.slice(0, 2)),
          parseInt(temp.meetings[0].start.slice(3, 5))
      )}
    />
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center'
  },
});