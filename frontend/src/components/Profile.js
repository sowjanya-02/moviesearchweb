import React,{ useEffect, useState } from "react";
import { Navigate } from 'react-router-dom';
import { useSelector } from "react-redux";
import addMovieToFavorite  from "./AddMovieFav";

const Profile = () => {
  
  const { user: currentUser } = useSelector((state) => state.auth);
  const [favoriteMovies, setFavoriteMovies] = useState([]);

  console.log(currentUser,'m')
  const handleAddMovieToFavorite = async (id) => {
    try {
      const response = await addMovieToFavorite(id);
      
      // Update the favorite movies list
      setFavoriteMovies(response);
      
    } catch (error) {
      console.error('Error adding movie to favorites:', error);
    }
  };
  
  if (!currentUser) {
    console.log(currentUser)
    return <Navigate to="/login" />;
  }

  return (
    <div className="container">
      <header className="jumbotron">
        <h3>
        
          <strong>{currentUser.username}</strong>
        </h3>
      </header>
      <div>
      <p>
        <strong>Id:</strong> {currentUser.id}
      </p>
      <p>
        <strong>Email:</strong> {currentUser.email}
      </p>
      <p>
        <strong>Favorite Movies:</strong>
      </p>
      <button onClick={() => handleAddMovieToFavorite(currentUser.id)}>Show Favorites</button>
      {favoriteMovies.map((movie) => (
          
          <div key={movie.imdb_id}>
            <img src={movie.poster} alt={movie.Title} style={{ width: '100px', height: 'auto' }} /> 
            <p>Year: {movie.year}</p>
            

          </div>
        ))}
       </div>
     
      <ul>
        {currentUser.roles &&
          currentUser.roles.map((role, index) => <li key={index}>{role}</li>)}
      </ul>
    </div>
  );
};

export default Profile;