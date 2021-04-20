import * as React from 'react';
import { StyleSheet } from 'react-native';

import { View } from '../components/Themed';
import {Title, Button, Card, Paragraph, Subheading, DataTable} from 'react-native-paper';
import { ScrollView } from 'react-native-gesture-handler';

import {BottomTabParamList} from "../types";
import {BottomTabNavigationProp} from "@react-navigation/bottom-tabs";

// type CourseInfoScreenNavigationProp = BottomTabNavigationProp<BottomTabParamList, 'CourseInfo'>;
// type CourseInfoScreenProps = {
//   navigation: CourseInfoScreenNavigationProp,
// };

export default function CourseInfoScreen({ navigation }) {
    return (
      <View style={styles.container}>
      <Title style={{width: '95%'}}>CS 242 Programming Studio</Title>
      <Paragraph style={{width: '95%'}}>
        Intensive programming lab intended to strengthen skills in programming.
      </Paragraph>
      
      <ScrollView style={{width: '95%'}}>
      <ScrollView horizontal={true}>
        <DataTable>
          <DataTable.Header>
            <DataTable.Title style={{width: 500}}>CRN</DataTable.Title>
            <DataTable.Title>Type</DataTable.Title>
            <DataTable.Title>Section</DataTable.Title>
            <DataTable.Title>Time</DataTable.Title>
            <DataTable.Title>Day</DataTable.Title>
            <DataTable.Title>Location</DataTable.Title>
            <DataTable.Title>Instructor</DataTable.Title>
            <DataTable.Title>GPA</DataTable.Title>
            <DataTable.Title>Professor's Rating</DataTable.Title>
          </DataTable.Header>

          <DataTable.Row>
            <DataTable.Cell style={{width: 500}}>45328</DataTable.Cell>
            <DataTable.Cell>Laboratory</DataTable.Cell>
            <DataTable.Cell>AB1</DataTable.Cell>
            <DataTable.Cell>ARRANGED</DataTable.Cell>
            <DataTable.Cell>n.a.</DataTable.Cell>
            <DataTable.Cell>ARR Siebel Center for Comp Sci</DataTable.Cell>
            <DataTable.Cell>Woodley, M</DataTable.Cell>
            <DataTable.Cell>3.8</DataTable.Cell>
            <DataTable.Cell>4.0</DataTable.Cell>
          </DataTable.Row>
        </DataTable>
      </ScrollView>
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