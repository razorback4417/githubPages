import React, { Component } from 'react';
import { Text, View, StyleSheet } from 'react-native';
import { Location, Permissions } from 'expo';
import MapView, { Marker } from 'react-native-maps';
import Constants from 'expo-constants';

import * as getStuff from '../data/Yelp';

import GLOBAL from '../global.js';

export default class MapScreen extends Component {
  state = {
    mapRegion: {
      latitude: 0,
      longitude: 0,
      latitudeDelta: 0,
      longitudeDelta: 0,
    },
    //userLocationResult: null,
    //userLocation: { coords: { latitude: 0, longitude: 0 } },
    myStoreLocations: [
      { coords: { latitude: 37.785155, longitude: -122.432075 } },
    ],
    location: { coords: { latitude: 0.0, longitude: 0.0 } },
  };

  static navigationOptions = ({ navigation }) => {
    return { headerTitle: 'Map' };
  };

  componentDidMount() {
    //this._getLocationAsync();
    this.findCoordinates();
    //this._getData();
    //console.log(this.props.navigation.state.params)
  }

  _getData = async () => {
    let storeLocations = [];
    storeLocations = await getStuff.getData(
      this.state.location,
      //this.state.userLocation,
      this.props.navigation.state.params
    );
    GLOBAL.businessLocations = storeLocations;
    this.setState({
      myStoreLocations: storeLocations,
    });
    //console.log(this.state.location);
    //console.log(this.state.myStoreLocations);
  };

  _handleMapRegionChange = mapRegion => {
    this.setState({ mapRegion });
  };

  findCoordinates = async () => {
    await navigator.geolocation.getCurrentPosition(
      location => {
        this.setState({ location });
        let data = this._getData();
        //console.log(this.state.location);
      },
      error => alert(error.message),
      { enableHighAccuracy: false, timeout: 5000, maximumAge: 0 }
    );

    //
  };

  // findCoordinates = () => {
  //   navigator.geolocation.getCurrentPosition(
  //     location => {
  //       this.setState({ location });
  //     },
  //     error => alert(error.message),
  //     { enableHighAccuracy: false, timeout: 5000, maximumAge: 0 }
  //   );
  //   //let data = setTimeout(this._getData(), 5000)

  //   let data = this._getData();
  // };

  // _getLocationAsync = async () => {
  //   let { status } = await Permissions.askAsync(Permissions.LOCATION);
  //   if (status !== 'granted') {
  //     this.setState({
  //       userLocationResult: 'Permission to access location was denied',
  //       Location,
  //     });
  //   }

  //   let userLocation = await Location.getCurrentPositionAsync({});
  //   this.setState({
  //     userLocationResult: JSON.stringify(userLocation),
  //     userLocation,
  //   });
  // let data = this._getData();
  // };

  render() {
    return (
      <MapView
        style={styles.map}
        region={{
          latitude: this.state.location.coords.latitude,
          longitude: this.state.location.coords.longitude,
          //latitude: this.state.userLocation.coords.latitude,
          //longitude: this.state.userLocation.coords.longitude,
          latitudeDelta: 0.0922,
          longitudeDelta: 0.0421,
        }}
        onRegionChange={this._handleMapRegionChange}>
        <Marker
          coordinate={this.state.location.coords}
          //coordinate={this.state.userLocation.coords}
          title="Current Location"
          description="You are here"
          pinColor="#50a2ef"
        />
        {this.state.myStoreLocations.map((item, index) => {
          return (
            <Marker
              coordinate={{
                latitude: item.coords.latitude,
                longitude: item.coords.longitude,
              }}
              title={item.name}
              description={item.location + ' ' + item.phone}
              key={index}
              pinColor="tomato"
            />
          );
        })}
      </MapView>
    );
  }
}

const styles = StyleSheet.create({
  map: {
    flex: 1,
    alignItems: 'center',
    alignSelf: 'stretch',
    height: 595,
  },
});

// {this.state.myStoreLocations.map((item, index) => {
//   return (
//     <Marker
//       coordinate={{
//         latitude: item.coords.latitude,
//         longitude: item.coords.longitude,
//       }}
//       title={item.name}
//       description={item.location + ' ' + item.phone}
//       key={index}
//       pinColor="tomato"
//     />
//   );
// })}
