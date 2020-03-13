// // action types
// const UPDATE_FAVORITE = 'UPDATE_FAVORITE'

// class Store {
//   constructor(reducer, initialState) {
//     this.reducer = reducer
//     this.state = initialState
//   }

//   getState() {
//     return this.state
//   }

//   dispatch(update) {
//     this.state = this.reducer(this.state, update)
//   }
// }

// const DEFAULT_STATE = {favorites: []}

// const merge = (prev, next) => Object.assign({}, prev, next)

// const favoriteReducer = (state, action) => {
//   if (action.type === UPDATE_FAVORITE) return [...state, action.payload]
//   return state
// }

// const reducer = (state, action) => ({
//   favorites: favoriteReducer(state, action),
// })

// const addFavorite = newFavorite => ({
//   type: UPDATE_FAVORITE,
//   payload: newFavorite,
// })

// const store = new Store(reducer, DEFAULT_STATE)

// store.dispatch(addFavorite({name: 'jordan h'}))
// store.dispatch(addFavorite({name: 'jordan h'}))
// store.dispatch(addFavorite({name: 'david m'}))

// console.log("here")
// console.log(store.getState())

//---------------------------------------------------------------------------------------------------
import { createStore } from 'redux';

import { addFavorite, deleteFavorite } from './actions';
import { ADD_FAVORITE } from './actions';

import reducer from './reducer';

import GLOBAL from '../global.js';

const DEFAULT_STATE = [];
const store = createStore(reducer, DEFAULT_STATE);
console.log(store.getState());

export default store;

//---------------------------------------------------------------------------------------------------
/*
store.dispatch(updateUser({foo: 'foo'}))
store.dispatch(updateUser({bar: 'bar'}))
store.dispatch(updateUser({foo: 'baz'}))
*/

// store.dispatch(addFavorite({name: 'Theo', address: 'location'}))

//console.log("here")
