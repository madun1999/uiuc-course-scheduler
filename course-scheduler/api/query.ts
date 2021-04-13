/**
 * File for API calls to backend
 */
import UserProfile from "./UserProfile";
import axios from 'axios';

const API_URL = 'http://localhost:5000/api'


// get user profile 
export async function getUserProfile(token : string) : Promise<UserProfile> {
    const config = {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    };
    let response = await axios.post<any>(API_URL + '/login', "", config);
    response = await axios.get<any>(API_URL + '/user', config);
    console.log(response.data);
    return new UserProfile(response.data.email);
}

// deactivate user 
export async function deactivate(token : string) : Promise<void> {
  const config = {
    headers: {
      Authorization: `bearer ${token}`,
    },
  };
  const response = await axios.delete<any>(API_URL + '/deactivate', config);
}