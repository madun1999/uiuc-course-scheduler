import * as React from 'react';
import { StyleSheet } from 'react-native';

import { View } from '../components/Themed';
import {Title, Button, Card, Paragraph, Subheading, DataTable} from 'react-native-paper';
import { ScrollView } from 'react-native-gesture-handler';
import { Calendar } from 'react-native-big-calendar'

export default function SchedulerScreen({ navigation }) {
  const events = [
    {
      title: 'CS 242',
      start: new Date(2021, 4, 14, 11, 0),
      end: new Date(2021, 4, 14, 11, 50),
    },
  ]

  return (
    <View style={styles.container}>
      <Button style={[styles.button, {marginTop: 10}]} icon="book" mode="contained" onPress={() => console.log()}>
        Courses
      </Button>
      <Button style={styles.button} icon="alert-octagon" mode="contained" onPress={() => console.log()}>
        Restrictions
      </Button>
      <Button style={styles.button} icon="swap-vertical-bold" mode="contained" onPress={() => console.log()}>
        Factors' Importance
      </Button>

      <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 10, width: '95%'}}>
        <Title>Schedules</Title>
        <Button icon="refresh" mode="contained" onPress={() => console.log()}>
          Generate Schedules
        </Button>
      </View>

      <ScrollView style={{width: '95%'}}>
        <Card style={{marginVertical: 5}}>
          <Card.Content>
            <View style={{ flexDirection: 'row', alignItems: 'center'}}>
              <Button style={{ width: '25%'}} mode="text" onPress={() => navigation.push('ScheduleViewScreen')}>
                View
              </Button>
              <Button style={{ width: '10%'}} icon="star" mode="text" onPress={() => console.log()}>
              </Button>
              <Paragraph style={{ width: '50%' }}>
                  MATH 417, CS 242
              </Paragraph>
              <Subheading style={{ color: 'green', width: '15%' }}>
                  95
              </Subheading>
            </View>
          </Card.Content>
        </Card>
        <Card style={{marginVertical: 5}}>
          <Card.Content>
            <View style={{ flexDirection: 'row', alignItems: 'center'}}>
              <Button style={{ width: '25%'}} mode="text" onPress={() => console.log()}>
                View
              </Button>
              <Button style={{ width: '10%'}} icon="star" mode="text" onPress={() => console.log()}>
              </Button>
              <Paragraph style={{ width: '50%' }}>
                  MATH 417, CS 242, CS 441, STAT 420
              </Paragraph>
              <Subheading style={{ color: 'green', width: '15%' }}>
                  95
              </Subheading>
            </View>
          </Card.Content>
        </Card>

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
