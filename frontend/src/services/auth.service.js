import axios from "axios";

const API_URL = "http://localhost:8000/user/";

const register = (username, email, password) => {
  return axios.post(API_URL + "register", {
    username,
    email,
    password,
     })
  };

const login = (email, password) => {
    return axios
      .post(API_URL + "login", {
       email,
       password,
     })
     .then((response) => {
      //console.log('X',response)
      if (response.data.accessToken) {
        localStorage.setItem("user", JSON.stringify(response.data));
      }
      return response});
      };
    
const logout = () => {
      localStorage.removeItem("user");
    };
    
const authService = {
      register,
      login,
      logout,
    };
    
export default authService;