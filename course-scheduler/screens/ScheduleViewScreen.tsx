import * as React from 'react';
import { StyleSheet } from 'react-native';

import { Calendar } from 'react-native-big-calendar'

const events = [
    {
      title: 'CS 242',
      start: new Date(2021, 3, 14, 11, 0),
      end: new Date(2021, 3, 14, 12, 50),
    }, {
      title: 'CS 446',
      start: new Date(2021, 3, 15, 12, 0),
      end: new Date(2021, 3, 15, 13, 50),
    },
  ]

export default function SchedulerScreen({ navigation }) {
  return (
      <Calendar events={events} height={1200}/>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center'
  },
});