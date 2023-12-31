import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { setMessage } from "./message";

import AuthService from "../services/auth.service";

//
const user = JSON.parse(localStorage.getItem("user"));
//const handleLogout = localStorage.clear();
//const user = {}
export const register = createAsyncThunk(
  "auth/register",
  async ({ username, email, password }, thunkAPI) => {
    try {
      const response = await AuthService.register(username, email, password);
      thunkAPI.dispatch(setMessage(response.data.message));
      return response.data;
    } catch (error) {
      console.log(error)
      const message =
        (error.response &&
          error.response.data &&
          error.response.data.message) ||
        error.message ||
        error.toString();
      thunkAPI.dispatch(setMessage(message));
      return thunkAPI.rejectWithValue();
    }
  }
);

export const login = createAsyncThunk(
  "auth/login",
  async ({ email, password }, thunkAPI) => {
    try {
      const response = await AuthService.login(email, password);
      //console.log(response)
      const { data,headers} = response;
      const user = {"username":data.username,"email":data.email,"accessToken":data.token,
                    "id":data.id,"favoritemovies":data.favoritemovies}
      //console.log(user,'m')
       // Check if the necessary properties are present in the response data
       if (!data || !data.username || !data.token) {
        throw new Error('Invalid response data');
      }
      localStorage.setItem("user", JSON.stringify(user));
      //localStorage.setItem("accessToken", data.token);
      return { user};
    } catch (error) {
      const message =
        (error.response &&
          error.response.data &&
          error.response.data.message) ||
        error.message ||
        error.toString();
      thunkAPI.dispatch(setMessage(message));
      return thunkAPI.rejectWithValue();
    }
  }
);
export const logout = createAsyncThunk("auth/logout", async () => {
    await AuthService.logout();
  });
  
  const initialState = user
    ? { isLoggedIn: true, user }
    : { isLoggedIn: false, user: null };
  
  const authSlice = createSlice({
    name: "auth",
    initialState,
    extraReducers: {
      [register.fulfilled]: (state, action) => {
        state.isLoggedIn = false;
      },
      [register.rejected]: (state, action) => {
        state.isLoggedIn = false;
      },
      [login.fulfilled]: (state, action) => {
        state.isLoggedIn = true;
        state.user = action.payload.user;
      },
      [login.rejected]: (state, action) => {
        state.isLoggedIn = false;
        state.user = null;
      },
      [logout.fulfilled]: (state, action) => {
        state.isLoggedIn = false;
        state.user = null;
      },
    },
  });
  
const { reducer } = authSlice;
export default reducer
