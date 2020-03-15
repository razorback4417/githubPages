import React, { Component } from 'react';
import {
  Platform,
  StyleSheet,
  Text,
  View,
  TextInput,
  Button,
  Alert,
  Switch,
  ScrollView,
} from 'react-native';

let id = 0;

const Todo = props => (
  <View style={styles.container}>
    <Switch value={props.todo.checked} onValueChange={props.onToggle} />
    <Text>{props.todo.text}</Text>
  </View>
);

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      TextInputValue: '',
      todos: [],
    };
  }

  buttonClickListener = () => {
    const { TextInputValue } = this.state;
    //Alert.alert(TextInputValue);
    this.addTodo();
    console.log(this.state.todos);
  };

  addTodo() {
    id++;
    const text = `${this.state.TextInputValue}`
    this.setState({
      todos: [...this.state.todos, { id: id, text: text, checked: false }],
    });
  }

  toggleTodo(id) {
    this.setState({
      todos: this.state.todos.map(todo => {
        if (todo.id !== id) return todo;
        return {
          id: todo.id,
          text: todo.text,
          checked: !todo.checked,
        };
      }),
    });
  }

  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.headerText}>Todo List</Text>

        <TextInput
          style={{
            height: 45,
            width: '95%',
            borderColor: 'gray',
            borderWidth: 2,
          }}
          placeholder="   Enter your  'Todo'  item"
          onChangeText={TextInputValue => this.setState({ TextInputValue })}
          underlineColorAndroid="transparent"
        />

        <View style={{ width: '80%', margin: 15 }}>
          <Button
            onPress={this.buttonClickListener}
            title="Add Todo"
            color="#00B0FF"
          />
        </View>

        <Text style={styles.words}>
          {'   '}
          Todo count: {this.state.todos.length}{' '}
        </Text>
        <Text style={styles.words}>
          {'   '}
          Unchecked Todo count:{' '}
          {this.state.todos.filter(todo => !todo.checked).length}
        </Text>

        <ScrollView style={styles.containerTwo}>
          {this.state.todos.map(todo => (
            <Todo
              onToggle={() => this.toggleTodo(todo.id)}
              onDelete={() => this.removeTodo(todo.id)}
              todo={todo}
            />
          ))}
        </ScrollView>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 40,
    paddingLeft: 20,
    paddingBottom: 40,
    //alignItems: "center",
    backgroundColor: '#f2f2f2',
  },
  containerTwo: {
    flex: 1,
    paddingTop: 10,
    paddingLeft: 20,
    paddingBottom: 10,
    //alignItems: "center",
    backgroundColor: '#f2f2f2',
  },
  headerText: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
    fontWeight: 'bold',
  },
  words: {
    fontSize: 18,
    color: 'gray',
    fontWeight: 'bold',
  },
});
