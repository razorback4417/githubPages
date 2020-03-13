import React from 'react';
import {
  Text,
  View,
  FlatList,
  StyleSheet,
  ScrollView,
  Button,
  Dimensions,
  TouchableOpacity,
} from 'react-native';
import GLOBAL from '../global.js';

import { Ionicons } from '@expo/vector-icons';

import store from '../redux/store';
import { addFavorite, deleteFavorite } from '../redux/actions';

import { Alert } from 'react-native';

function Squares(props) {
  let bData = [];
  for (var i = 0; i < GLOBAL.num; i++) {
    bData.push(GLOBAL.businessLocations[i].name);
  }
  return (
    <View style={{ height: 400, backgroundColor: props.color1 }}>
      {bData.map((item, index) => {
        return (
          <TouchableOpacity
            style={styles.btnContainer}
            index={index}
            onPress={event => {
              Alert.alert('You added a favorite', `${item}`);
              store.dispatch(addFavorite(item));
              console.log(`store = ${JSON.stringify(store.getState())}`);
            }}>
            <Text>{item}</Text>
          </TouchableOpacity>
        );
      })}
    </View>
  );
}

function SquareFavorites(props) {
  let favB = store.getState(); //[{ name: "Domenic's" }, { name: 'Knotty Pine' }]; //
  // for (var i = 0; i < 3; i++) {
  //   favB.push(store.getState().i);
  // }
  //console.log(`favB is ${JSON.stringify(favB)}`);
  //console.log(`square favorites.... ${JSON.stringify(store.getState())}`)
  return (
    <View style={{ height: 400, backgroundColor: props.color1 }}>
      {favB.map((item, index) => {
        return (
          <TouchableOpacity
            style={styles.btnContainer}
            onPress={event => {
              Alert.alert(`You have deleted ${item}`);
              console.log(`store b4 = ${JSON.stringify(store.getState())}`);
              store.dispatch(deleteFavorite(item));
              console.log(`store after= ${JSON.stringify(store.getState())}`);
            }}>
            <Text>{item}</Text>
          </TouchableOpacity>
        );
      })}
    </View>
  );
}

// function Squares(props) {
//   var squares = [];
//   for (var i = 0; i < props.numRows; i++) {
//     squares.push(
//       <View style={{ height: 50, backgroundColor: props.color1 }}>
//         <TouchableOpacity
//           style={styles.btnContainer}
//           onPress={() => {
//             store.dispatch(addFavorite({ name: GLOBAL.businessLocations[0].name }));
//             alert('Pressed');
//             console.log(GLOBAL.businessLocations)
//             //console.log(store.getState());
//           }}>
//           <Ionicons name={'ios-add-circle-outline'} size={25} color={'#bbb'} />
//           <Text>{`${i} ${GLOBAL.businessLocations[i].name}`}</Text>
//         </TouchableOpacity>
//       </View>
//     );
//   }
//   return squares;
// }

// function SquareFavorites(props) {
//   var squares = [];
//   for (var i = 0; i < props.numRows; i++) {
//     squares.push(
//       <View style={{ height: 50, backgroundColor: props.color1 }}>
//         <TouchableOpacity
//           style={styles.btnContainer}
//           onPress={() => {
//             alert('Pressed');
//           }}>
//           <Ionicons
//             name={'ios-close-circle-outline'}
//             size={25}
//             color={'#bbb'}
//           />
//           <Text>{`${store.getState().name}`}</Text>
//         </TouchableOpacity>
//       </View>
//     );
//   }
//   return squares;
// }

export default class FavoriteScreen extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      data: GLOBAL.businessLocations,
    };
  }

  // componentDidMount() {
  //   console.log(GLOBAL.businessLocations)
  // }

  listEmptyComponent = () => {
    return (
      <View>
        <Text style={{ textAlign: 'center', marginTop: 280 }}>
          No Favorites
        </Text>
      </View>
    );
  };

  render() {
    return (
      <View
        style={{
          flex: 1,
          alignItems: 'flex-start',
          backgroundColor: 'yellow',
        }}>
        <View style={{ backgroundColor: '#bbb', flexDirection: 'row' }}>
          <ScrollView
            style={{
              height: Dimensions.get('window').height / 2,
              width: Dimensions.get('window').width,
            }}
            scrollEventThrottle={16}
            ref={scrollView => {
              this._leftView = scrollView;
            }}
            onScroll={e => {
              if (!this.leftIsScrolling) {
                this.rigthIsScrolling = true;
                var scrollY = e.nativeEvent.contentOffset.y;
                this._rightView.scrollTo({ y: scrollY });
              }
              this.leftIsScrolling = true;
            }}>
            <Squares numRows={GLOBAL.num} color1={'#50a2ef'} />
          </ScrollView>
        </View>

        <View style={{ backgroundColor: '#bbb', flexDirection: 'row' }}>
          <ScrollView
            style={{
              justifyContent: 'flex-start',
              height: Dimensions.get('window').height / 2,
              width: Dimensions.get('window').width,
              backgroundColor: 'tomato',
            }}
            ref={scrollView => {
              this._rightView = scrollView;
            }}
            scrollEventThrottle={16}
            onScroll={e => {
              if (!this.rigthIsScrolling) {
                this.leftIsScrolling = true;
                var scrollY = e.nativeEvent.contentOffset.y;
                this._leftView.scrollTo({ y: scrollY });
              }
              this.rigthIsScrolling = true;
            }}>
            <SquareFavorites numRows={GLOBAL.num} color1={'tomato'} />
          </ScrollView>
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  btnContainer: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'stretch',
    alignSelf: 'stretch',
    borderRadius: 10,
  },
});
