// action types
export const ADD_FAVORITE = 'ADD_FAVORITE'
export const DELETE_FAVORITE = 'DELETE_FAVORITE'

// action creators
export const addFavorite = update => ({
  type: ADD_FAVORITE,
  payload: update,
})

export const deleteFavorite = update => ({
  type: DELETE_FAVORITE,
  payload: update,
})