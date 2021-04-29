import * as React from 'react';
import { StyleSheet } from 'react-native';

import { View } from '../components/Themed';
import Slider from '@react-native-community/slider';
import {Title, Text, Subheading} from 'react-native-paper';
import { BottomTabNavigationProp } from "@react-navigation/bottom-tabs";
import { BottomTabParamList } from "../types";
import {useContext} from "react";
import {UserContext} from "../contexts/UserContext";

export default function FactorsScreen({ navigation } :
  { navigation : BottomTabNavigationProp<BottomTabParamList, 'Factors'> }) {

  const [loggedIn, setLoggedIn] = React.useState<boolean>(false)

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
        <Title>Log in to set importance factors.</Title>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Subheading>Set importance factors to score schedules.</Subheading>
      <Title style={{width: '95%', textAlign: 'left'}}>GPA</Title>
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 10, width: '95%'}}>
          <Text>Not important</Text>
          <Text>Important</Text>
        </View>
      <Slider
        style={{width: '90%', height: 40}}
        minimumValue={0}
        maximumValue={1}
        step={0.1}
        thumbTintColor="#6507ea"
        minimumTrackTintColor="black"
        maximumTrackTintColor="gray"
        onValueChange={value => {userInfo.changeGPAFactor(value)}}
      />

      <Title style={{width: '95%', textAlign: 'left'}}>A Rate</Title>
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 10, width: '95%'}}>
          <Text>Not important</Text>
          <Text>Important</Text>
        </View>
      <Slider
        style={{width: '90%', height: 40}}
        minimumValue={0}
        maximumValue={1}
        step={0.1}
        thumbTintColor="#6507ea"
        minimumTrackTintColor="black"
        maximumTrackTintColor="gray"
        onValueChange={value => {userInfo.changeARateFactor(value)}}
      />

      {/* for future development */}
    {/*  <Title style={{width: '95%', textAlign: 'left'}}>Professor's Rating</Title>*/}
    {/*    <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 10, width: '95%'}}>*/}
    {/*      <Text>Not important</Text>*/}
    {/*      <Text>Important</Text>*/}
    {/*    </View>*/}
    {/*  <Slider*/}
    {/*    style={{width: '90%', height: 40}}*/}
    {/*    minimumValue={0}*/}
    {/*    maximumValue={10}*/}
    {/*    step={1}*/}
    {/*    thumbTintColor="#6507ea"*/}
    {/*    minimumTrackTintColor="black"*/}
    {/*    maximumTrackTintColor="gray"*/}
    {/*  />*/}

    {/*  <Title style={{width: '95%', textAlign: 'left'}}>Will-take-again Rate</Title>*/}
    {/*    <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 10, width: '95%'}}>*/}
    {/*      <Text>Not important</Text>*/}
    {/*      <Text>Important</Text>*/}
    {/*    </View>*/}
    {/*  <Slider*/}
    {/*    style={{width: '90%', height: 40}}*/}
    {/*    minimumValue={0}*/}
    {/*    maximumValue={10}*/}
    {/*    step={1}*/}
    {/*    thumbTintColor="#6507ea"*/}
    {/*    minimumTrackTintColor="black"*/}
    {/*    maximumTrackTintColor="gray"*/}
    {/*  />*/}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center'
  },
});
