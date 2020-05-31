//import * as React from 'react';
import React, { Component, useState } from 'react';

import { Text, View, TextView, TextInput, StyleSheet, Button, Alert, Constants, SafeAreaView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { NavigationContainer } from '@react-navigation/native';

import GLOBAL from '../global.js';
//export default function RecordScreen() {//class RecordScreen extends React.Component {
function RecordScreenFunction(input) {
  //render() {
  const [text, setText] = useState('');
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Record Here!</Text>
      <TextInput
        style={{ height: 40 }}
        placeholder= "${input}"
        onChangeText={(text) => setText(text)}
        defaultValue={text}
      />
    </View>
  );
  //}
}

export default class RecordScreen extends React.Component {
  state = {
    name: '',
    type: '',
    distance: 0,
    time: 0,
  };

  handleSubmit = () => {
    GLOBAL.gName = this.state.name
    GLOBAL.gType = this.state.type
    GLOBAL.gDistance = this.state.distance
    GLOBAL.gTime = this.state.time
    Alert.alert('Data has been submitted')
  }
  render() {
    return (
      <SafeAreaView style={styles.container}>
        <View>
          <Text> Record </Text>
          <TextInput
            style={styles.input}
            placeholder=" Name Of Run"
            onChangeText={(value) => this.setState({ name: value })}
            value={this.state.name}
            onBlur={() => console.log(`here is the state: ${this.state.name}`)}
          />
          <TextInput
            style={styles.input}
            placeholder=" Type"
            onChangeText={(value) => this.setState({ type: value })}
            value={this.state.type}
          />
          <TextInput
            style={styles.input}
            placeholder=" Distance"
            onChangeText={(value) => this.setState({ distance: value })}
            value={this.state.distance}
          />
          <TextInput
            style={styles.input}
            placeholder=" Time"
            onChangeText={(value) => this.setState({ time: value })}
            value={this.state.time}
          />
          <Button
            style={{borderWidth: 20}}
            title="Submit"
            onPress={() => this.handleSubmit()}
          />
          
        </View>
      </SafeAreaView>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: 15,
    marginHorizontal: 16,
  },
  input: {
    borderWidth: 1,
    borderColor: 'black',
    minWidth: 100,
    marginTop: 20,
    marginBottom: 20,
    marginHorizontal: 20,
    paddingHorizantal: 10,
    paddingVertical: 5,
    borderRadius: 3,
  },
});
