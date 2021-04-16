import * as React from 'react';
import { StyleSheet } from 'react-native';

import { View } from '../components/Themed';
import Slider from '@react-native-community/slider';
import {Title, Button, Card, Paragraph, Text} from 'react-native-paper';

export default function SchedulerScreen() {
  const [state, setState] = React.useState('');

  return (
    <View style={styles.container}>
      <Title style={{width: '95%', textAlign: 'left'}}>GPA</Title>
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 10, width: '95%'}}>
          <Text>Not important</Text>
          <Text>Important</Text>
        </View>
      <Slider
        style={{width: '90%', height: 40}}
        minimumValue={0}
        maximumValue={10}
        step={1}
        thumbTintColor="#6507ea"
        minimumTrackTintColor="black"
        maximumTrackTintColor="gray"
      />

      <Title style={{width: '95%', textAlign: 'left'}}>A Rate</Title>
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 10, width: '95%'}}>
          <Text>Not important</Text>
          <Text>Important</Text>
        </View>
      <Slider
        style={{width: '90%', height: 40}}
        minimumValue={0}
        maximumValue={10}
        step={1}
        thumbTintColor="#6507ea"
        minimumTrackTintColor="black"
        maximumTrackTintColor="gray"
      />

      <Title style={{width: '95%', textAlign: 'left'}}>Professor's Rating</Title>
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 10, width: '95%'}}>
          <Text>Not important</Text>
          <Text>Important</Text>
        </View>
      <Slider
        style={{width: '90%', height: 40}}
        minimumValue={0}
        maximumValue={10}
        step={1}
        thumbTintColor="#6507ea"
        minimumTrackTintColor="black"
        maximumTrackTintColor="gray"
      />

      <Title style={{width: '95%', textAlign: 'left'}}>Will-take-again Rate</Title>
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 10, width: '95%'}}>
          <Text>Not important</Text>
          <Text>Important</Text>
        </View>
      <Slider
        style={{width: '90%', height: 40}}
        minimumValue={0}
        maximumValue={10}
        step={1}
        thumbTintColor="#6507ea"
        minimumTrackTintColor="black"
        maximumTrackTintColor="gray"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center'
  },
});
