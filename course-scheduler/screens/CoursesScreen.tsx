import * as React from 'react';
import { StyleSheet } from 'react-native';

import { View } from '../components/Themed';
import {Title, Button, Card, Subheading, Switch, TextInput} from 'react-native-paper';
import { ScrollView } from 'react-native-gesture-handler';

import {BottomTabNavigationProp} from "@react-navigation/bottom-tabs";
import {BottomTabParamList} from "../types";

// type CoursesScreenNavigationProp = BottomTabNavigationProp<BottomTabParamList, 'CourseInfo'>;
// type CoursesScreenProps = {
//   navigation: CoursesScreenNavigationProp,
// };

export default function CoursesScreen({ navigation }) {
  const [subjectText, setSubjectText] = React.useState('');
  const [courseText, setCourseText] = React.useState('');

  const [isSwitchOn, setIsSwitchOn] = React.useState(false);
  const onToggleSwitch = () => setIsSwitchOn(!isSwitchOn);

  return (
    <View style={styles.container}>
      <TextInput
        style={{ width: '95%', marginVertical: 3}}
        label="Subject"
        value={subjectText}
        onChangeText={text => setSubjectText(subjectText)}
      />
      <TextInput
        style={{ width: '95%', marginBottom: 3}}
        label="Course"
        value={courseText}
        onChangeText={text => setCourseText(courseText)}
      />
      <Button style={{ width: '95%' }} icon="plus-thick" mode="contained" onPress={() => console.log()}>
        Add Courses
      </Button>
      <Title style={{ textAlign: 'left', width: '95%'}}>Courses</Title>
      <Subheading style={{ textAlign: 'left', width: '95%', marginTop: 5}}>mandatory?</Subheading>
      <ScrollView style={{width: '95%'}}>
        <Card style={{marginVertical: 5}}>
          <Card.Content>
            <View style={{ flexDirection: 'row', alignItems: 'center'}}>
              <Switch style={{ width: '10%'}} value={isSwitchOn} onValueChange={onToggleSwitch} />
              <Button style={{ width: '45%'}} mode="text" onPress={() => navigation.push('CourseInfoScreen')}>
                View More 
              </Button>
              <Subheading style={{ width: '35%' }}>
                CS 242
              </Subheading>
              <Button style={{ width: '10%'}} icon="delete" mode="text" onPress={() => console.log()}>
              </Button>
            </View>
          </Card.Content>
        </Card>
        <Card style={{marginVertical: 5}}>
          <Card.Content>
            <View style={{ flexDirection: 'row', alignItems: 'center'}}>
              <Switch style={{ width: '10%'}} value={isSwitchOn} onValueChange={onToggleSwitch} />
              <Button style={{ width: '45%'}} mode="text" onPress={() => console.log()}>
                View More 
              </Button>
              <Subheading style={{ width: '35%' }}>
                MATH 417
              </Subheading>
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
  button: {
    margin: 2,
    width: '95%'
  },
});
