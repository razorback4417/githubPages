import React from 'react';
import {
  Text,
  View,
  StyleSheet,
  ScrollView,
  TextInput,
  FlatList,
} from 'react-native';
import { Constants } from 'expo';

import Row from '../Row';

const KEY = 'a0a882ab';

export default class SearchScreen extends React.Component {
  state = {
    search: '',
    data: [],
    pages: 1,
    page: 2,
    refresh: false,
  };

  static navigationOptions = ({ navigation }) => {
    return { headerTitle: 'Home' };
  };

  getMoviesFromApiAsync = () => {
    if (this.state.search.length < 3) {
      this.setState({
        data: [],
      });
    }
    
    //https://www.omdbapi.com/?apikey=a0a882ab&s=titanic
    return fetch(
      `https://www.omdbapi.com/?apikey=${KEY}&s=${this.state.search}`
    )
      .then(response => response.json())
      .then(responseJson => {
        const { Search } = responseJson;
        this.setState({
          data: [...Search],
          pages: Math.ceil(+responseJson.totalResults / 10),
        });
      })
      .catch(err => {
        console.log(err);
      });
  };

  getMoviesWhenScrolling = () => {
    if (this.state.data.length === 0 || this.state.page === this.state.pages) {
      return;
    }
    return fetch(
      `http://www.omdbapi.com/?apikey=${KEY}&s=${
        this.state.search
      }&page={this.state.page}`
    )
      .then(response => response.json())
      .then(responseJson => {
        const newData = this.state.data.concat(responseJson.Search);
        this.setState(prevstate => ({
          data: [...newData],
          page: prevstate.page + 1,
          refresh: !prevstate.refresh,
        }));
      })
      .catch(err => {
        console.log(err);
      });
  };

  handleSearch = search => {
    this.setState({ search }, () => this.getMoviesFromApiAsync());
  };

  handleSelectMovie = movie => {
    this.props.navigation.push('movie', movie);
  };

  listEmptyComponent = () => (
    <Text style={{ textAlign: 'center', marginTop: 30 }}>No results</Text>
  );

  render() {
    return (
      <View styles={{ flex: 1 }}>
        <TextInput
          style={styles.input}
          placeholder="Search..."
          value={this.state.search}
          onChangeText={this.handleSearch}
        />
        <FlatList
          ListEmptyComponent={this.listEmptyComponent}
          keyExtractor={(item, index) => index.toString()}
          renderItem={({ item }) => (
            <Row {...item} onSelectMovie={this.handleSelectMovie} />
          )}
          data={this.state.data}
          extraData={this.state.refresh}
          onEndReached={() => this.getMoviesWhenScrolling()}
          onEndReachedThreshold={0.4}
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
