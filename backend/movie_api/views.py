import requests
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
#from rest_framework.decorators import api_view
from .serializer import MovieSerializer

from elasticsearch import Elasticsearch

# create an instance of Elasticsearch
es = Elasticsearch([{"host":"localhost", "port":9200}])
def create_index(index_name):
   if not es.indices.exists(index=index_name):
    # Create the index
       es.indices.create(index=index_name)
   
def search_movies(query):
  # search movies using the Elasticsearch `search` method
  # and return the search results
  res = es.search(index="movies", body=query)
  movies_list = [i.get('_source') for i in res.get('hits').get('hits')]
  return movies_list

def search_movies_omdp(query):
  # search movies using the Elasticsearch `search` method
  # and return the search results
    res = requests.get(
    "http://www.omdbapi.com/",
    params={
      "apikey": "f4209151",
      "s": query,
      "type":"movie"
    }
    )
    result = res.json()
    return result


def filter_movies(title=None, actors=None,director=None, year=None):
  # create a bool query to filter the movies
  bool_query = {
    "bool": {
      "must": []
    }
  }
  # add filters to the bool query based on the provided parameters
  if title:
    bool_query["bool"]["must"].append({"match": {"title": title}})
  elif actors:
    bool_query["bool"]["must"].append({"match": {"actors": actors}})
  elif director:
    bool_query["bool"]["must"].append({"match": {"director": director}})
  elif year:
    bool_query["bool"]["must"].append({"match": {"year": year}})
  else:
    bool_query["bool"]["must"].append({
        "match_all" : {}
    })
  #create the Elasticsearch query
  query = {
    "query": bool_query
  }
  # search and return the movies
  return search_movies(query)

# Create your views here.
class Searchomdb(APIView):
      def post(self,request):
        #print(request.data)
        title = request.data.get("title")
        movies = search_movies_omdp(title)
        for row in movies.get("Search"):
            movie = {
                "title": row["Title"],
                "imdb_id": row["imdbID"],
                "genre": row["Type"],
                "year": row["Year"],
                "poster":row["Poster"],
                
            }
            movie_data = MovieSerializer(data = movie)
            movie_data.is_valid(raise_exception=True)
            validated_movie = movie_data.validated_data
            try:
               create_index('movies')
               es.index(index="movies", body=validated_movie,id=validated_movie['imdb_id'])
            except Exception as er:
                return Response({'message':er.error})
        #serializer_m = MovieSerializer(movies,many=True)
        return Response(movies.get('Search'), status=status.HTTP_200_OK)
      
class DeletMovie(APIView):
      def post(self,request):
        print(request.data)
        imdb_id = request.data.get("imdb_id")
        query = {
         "query": {
          "match": {
            "imdb_id": imdb_id
             }
             }
            }
        try:
            movie_rem = es.delete_by_query(index="movies", body=query)
            return Response({'message':'Movie deleted from database'}, status=status.HTTP_200_OK)
        except:
           return Response({'message':'Movie not exists in db'},status=status.HTTP_204_NO_CONTENT)

class Getlistview(APIView):
        def get(self,request):
          query = {
            "query": {
             "match_all": {}
                }
               }
          try:
            create_index('movies')
            response = es.search(index="movies", body=query, size=10000)
            documents = [hit['_source'] for hit in response['hits']['hits']]
            serializer_m = MovieSerializer(documents,many=True)
            return Response(serializer_m.data, status=status.HTTP_200_OK)
          except Exception as er:
            return Response({'message':er.args},status = status.HTTP_400_BAD_REQUEST)

    
   