// action types
import { ADD_FAVORITE, DELETE_FAVORITE } from './actions';
//const merge = (prev, next) => Object.assign({}, prev, next);
//const reducer = (state, update) => merge(state, update);
//let state = [];

const deleteFav = (state, action) => {
  console.log(`the action is ${JSON.stringify(action)}`);
  console.log(`the state is ${JSON.stringify(state)}`);
  const index = state.indexOf(action);
  console.log(index);
  const stateTemp = [...state.slice(0, index), ...state.slice(index + 1)];
  //console.log(`the stateTemp is ${JSON.stringify(stateTemp)}`)
  return stateTemp;
  //return ( state.filter((val, i) => i !== action.payload ) )
  // console.log(`deleteFav has been run....... the action is ${JSON.stringify(action)}`)
  // console.log(`deleteFav has been run....... the state is ${JSON.stringify(state)}`)
  // return [
  //   ...state.slice(0, action),
  //   ...state.slice(action + 1)
  // ]
};

const reducer = (state, action) => {
  if (action.type === DELETE_FAVORITE)
    return deleteFav(state, action.payload);
  if (action.type === ADD_FAVORITE) return [...state, action.payload];
  return state;
};
// const reducer = (state, action) => {
//   if (action.type === DELETE_FAVORITE) return [
//       ...state.slice(0, action.payload),
//       ...state.slice(action.payload + 1),
//     ];
//   if (action.type === ADD_FAVORITE) return [...state, action.payload];
//   return state;
// };

// const reducer = (state, action) => {
//   switch (action.type) {
//     case ADD_FAVORITE:
//       return [
//         ...state,
//         ...action.payload
//       ]
//     case DELETE_FAVORITE:
//       return [
//         ...state.slice(0, action.payload),
//         ...state.slice(action.payload + 1),
//       ]
//   }
// };

export default reducer;

// const reducer = (state, action) => ({
//   favorites: favoritesReducer(this.state, action),
// })

//------------------------------------------------------------------------------------------------------------

// import { ADD_FAVORITE, DELETE_FAVORITE } from './actions';

// const merge = (prev, next) => Object.assign({}, prev, next)

// const reducer = (state, update) => merge(state, update)

// let state = {}
// state = reducer(state, {foo: 'foo'})
// state = reducer(state, {bar: 'bar'})
// state = reducer(state, {foo: 'baz'})

// state = reducer(state, {'name':'Express Gourmet'})
// state = reducer(state, {'name1':'The Linden Store'})
// state = reducer(state, {name2:'Riverbend Bar & Grill'})

// console.log(state)

//export default reducer;

//------------------------------------------------------------------------------------------------------------
// const merge = (prev, next) => Object.assign({}, prev, next);

// const reducer = (state, update) => ({
//   ...state,
//   ...update,
// })

// const reducer = (state = {}, action) => {
//   switch (action.type) {
//     case ADD_FAVORITE:
//     return [
//       ...state,
//       ...action.payload
//     ]
//       //return merge(state, action.payload);
//     case DELETE_FAVORITE:
//       return action.payload //return merge(state, action.payload)
//     default:
//       return state;
//   }
// };
