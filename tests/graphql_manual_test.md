# GraphQL Test plan

## Set up and Prerequisites
- running python server
  - set up python server according to `README.md`
- Working MongoDB
    - set up `.env` file according to `README.md`
- Connect to '/graphql' route of the python server in a web browser to use GraphQL Explorer.

## Test Cases
### Subjects
```graphql
query {
  subjects {
    success
    error
    result {
      subjectId
      name
    }
  }
}
```
![alt text](../screenshots/graphql_subjects.png "subjects")

### Courses of subject
```graphql
query {
  courses(subject: "LAS") {
    courseNum
    courseDetail {
      title
    }
  }
}
```
![alt text](../screenshots/graphql_courses.png "courses")

### Course by course_id
```graphql
query {
  course(courseId: "MATH 347") {
    courseNum
    courseDetail {
      title
      credit_hours
      sections {
        sectionId
      }
    }
    subjectId
  }
}
```
![alt text](../screenshots/graphql_course.png "course")

### User information
```graphql
query {
  user {
    id
    email
    name
    picture
  }
}
```
![alt text](../screenshots/graphql_user.png "user")

### Update User
```graphql
mutation {
  updateUser {
    success
  }
}

```
![alt text](../screenshots/graphql_updateUser.png "updateUser")

### Schedule
```graphql
query {
  schedule(courses:["LING 506", "MATH 347"]) {
    success
    errors
    schedules {
      sections {
        sectionId
      }
    }
  }
}
```
![alt text](../screenshots/graphql_schedule.png "schedule")


### Schedule with no Restriction
```graphql
query NormalSchedule{
  scheduleRestriction(
    courses:[{courseId: "LING 506", mandatory: true}, {courseId: "CS 576", mandatory: true}], 
    restrictions:{
    	maxCourses: null
      minMandatory: null
      breaks: []
    }) {
    success
    errors
    schedules {
      sections {
        sectionId
        meetings {
          start
          end
          daysOfTheWeek
        }
      }
    }
  }
}
```
![alt text](../screenshots/graphql_normal_schedule.png "schedule")


### Schedule with minimum mandatory course restriction
```graphql
query MinMandatoryRestriction{
  scheduleRestriction(
    courses:[{courseId: "LING 506", mandatory: true}, {courseId: "CS 576", mandatory: true}], 
    restrictions:{
    	maxCourses: null
      minMandatory: 2
      breaks: []
    }) {
    success
    errors
    schedules {
      sections {
        course {
          subjectId
          courseNum
        }
        sectionId
        meetings {
          start
          end
          daysOfTheWeek
        }
      }
    }
  }
}
```
![alt text](../screenshots/graphql_min_mand_schedule.png "schedule")


### Schedule with maximum course restriction
```graphql
query MaxCourseRestriction{
  scheduleRestriction(
    courses:[{courseId: "LING 506", mandatory: true}, {courseId: "CS 576", mandatory: true}], 
    restrictions:{
    	maxCourses: 1
      minMandatory: null
      breaks: []
    }) {
    success
    errors
    schedules {
      sections {
        sectionId
        meetings {
          start
          end
          daysOfTheWeek
        }
      }
    }
  }
}
```
![alt text](../screenshots/graphql_max_courses_schedule.png "schedule")


### Schedule with break restriction
```graphql
query BreakRestriction{
  scheduleRestriction(
    courses:[{courseId: "LING 506", mandatory: true}, {courseId: "CS 576", mandatory: true}], 
    restrictions:{
    	maxCourses: null
      minMandatory: null
      breaks: [{
        start: "07:00 AM"
        end: "08:00 PM"
        daysOfTheWeek: "MTWRF"
      }]
    }) {
    success
    errors
    schedules {
      sections {
        sectionId
        meetings {
          start
          end
          daysOfTheWeek
        }
      }
    }
  }
}
```
![alt text](../screenshots/graphql_break_schedule.png "schedule")


### Saving Schedule
```graphql
mutation StarSchedule {
  starSchedule (sectionIds: [70099, 71847]){
    success
    errors
  }
}
```
![alt text](../screenshots/graphql_star_schedule.png "schedule")


### Query Saved Schedule
```graphql
query GetUser {
  user {
    staredSchedules {
      sectionId
      course {
        courseNum
        subjectId
      }
    }
  }
}
```
![alt text](../screenshots/graphql_get_star_schedule.png "schedule")