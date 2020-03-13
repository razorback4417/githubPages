import React, { Component } from 'react';
import { Text, View, StyleSheet } from 'react-native';
import { Constants, MapView, Location, Permissions } from 'expo';

import MapScreen from './screens/MapScreen';
import SearchScreen from './screens/SearchScreen';
import FavoriteScreen from './screens/FavoriteScreen';

import {Provider} from 'react-redux'
import store from './redux/store'

import { Ionicons } from '@expo/vector-icons';

import {
  createSwitchNavigator,
  createAppContainer,
} from 'react-navigation';

import { createStackNavigator } from 'react-navigation-stack';
import { createMaterialBottomTabNavigator } from 'react-navigation-material-bottom-tabs';



const MainStack = createStackNavigator(
  {
    _map: MapScreen,
    search: SearchScreen,
  },
  { initialRouteName: 'search' }
);

const HomeNavigator = createSwitchNavigator({
  main: MainStack,
});

const AppNavigator = createMaterialBottomTabNavigator(
  {
    Search: HomeNavigator,
    Favorites: FavoriteScreen,
  },
  {
    defaultNavigationOptions: ({ navigation }) => ({
      tabBarIcon: ({ focused, tintColor }) => {
        const { routeName } = navigation.state;
        let iconName;
        if (routeName === 'Search') {
          iconName = `ios-search`;
        } else if (routeName === 'Favorites') {
          iconName = `ios-thumbs-up`;
        }
        return <Ionicons name={iconName} size={25} color={tintColor} />;
      }
    }),
    tabBarOptions: {
      activeTintColor: 'tomato',
      inactiveTintColor: 'gray',
    },
  }
);

const RootStack = createAppContainer(AppNavigator);


export default class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <RootStack style={styles.container} />
      </Provider>
    );
  }
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    paddingTop: 10,
    backgroundColor: '#ecf0f1',
    padding: 8,
  },
});
