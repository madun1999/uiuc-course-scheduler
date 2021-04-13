# Test plan

## Set up and Prerequisites
- running python server
  - set up python server according to `README.md`
- Working MongoDB
    - set up `.env` file according to `README.md`
- nodejs
  - set up expo app according to `README.md`

## Test Cases
### Login
    - Login screen with a button
![alt text](../resource/screenshots/login.png "Login")
### Google Login
    - Google login screen pop up
    - Navigate to User profile screen afterwards
![alt text](../resource/screenshots/google.png "Google")
    - User id and email stored in database
![alt text](../resource/screenshots/mongodb.png "MongoDB")
### User Profile
    - Shows user email
    - Logout button that sends back to login screen
![alt text](../resource/screenshots/user_profile.png "User Profile")
    - Shows error if error
![alt text](../resource/screenshots/error.png "Error")