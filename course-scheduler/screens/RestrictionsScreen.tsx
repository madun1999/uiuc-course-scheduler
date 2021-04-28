import * as React from 'react';
import { StyleSheet } from 'react-native';

import { View } from '../components/Themed';
import {Title, Button, Card, Paragraph, Subheading, TextInput, Text} from 'react-native-paper';
import {ButtonGroup} from 'react-native-elements';
import {ScrollView} from "react-native-gesture-handler";
import {BottomTabNavigationProp} from "@react-navigation/bottom-tabs";
import {BottomTabParamList} from "../types";

export default function RestrictionsScreen({ navigation } :
  { navigation : BottomTabNavigationProp<BottomTabParamList, 'Restrictions'> })  {
  const [minMandatoryText, setMinMandatoryText] = React.useState('');
  const [maxText, setMaxText] = React.useState('');
  const [startTimeText, setStartTimeText] = React.useState('');
  const [endTimeText, setEndTimeText] = React.useState('');

  const days = ['M', 'T', 'W', 'T', 'F']
  const ampm = ['AM', 'PM']

  return (
    <View style={styles.container}>
      <TextInput
        style={{ width: '95%', marginVertical: 3}}
        label="Minimum number of mandatory courses"
        value={minMandatoryText}
        onChangeText={text => setMinMandatoryText(text)}
      />
      <TextInput
        style={{ width: '95%', marginBottom: 3}}
        label="Maximum number of courses"
        value={maxText}
        onChangeText={text => setMaxText(text)}
      />

      <Button style={{width: '95%', marginBottom: 10}} icon="plus-thick" mode="contained" onPress={() => console.log()}>
        Set Restrictions
      </Button>

      <View style={{ flexDirection: 'row', marginTop: 10, width: '95%', alignItems: 'center'}}>
        <Subheading style={{width: '15%'}}>Start</Subheading>
        <TextInput
          style={{ width: '55%', marginBottom: 3}}
          label="Time"
          value={startTimeText}
          onChangeText={text => setStartTimeText(text)}
        />
        <ButtonGroup
          onPress={() => console.log()}
          selectedIndex={1}
          buttons={ampm}
          selectedButtonStyle={{backgroundColor: '#6507ea'}}
          containerStyle={{width: '25%', marginLeft: 10}}
        />
      </View>

      <View style={{ flexDirection: 'row', marginTop: 10, width: '95%', alignItems: 'center'}}>
        <Subheading style={{width: '15%'}}>End</Subheading>
        <TextInput
          style={{ width: '55%', marginBottom: 3}}
          label="Time"
          value={endTimeText}
          onChangeText={text => setEndTimeText(text)}
        />
        <ButtonGroup
          onPress={() => console.log()}
          selectedIndex={1}
          buttons={ampm}
          selectedButtonStyle={{backgroundColor: '#6507ea'}}
          containerStyle={{width: '25%', marginLeft: 10}}
        />
      </View>

      <View style={{ flexDirection: 'row', marginTop: 10, width: '95%', alignItems: 'center'}}>
        <ButtonGroup
          onPress={() => console.log()}
          selectedIndex={1}
          buttons={days}
          selectedButtonStyle={{backgroundColor: '#6507ea'}}
          containerStyle={{width: '40%', height:38}}
        />
        <Button style={{width: '50%', height:38}} icon="plus-thick" mode="contained" onPress={() => console.log()}>
        Add breaks
      </Button>
      </View>


      <Title style={{width: '95%', textAlign: 'left'}}>Breaks</Title>

      <ScrollView style={{width: '95%', marginTop: 5}}>
        <Card style={{marginVertical: 5}}>
          <Card.Content>
            <View style={{ flexDirection: 'row', alignItems: 'center'}}>
              <Text style={{ width: '60%' }}>
                11:oo AM - 12:00 PM
              </Text>
              <Text style={{ width: '30%' }}>
                MWF
              </Text>
              <Button style={{ width: '10%'}} icon="delete" mode="text" onPress={() => console.log()}>
              </Button>
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
});
