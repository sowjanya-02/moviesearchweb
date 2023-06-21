import React, { useState, useEffect } from "react";
import UserService from "../services/user.service";
import DeleteMovie from "./DeleteMovie";

const Home = () => {
  const [movies, setMovies] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [moviesPerPage] = useState(3 * 5);

  useEffect(() => {
    fetchMovies();
  }, []);

  const fetchMovies = () => {
    UserService.getMovieContent()
      .then((response) => {
        setMovies(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  };
  const handleDeleteMovie = async (id) => {
    try {
      console.log(id)
      const response = await DeleteMovie(id);
      console.log(response,'S');
      // Update the favorite movies list
      //setFavoriteMovies(response);
      
    } catch (error) {
      console.error('Error Deleting movie:', error);
    }
  };

  // Get current movies
  const indexOfLastMovie = currentPage * moviesPerPage;
  const indexOfFirstMovie = indexOfLastMovie - moviesPerPage;
  const currentMovies = movies.slice(indexOfFirstMovie, indexOfLastMovie);

  // Change page
  const paginate = (pageNumber) => {
    setCurrentPage(pageNumber);
  };
  
  return (
    <div className="container">
      <header className="jumbotron">
        <div className="row">
          {currentMovies.map((movie) => (
            <div className="col-lg-4" key={movie.imdb_id}>
              <div className="card mb-4">
                <img
                  className="card-img-top"
                  src={movie.poster}
                  alt={movie.title}
                />
                <div className="card-body">
                  <h5 className="card-title">{movie.title}</h5>
                  <p className="card-text">Year: {movie.year}</p>
                  <p className="card-text">Genre: {movie.genre}</p>
                  <p className="card-text">IMDB ID: {movie.imdb_id}</p>
                  <div className="d-flex justify-content-between">
                  <button className="btn btn-danger" onClick={() => handleDeleteMovie(movie.imdb_id)}>Delete</button>
                  
                </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        <nav>
          <ul className="pagination">
            {Array.from({ length: Math.ceil(movies.length / moviesPerPage) }).map(
              (item, index) => (
                <li key={index} className="page-item">
                  <button
                    className="page-link"
                    onClick={() => paginate(index + 1)}
                  >
                    {index + 1}
                  </button>
                </li>
              )
            )}
          </ul>
        </nav>
      </header>
    </div>
  );
};

export default Home;
