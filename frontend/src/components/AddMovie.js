import React from "react";
import axios from "axios";
import { useNavigate } from 'react-router-dom';
//import { useDispatch } from "react-redux";

const AddMovie = async (imdb_id,id) => {
        //const dispatch = useDispatch();
        console.log(id)
        try {
         const response = await axios.post('http://localhost:8000/user/addmovie', 
              {imdb_id,id} )
          
            if (response.status === 200) {
                window.location.href = "/profile";
              }
            return response;
          } catch(error) {
            // Handle error
            console.error(error);
          }
      };
    
  //if (!currentUser) {
    //console.log(currentUser,'p')
    //return <Navigate to="/Profile" />;
  //}

  

export default AddMovie;