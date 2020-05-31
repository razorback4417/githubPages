import React from 'react';
import { Text, View, StyleSheet, TextInput } from 'react-native';
import { Constants } from 'expo';
import axios from 'axios';

export default class SearchScreen extends React.Component {
  state = {
    search: '',
  };

  static navigationOptions = ({ navigation }) => {
    return { headerTitle: 'Search' };
  };

  handleSearch = search => {
    this.setState({ search });
    this.props.navigation.push('_map', this.state.search);
  };

  render() {
    return (
      <View styles={{ flex: 1 }}>
        <TextInput
          style={styles.input}
          placeholder="  Search..."
          value={this.state.search}
          onChangeText={(search) => this.setState({search})}
          onSubmitEditing={this.handleSearch}
        />
      </View>
    );
  }
}

const styles = StyleSheet.create({
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
