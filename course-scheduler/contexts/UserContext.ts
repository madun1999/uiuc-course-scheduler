import React from 'react';

const UserContext = React.createContext({
  token: "",
  courses: [],
  restrictions: {"minMandatory": 0, "maxAll": 10, breaks: []},
  changeToken: (newToken:string)=>{},
  changeCourses: (newCourses)=>{},
  addCourse: (newCourse)=>{},
  deleteCourse: (deleteCourse)=>{},
  changeRestrictions: (newRestrictions)=>{},
});

export { UserContext };