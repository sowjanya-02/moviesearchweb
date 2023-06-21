import axios from "axios";




const API_URL = "http://localhost:8000/movies/";

const getMovieContent = () => {
  return axios.get(API_URL + "all");
};


const getMovieSearch = (title) => {
  return axios.post(API_URL+'search',{title})
  .then(response => {
    // Handle successful response
    console.log(response);
    return response;
  })
  .catch(error => {
    // Handle error
    console.error(error);
  });
};



const userService = {
  getMovieContent,
  getMovieSearch,
  
  
  
};

export default userService