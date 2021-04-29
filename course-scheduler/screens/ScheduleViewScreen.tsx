import * as React from 'react';
import { StyleSheet } from 'react-native';

import { Calendar } from 'react-native-big-calendar'
import { BottomTabNavigationProp } from "@react-navigation/bottom-tabs";
import { SchedulerParamList } from "../types";
import { Text } from "react-native-paper";

function daysToNums(days) {
  let offset = []
  if (days.includes('M')) {
    offset.push(0);
  }
  if (days.includes('T')) {
    offset.push(1);
  }
  if (days.includes('W')) {
    offset.push(2);
  }
  if (days.includes('R')) {
    offset.push(3);
  }
  if (days.includes('F')) {
    offset.push(4);
  }
  return offset;
}

export default function SchedulerScreen({ navigation, route } :
  { navigation : BottomTabNavigationProp<SchedulerParamList, 'ScheduleViewScreen'> }) {
  const events = route.params?.schedule.sections.map(
    section => {
      if (section.sectionId === -1) {
        let result = []
        let offset = daysToNums(section.meetings[0].daysOfTheWeek);
        for (var i = 0; i < offset.length; i++) {
          result.push({
            title: "break",
            color: "green",
            start: new Date(
              2021,
              8,
              20 + offset[i],
              parseInt(section.meetings[0].start.slice(0, 2)),
              parseInt(section.meetings[0].start.slice(3, 5))
            ),
            end: new Date(
              2021,
              8,
              20 + offset[i],
              parseInt(section.meetings[0].end.slice(0, 2)),
              parseInt(section.meetings[0].end.slice(3, 5))
            )
          })
        }
        return(result);
      }
      let result = []
      let offset = daysToNums(section.meetings[0].daysOfTheWeek);
      for (var i = 0; i < offset.length; i++) {
        result.push({
          title: section.sectionId,
          start: new Date(
            2021,
            8,
            20 + offset[i],
            parseInt(section.meetings[0].start.slice(0, 2)),
            parseInt(section.meetings[0].start.slice(3, 5))
          ),
          end: new Date(
            2021,
            8,
            20 + offset[i],
            parseInt(section.meetings[0].end.slice(0, 2)),
            parseInt(section.meetings[0].end.slice(3, 5))
          )
        })
      }
      return(result);
    }
  )

  let idx = 0;
  while (route.params?.schedule.sections[idx].sectionId === -1) {
    idx++;
  }
  const temp = route.params?.schedule.sections[idx];

  if (temp === null) {
    <Text>No courses added.</Text>
  }

  return (
    <Calendar events={events.flat()} height={1200}
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