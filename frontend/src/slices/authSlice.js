import {createSlice} from '@reduxjs/toolkit';

const initialState = {
    userInfo: localStorage.getItem('userInfo') ? JSON.parse(localStorage.getItem('userInfo')) : null,
    cumulativeResults: []
}

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setCredentials: (state, action) => {
            state.userInfo = action.payload;
            localStorage.setItem('userInfo', JSON.stringify(action.payload));
        },
        setCumulativeResults: (state, action) => {
            state.cumulativeResults = action.payload; 
        },
        logout: (state, action) => {
            state.userInfo = null;
            localStorage.clear();
        },
    }
});

export const { setCredentials, logout, setCumulativeResults } = authSlice.actions;

export default authSlice.reducer;