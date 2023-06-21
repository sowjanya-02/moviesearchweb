import React, { useState } from "react";
import axios from "axios";
import AddMovie from "./components/AddMovie";
import { useSelector } from "react-redux";

const MovieSearch = () => {
  const [title, setTitle] = useState("");
  const [movies, setMovies] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [moviesPerPage] = useState(3 * 5);
  const { user: currentUser } = useSelector((state) => state.auth);
  
  const searchMovies = async () => {
    try {
      const response = await axios.post("http://localhost:8000/movies/search", { title });
      setMovies(response.data);
      console.log(response)
    } catch (error) {
      console.error(error);
    }
  };

  const handleSearch = (event) => {
    event.preventDefault();
    searchMovies();
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
    <div>
      <form onSubmit={handleSearch}>
        <label>
          title:
          <input type="text" value={title} onChange={(event) => setTitle(event.target.value)} />
        </label>
        <br />
        <button type="submit">Search</button>
      </form>
      <div className="row">
          {currentMovies.map((movie) => (
            <div className="col-lg-4" key={movie.imdbID}>
              <div className="card mb-4">
                <img
                  className="card-img-top"
                  src={movie.Poster}
                  alt={movie.Title}
                />
                <div className="card-body">
                  <h5 className="card-title">{movie.Title}</h5>
                  <p className="card-text">Year: {movie.Year}</p>
                  <p className="card-text">Genre: {movie.Type}</p>
                  <p className="card-text">IMDB ID: {movie.imdbID}</p>
                  <div className="d-flex justify-content-between">
                  
                  <button className="btn btn-primary" onClick={() => AddMovie(movie.imdbID,currentUser.id)}>Add</button>
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
    </div>
  );
};

export default MovieSearch;
