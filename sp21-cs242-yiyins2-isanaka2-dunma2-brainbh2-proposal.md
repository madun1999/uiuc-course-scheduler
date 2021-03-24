# UIUC Course Scheduler
Dun Ma (dunma2) Moderator: Brian Huang (brianbh2) 

Yiyin Shen (yiyins2) Moderator: Akhil Isanaka (isanaka2)


## Abstract 
---
### Project Purpose 
Create a mobile app that show information about courses user added fetched from various platforms (Course Explorer, Rate My Professor, GPAs of Every Courses at UIUC) and generate possible schedules accordingly. 

### Project Motivation 
Students need to visit a lot of platforms to fetch information about one course and it takes a great deal of effort to manually generate a schedule to balance all the factors (GPAs, professor ratings). This app want to minimize this effort by writing a smart algorithm to generate possible schedules and give scores of each schedule by user-given factors' weight. 

## Technical Specification
---
- Data Sources: 
  - CIS API (https://courses.illinois.edu/cisdocs/) (RESTful API)
  - Rate My Professor (Selenium)
  - GPAs of Every Courses at UIUC (Static)
- Programming Language: mobile app: JavaScript; backend: python 
- Stylistic Conventions: Python style guide, JavaScript Style Guide 
- IDE: Visual Studio Code, PyCharm Professional 
- Interface: React Native
- Backend: Flask, MongoDB, Selenium, GraphQL API

## Functional Specification
---
- User can Google sign-in to save courses and schedules. 
- For each course the following information will be demonstrated:
  - general information (meeting time, location, instructors, and etc.) from course explorer; 
  - ratings of professors, difficulties of the course, will-take-again rate, popular comments from rate my professor;
  - GPAs for each professor from GPAs of Every Courses at UIUC.
- User can input the year and semester to add courses and generate schedule. 
- User can mark each course as mandatory or elective. 
- User can input the minimum number of mandatory courses to take. 
- User can input the maximum number of courses to take. 
- User can input break time. 
- All possible schedules will be demonstrated with the above restrictions.
- A set of sliders (from very unimportant to very important) allows user to input the importance of each factor. The factors are: 
  - GPA
  - Professor rating
  - Course difficulty
  - Will-take-again rate
- A score will be generated for each schedule based on the above factors. 

## Brief Timeline
---
### Week 1: 
Dun Ma: 
- Create a Selenium scrapper (We chose Selenium since Rate My Professor updates dynamically.) 
- Scrape the following information from Rate My Professor:
  - For each course: 
    - Professor's rating 
    - Course difficulty
    - Will-take-again rate 
    - Popular comments 
    - Number of ratings/comments 
- Store the above information into MongoDB 

Yiyin Shen: 
- Set up Flask server 
- Connect with CIS API 
- Given the year and semester: 
  - Fetch a list of all subjects in UIUC
  - Fetch a list of all courses for each subject
  - Store the above information into MongoDB
  - Able to fetch all information about the course and their IDs, including: 
    - Course explorer URL 
    - Year
    - Semester 
    - Subject 
    - Course name 
    - Description 
    - Credit hours 
    - For each section: 
      - Section number 
      - Status code
      - Section status code 
      - Part of term 
      - Enrollment status 
      - Start date 
      - End date 
      - Start time 
      - End time 
      - Days of the Week 
      - Room number 
      - Building name
      - Instructors
  - Store above information into MongoDB
  
### Week 2: 
Dun Ma: 
- Create a GraphQL API: 
  - api/subjects/[semester-year] to get a list of all subjects offered at semester-year 
  - api/courses/[semester-year]/[subject] to get a list of all courses offered by subject at semester-year 
  - api/course-info/[semester-year]/[subject-course number] to get all course information by the course offered at semester-year
  - api/schedules/[semester-year]/[subject1-course number1, subject2-course number2, ...] to get all possible schedules given the list of courses. 
- Create an algorithm to generate schedules based on courses and restrictions. 

Yiyin Shen: 
- Clean up GPA data from GPAs of Every Courses at UIUC.
- Store GPA data into MongoDB
- Create the following UI screens: 
  - Home:
    - add course + course list
    - generate schedule + schedule list
    - restrictions inputs
    - factor importance sliders
  - View courses' information 
  - View schedule 
  
### Week 3:
Dun Ma: 
- Create an algorithm to score a schedule based on importance factors
- Update api/schedules with score


Yiyin Shen  
- Enable Google sign in 
- Fetch Google user information: 
  - Six fields of Google ID Token
  - email
  - name
- Store the above user information into MongoDB 
- Save liked schedules into MongoDB 
- More API commands: 
  - api/user/[user-id] to get user information
  - api/saved-schedules/[user-id] to get user's saved schedules
- UI: 
  - Profile screen: 
    - User information 
    - Saved schedules
  - Sign in screen: 
  
### Week 4: 
## Rubrics
---
### Week 1: 
Dun Ma: 
| Category | Total Score Allocated | Detailed Rubrics |
| --- | --- | --- |
| Unit Test | 5 | +0.5 per unit test |

Yiyin Shen: 
| Category | Total Score Allocated | Detailed Rubrics |
| --- | --- | --- |
| Set up Flask server | 1 | +1 properly set up Flask server |
| Connect with CIS API | 1 | +1 successfully connect with CIS API |
| Fetch a list of all subjects | 2 | +1 fetch and parse <br> + 1 store in MongoDB |
| Fetch a list of all courses | 2 | +1 fetch and parse <br> + 1 store in MongoDB |
| Create a Course type/object | 1 | +1 create a course type/object |
| Fetch course information | 4 | +1 fetch <br> +2 parse into Course type/object <br> + 1 store in MongoDB |
| Unit test | 5 | +0.5 per unit test |

### Week 2: 
Dun Ma: 
| Category | Total Score Allocated | Detailed Rubrics |
| --- | --- | --- |
| Set up GraphQL API | 1 | +1 properly set up GraphQL API |
| api/subjects/[semester-year] | 3 | +2 support this API command and return correctly <br> +1 error handling |
| api/courses/[semester-year]/[subject] | 3 | +2 support this API command and return correctly <br> +1 error handling |
| api/course-info/[semester-year]/[subject-course number] | 3 | +2 support this API command and return correctly <br> +1 error handling |
| api/schedules/[semester-year]/[subject1-course number1, subject2-course number2, ...]| 3 | +2 support this API command and return correctly <br> +1 error handling |
| Schedule object | 2 | +2 properly create the Schedule type/object |
| Schedule Algorithm | 5 | +1 schedules are correct <br> +2 implement restrictions <br> +2 use some advanced techniques to improve efficiency (e.g. dynamic programming) |
| Unit Test | 6 | +0.5 per unit test |

Yiyin Shen: 
| Category | Total Score Allocated | Detailed Rubrics |
| --- | --- | --- |
| GPA Data Cleaning | 5 | +1 convert GPA data into propitiate format <br> +2 store GPA to corresponding course information <br> +2 for error handling (missing/wrong GPA, instructor, etc.) |
| Set up React Native App | 1 | +1 properly set up React Native App |
| Home Screen | 5 | +1 add course form & course list <br> +1 generate schedule button & schedule list <br> + 2 restriction input forms <br> +1 importance factors' sliders |
| Course information Screen | 5 | +1 general course information <br> +2 section information <br> +2 GPA and Rate My Professor information |
| Schedule Screen | 3 | +1 calendar <br> +2 add courses | 
| Unit Test | 2 | +0.5 per unit test |
| Manual Test Plan | 4 | +1 per screen <br> +1 error handling view |

### Week 3: 
Dun Ma: 
| Category | Total Score Allocated | Detailed Rubrics |
| --- | --- | --- |
| Score Algorithm | 4 | +1 algorithm is correct <br> +2 implement importance factor's weight <br> +1 improve efficiency |
| Add score to API | 1 | +1 successfully add schedule's score to API |
| Unit Test | 4 | +0.5 per unit test |

Yiyin Shen: 
| Category | Total Score Allocated | Detailed Rubrics |
| --- | --- | --- |
| Enable Google sign-in | 2 | +2 properly enable Google sign-in |
| Sign-in Screen | 1 | +1 sign-in button |
| Profile Screen | 2 | +1 user information <br> +1 saved schedule list |
| Fetch user information from Google | 1 | +1 successfully fetch information |
| Store user information into MongoDB | 1 | +1 successfully stored information |
| api/user/[user-id] | 3 | +2 support this API command and return correctly <br> +1 error handling |
| api/saved-schedules/[user-id] | 3 | +2 support this API command and return correctly <br> +1 error handling |
| Unit test | 3 | +0.5 per unit test |
| Manual Test Plan | 3 | +1 per screen <br> +1 error handling view |

### Week 4: 
Dun Ma: 
| Category | Total Score Allocated | Detailed Rubrics |
| --- | --- | --- |

Yiyin Shen: 
| Category | Total Score Allocated | Detailed Rubrics |
| --- | --- | --- |

## Figure
---
