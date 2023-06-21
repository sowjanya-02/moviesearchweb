import axios from 'axios';

const addMovieToFavorite = async (id) => {
  try {
    console.log(id)
    const response = await axios.post('http://localhost:8000/user/getuser',{id})
    return response.data.favoritemovies;
  } catch (error) {
    console.error('Error adding movie to favorites:', error);
    throw error;
  }
};

export default addMovieToFavorite;