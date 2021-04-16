import { MaterialCommunityIcons } from '@expo/vector-icons';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import * as React from 'react';

import Colors from '../constants/Colors';
import useColorScheme from '../hooks/useColorScheme';
import SchedulerScreen from '../screens/SchedulerScreen';
import CoursesScreen from '../screens/CoursesScreen';
import RestrictionsScreen from '../screens/RestrictionsScreen';
import FactorsScreen from '../screens/FactorsScreen';
import LoginScreen from '../screens/LoginScreen';
import CourseInfoScreen from '../screens/CourseInfoScreen'
import ScheduleViewScreen from '../screens/ScheduleViewScreen'
import ProfileScreen from '../screens/ProfileScreen';
import { BottomTabParamList, 
  SchedulerParamList, 
  ScheduleViewParamList, 
  CoursesParamList, 
  CourseInfoParamList, 
  RestrictionsParamList, 
  FactorsParamList, 
  LoginParamList, 
  ProfileParamList
} from '../types';

const BottomTab = createBottomTabNavigator<BottomTabParamList>();

export default function BottomTabNavigator() {
  const colorScheme = useColorScheme();

  return (
    <BottomTab.Navigator
      initialRouteName="Scheduler"
      tabBarOptions={{ activeTintColor: Colors[colorScheme].tint }}>
      <BottomTab.Screen
        name="Scheduler"
        component={SchedulerNavigator}
        options={{
          tabBarIcon: ({ color }) => <TabBarIcon name="calendar-edit" color={color} />,
        }}
      />
      <BottomTab.Screen
        name="Courses"
        component={CoursesNavigator}
        options={{
          tabBarIcon: ({ color }) => <TabBarIcon name="book" color={color} />,
        }}
      />
      <BottomTab.Screen
        name="Restrictions"
        component={RestrictionsNavigator}
        options={{
          tabBarIcon: ({ color }) => <TabBarIcon name="alert-octagon" color={color} />,
        }}
      />
      <BottomTab.Screen
        name="Factors"
        component={FactorsNavigator}
        options={{
          tabBarIcon: ({ color }) => <TabBarIcon name="swap-vertical-bold" color={color} />,
        }}
      />
      {/*<BottomTab.Screen*/}
      {/*  name="Login"*/}
      {/*  component={LoginNavigator}*/}
      {/*  options={{*/}
      {/*    tabBarIcon: ({ color }) => <TabBarIcon name="ios-code" color={color} />,*/}
      {/*  }}*/}
      {/*/>*/}
      <BottomTab.Screen
        name="Profile"
        component={ProfileNavigator}
        options={{
          tabBarIcon: ({ color }) => <TabBarIcon name="account" color={color} />,
        }}
      />
    </BottomTab.Navigator>
  );
}

// You can explore the built-in icon families and icons on the web at:
// https://icons.expo.fyi/
function TabBarIcon(props: { name: React.ComponentProps<typeof MaterialCommunityIcons>['name']; color: string }) {
  return <MaterialCommunityIcons size={24} style={{ marginBottom: -3 }} {...props} />;
}

// Each tab has its own navigation stack, you can read more about this pattern here:
// https://reactnavigation.org/docs/tab-based-navigation#a-stack-navigator-for-each-tab
const SchedulerStack = createStackNavigator<SchedulerParamList>();

function SchedulerNavigator() {
  return (
    <SchedulerStack.Navigator>
      <SchedulerStack.Screen
        name="SchedulerScreen"
        component={SchedulerScreen}
        options={{ headerTitle: 'Scheduler' }}
      />
      <SchedulerStack.Screen
        name="ScheduleViewScreen"
        component={ScheduleViewScreen}
        options={{ headerTitle: 'Schedule View' }}
      />
    </SchedulerStack.Navigator>
  );
}

const CoursesStack = createStackNavigator<CoursesParamList>();

function CoursesNavigator() {
  return (
    <CoursesStack.Navigator>
      <CoursesStack.Screen
        name="CoursesScreen"
        component={CoursesScreen}
        options={{ headerTitle: 'Courses' }}
      />
      <CoursesStack.Screen
        name="CourseInfoScreen"
        component={CourseInfoScreen}
        options={{ headerTitle: 'Course Information' }}
      />
    </CoursesStack.Navigator>
  );
}

const RestrictionsStack = createStackNavigator<RestrictionsParamList>();

function RestrictionsNavigator() {
  return (
    <RestrictionsStack.Navigator>
      <RestrictionsStack.Screen
        name="RestrictionsScreen"
        component={RestrictionsScreen}
        options={{ headerTitle: 'Restrictions' }}
      />
    </RestrictionsStack.Navigator>
  );
}

const FactorsStack = createStackNavigator<FactorsParamList>();

function FactorsNavigator() {
  return (
    <FactorsStack.Navigator>
      <FactorsStack.Screen
        name="FactorsScreen"
        component={FactorsScreen}
        options={{ headerTitle: 'Factors\' Importance' }}
      />
    </FactorsStack.Navigator>
  );
}

// const LoginStack = createStackNavigator<LoginParamList>();
// function LoginNavigator() {
//   return (
//     <LoginStack.Navigator>
//       <LoginStack.Screen
//         name="LoginScreen"
//         component={LoginScreen}
//         options={{ headerTitle: 'Login' }}
//       />
//     </LoginStack.Navigator>
//   );
// }

const ProfileStack = createStackNavigator<ProfileParamList>();
function ProfileNavigator() {
  return (
    <ProfileStack.Navigator initialRouteName="ProfileScreen">
      <ProfileStack.Screen
        name="ProfileScreen"
        component={ProfileScreen}
        options={{ headerTitle: 'Profile' }}
      />
      <ProfileStack.Screen
        name="LoginScreen"
        component={LoginScreen}
        options={{ headerTitle: 'Login' }}
      />
    </ProfileStack.Navigator>
  );
}
