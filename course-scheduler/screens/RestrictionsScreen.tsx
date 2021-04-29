import * as React from 'react';
import {FlatList, StyleSheet} from 'react-native';

import { View } from '../components/Themed';
import {
  Title,
  Button,
  Card,
  Paragraph,
  Subheading,
  TextInput,
  Text,
  ActivityIndicator,
  Switch
} from 'react-native-paper';
import {ButtonGroup} from 'react-native-elements';
import {ScrollView} from "react-native-gesture-handler";
import {BottomTabNavigationProp} from "@react-navigation/bottom-tabs";
import {BottomTabParamList} from "../types";
import {useContext} from "react";
import {UserContext} from "../contexts/UserContext";
import { TimePickerModal } from 'react-native-paper-dates'

export default function RestrictionsScreen({ navigation } :
  { navigation : BottomTabNavigationProp<BottomTabParamList, 'Restrictions'> })  {
  const [minMandatoryText, setMinMandatoryText] = React.useState('0');
  const [maxText, setMaxText] = React.useState('10');

  const [startTimeText, setStartTimeText] = React.useState('');
  const [endTimeText, setEndTimeText] = React.useState('');
  const [startAMPM, setStartAMPM] = React.useState();
  const [endAMPM, setEndAMPM] = React.useState();
  const [daysOfWeek, setDaysOfWeek] = React.useState('');

  const [visible, setVisible] = React.useState(false)
  const onDismiss = React.useCallback(() => {
    setVisible(false)
  }, [setVisible])

  const onConfirm = React.useCallback(
    ({ hours, minutes }) => {
      setVisible(false);
      console.log({ hours, minutes });
    },
    [setVisible]
  );

  const days = ['M', 'T', 'W', 'T', 'F']
  const ampm = ['AM', 'PM']

  const [loggedIn, setLoggedIn] = React.useState<boolean>(false);

  const userInfo = useContext(UserContext)

  React.useEffect(() => {
    const token = userInfo.token;
    if (token === null || token === '') {
        setLoggedIn(false);
      } else {
        setLoggedIn(true);
    }
  }, [navigation, userInfo, visible]);

  if (!loggedIn) {
     return (
      <View style={styles.container}>
        <Title>Log in to add restrictions. </Title>
      </View>
    );
  }

  function renderBreak(props) {
    const break1 = props.item;
    return (
      <Card style={{marginVertical: 5}}>
        <Card.Content>
          <View style={{ flexDirection: 'row', alignItems: 'center'}}>
            <Text style={{ width: '60%' }}>
              {break1.start} - {break1.end}
            </Text>
            <Text style={{ width: '30%' }}>
              {break1.daysOfTheWeek}
            </Text>
            <Button style={{ width: '10%'}} icon="delete" mode="text"
                    onPress={() => userInfo.deleteBreak(break1.breakId)}>
            </Button>
          </View>
        </Card.Content>
      </Card>
    );
  }

  return (
    <View style={styles.container}>

      <Text style={styles.minMaxText}>
        Your current minimum number of mandatory courses is {userInfo.minMandatory}.
      </Text>
      <TextInput
        style={{ width: '95%', marginVertical: 3}}
        label="Minimum number of mandatory courses"
        value={minMandatoryText}
        onChangeText={
          text => setMinMandatoryText(text)
        }
      />
      <Text style={styles.minMaxText}>
        Your current maximum number of courses is {userInfo.maxCourses}.
      </Text>
      <TextInput
        style={{ width: '95%', marginBottom: 3}}
        label="Maximum number of courses"
        value={maxText}
        onChangeText={text => setMaxText(text)}
      />

      <Button style={{width: '95%', marginBottom: 10}} icon="plus-thick" mode="contained"
              onPress={
                () => {
                  userInfo.changeMinMandatory(parseInt(minMandatoryText))
                  userInfo.changeMaxCourses(parseInt(maxText))
                }
              }>
        Set Restrictions
      </Button>

      <View style={{ flexDirection: 'row', marginTop: 10, width: '95%', alignItems: 'center'}}>
        <Subheading style={{width: '15%'}}>Start</Subheading>
        <TextInput
          style={{ width: '55%', marginBottom: 3}}
          label="Start time"
          value={startTimeText}
          onChangeText={text => setStartTimeText(text)}
        />
        {/*<ButtonGroup*/}
        {/*  onPress={() => setStartAMPM(startAMPM)}*/}
        {/*  selectedIndex={startAMPM}*/}
        {/*  buttons={ampm}*/}
        {/*  selectedButtonStyle={{backgroundColor: '#6507ea'}}*/}
        {/*  containerStyle={{width: '25%', marginLeft: 10}}*/}
        {/*  textStyle={{fontFamily: 'sans-serif'}}*/}
        {/*/>*/}
      </View>

      {/*<Button style={{width: '95%', marginBottom: 10}}  mode="contained" onPress={()=> setVisible(true)}>*/}
      {/*  Pick time*/}
      {/*</Button>*/}
      {/*<TimePickerModal*/}
      {/*  visible={visible}*/}
      {/*  onDismiss={onDismiss}*/}
      {/*  onConfirm={onConfirm}*/}
      {/*  hours={12}*/}
      {/*  minutes={14}*/}
      {/*  label="Select time"*/}
      {/*  cancelLabel="Cancel"*/}
      {/*  confirmLabel="Ok"*/}
      {/*/>*/}

      <View style={{ flexDirection: 'row', marginTop: 10, width: '95%', alignItems: 'center'}}>
        <Subheading style={{width: '15%'}}>End</Subheading>
        <TextInput
          style={{ width: '55%', marginBottom: 3}}
          label="End time"
          value={endTimeText}
          onChangeText={text => setEndTimeText(text)}
        />
        {/*<ButtonGroup*/}
        {/*  onPress={() => console.log()}*/}
        {/*  selectedIndex={1}*/}
        {/*  buttons={ampm}*/}
        {/*  selectedButtonStyle={{backgroundColor: '#6507ea'}}*/}
        {/*  containerStyle={{width: '25%', marginLeft: 10}}*/}
        {/*  textStyle={{fontFamily: 'sans-serif'}}*/}
        {/*/>*/}
      </View>

      <View style={{ flexDirection: 'row', marginTop: 10, width: '95%', alignItems: 'center'}}>
        {/*<ButtonGroup*/}
        {/*  onPress={() => console.log()}*/}
        {/*  selectedIndex={1}*/}
        {/*  buttons={days}*/}
        {/*  selectedButtonStyle={{backgroundColor: '#6507ea'}}*/}
        {/*  containerStyle={{width: '40%', height:38}}*/}
        {/*  textStyle={{fontFamily: 'sans-serif'}}*/}
        {/*/>*/}
        <TextInput
          style={{ width: '55%', marginBottom: 3}}
          label="Days of Week"
          value={daysOfWeek}
          onChangeText={text => setDaysOfWeek(text)}
        />

        <Button style={{width: '50%', height:38}} icon="plus-thick" mode="contained"
                onPress={() => {
                  userInfo.addBreak({
                    breakId: startTimeText.concat(endTimeText).concat(daysOfWeek),
                    start: startTimeText,
                    end: endTimeText,
                    daysOfTheWeek: daysOfWeek,
                  })
                }}>
          Add breaks
        </Button>
      </View>


      <Title style={{width: '95%', textAlign: 'left'}}>Breaks</Title>

      <ScrollView style={{width: '95%', marginTop: 5}}>
        <FlatList
          data={userInfo.breaks}
          renderItem={renderBreak}
          keyExtractor={ (item) => item.breakId }
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
  minMaxText: {
    margin: 3
  },
});
