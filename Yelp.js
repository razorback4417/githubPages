import React, { Component } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import axios from 'axios';

import GLOBAL from '../global.js'

export const getData = (userLocation, search) => {
  return axios
    .get('https://api.yelp.com/v3/businesses/search', {
      headers: {
        Authorization:
          'Bearer IDcg2dhsQ2uoWHzmtpvyAFGW5mRuAEipU9RbkZGodquVjhLjQAc1NbyShQ_9-rlxa0-sj3xvhxZcCybuucY22Vtc7PLqviYxXfGIQKo1WCPi6K63wbHBDOs1HXlLXXYx',
      },
      params: {
        limit: GLOBAL.num,
        term: search,
        longitude: userLocation.coords.longitude,
        latitude: userLocation.coords.latitude,
      },
    })
    .then(response =>
      response.data.businesses.map(business => {
        return {
          coords: business.coordinates,
          name: business.name,
          location: business.location.address1,
          phone: business.display_phone,
        };
      })
    );
};

// export const a = 1;