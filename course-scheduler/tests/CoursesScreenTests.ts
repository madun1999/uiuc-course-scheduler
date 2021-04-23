// import React from 'react';
// import renderer, { act } from 'react-test-renderer';
// import axios from 'axios';
// import CoursesScreen from '../screens/CoursesScreen';
//
// jest.mock('axios');
// const mockedAxios = axios as jest.Mocked<typeof axios>;
//
// test('renders undefined response with activity indicator', async () => {
//   mockedAxios.post.mockResolvedValue(undefined);
//   let tree : renderer.ReactTestRenderer | undefined;
//   const navigation : any = { navigate: jest.fn() };
//   const route: any = { params: { login: jest.fn() } };
//   await act(async () => {
//     tree = renderer.create(<FollowingScreen navigation={navigation} route={route} />);
//   });
//   expect(tree?.toJSON()).toMatchSnapshot();
// });