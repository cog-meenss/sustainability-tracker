import { configureStore } from '@reduxjs/toolkit';

// Example basic reducer (replace with your actual reducers)
const initialState = {};
function rootReducer(state = initialState, action) {
  switch (action.type) {
    default:
      return state;
  }
}

const store = configureStore({
  reducer: rootReducer,
});

export default store;
