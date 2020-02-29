import * as React from 'react';
import { Text, View, StyleSheet } from 'react-native';
import { Constants } from 'expo';
import MovieScreen from './screens/MovieScreen';
import SearchScreen from './screens/SearchScreen';

// import AssetExample from './components/AssetExample';

import { Card } from 'react-native-paper';

import {
  createStackNavigator,
  createSwitchNavigator,
  createBottomTabNavigator,
  createAppContainer,
} from 'react-navigation';

const MainStack = createStackNavigator(
  {
    movie: MovieScreen,
    search: SearchScreen,
  },
  { initialRouteName: 'search' }
);

const AppNavigator = createSwitchNavigator({
  main: MainStack,
});

const RootStack = createAppContainer(AppNavigator);

export default class App extends React.Component {
  render() {
    return <RootStack style={styles.container} />;
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    paddingTop: Constants.statusBarHeight,
    backgroundColor: '#ecf0f1',
    padding: 8,
  },
});
