import React from "react";
import axios from "axios";
import { useNavigate } from 'react-router-dom';
//import { useDispatch } from "react-redux";

const DeleteMovie = async (imdb_id) => {
        //const dispatch = useDispatch();
        console.log(imdb_id)
        try {
         const response = await axios.post('http://localhost:8000/movies/delmovie', 
              {imdb_id} )
         console.log(response)
            if (response.status === 200) {
                window.location.href = "/Home";
                window.location.reload();
              }
            return response;
          } catch(error) {
            // Handle error
            console.error(error);
          }
      };
    
  
  

export default DeleteMovie;