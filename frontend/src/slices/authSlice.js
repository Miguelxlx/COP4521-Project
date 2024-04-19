import {createSlice} from '@reduxjs/toolkit';

const initialState = {
    userInfo: localStorage.getItem('userInfo') ? JSON.parse(localStorage.getItem('userInfo')) : null,
}

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setCredentials: (state, action) => {
            state.userInfo = action.payload;
            localStorage.setItem('userInfo', JSON.stringify(action.payload));
        },
        logout: (state, action) => {
            state.userInfo = null;
            localStorage.clear();
        },
        updateUserBalance: (state, action) => {
            if (state.userInfo) {
                state.userInfo.balance = action.payload;  // Update the balance
            }
        },
    }
});

export const { setCredentials, logout, updateUserBalance } = authSlice.actions;

export default authSlice.reducer;