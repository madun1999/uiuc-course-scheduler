import React from 'react';

const UserContext = React.createContext({
  token: "",
  courses: [],
  minMandatory: 0,
  maxCourses: 10,
  breaks: [],
  gpaFactor: 0,
  aRateFactor: 0,
  changeToken: (newToken: string)=>{},
  addCourse: (newCourse)=>{},
  changeCourseMandatory: (courseId, mandatory)=>{},
  deleteCourse: (deleteCourse)=>{},
  changeMinMandatory: (newMinMandatory)=>{},
  changeMaxCourses: (newMaxCourses)=>{},
  addBreak: (newBreak)=>{},
  deleteBreak: (deleteBreak)=>{},
  changeGPAFactor: (newGPAFactor)=>{},
  changeARateFactor: (newARateFactor)=>{},
});

export { UserContext };