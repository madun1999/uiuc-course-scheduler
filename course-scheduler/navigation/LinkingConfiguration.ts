import * as Linking from 'expo-linking';

export default {
  prefixes: [Linking.makeUrl('/')],
  config: {
    screens: {
      Root: {
        screens: {
          Scheduler: {
            screens: {
              SchedulerScreen: 'scheduler',
            },
          },
          Courses: {
            screens: {
              CoursesScreen: 'courses',
            },
          },
          Restrictions: {
            screens: {
              RestrictionsScreen: 'restrictions',
            },
          },
          Factors: {
            screens: {
              FactorsScreen: 'factors',
            },
          },
          Login: {
            screens: {
              LoginScreen: 'login',
            },
          },
          CourseInfo: {
            screens: {
              CourseInfoScreen: 'courseInfo',
            },
          },
          ScheduleView: {
            screens: {
              ScheduleViewScreen: 'scheduleView', 
            },
          },
          Profile: {
            screens: {
              ProfileScreen: 'profile',
            },
          },
        },
      },
      NotFound: '*',
    },
  },
};
