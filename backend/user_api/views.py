from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from .es_connect import es


class UserCreate(APIView):
    """ 
    Creates the user. 
    """
    def post(self, request, format='json'):
        User.objects.filter(username__contains='test').delete()
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                validated_user = serializer.validated_data
                if validated_user:
                      json = serializer.data
                      json['token'] = token.key
                try:
                     json['favoritemovies'] = []
                     es.index(index="users", body=json)
                except Exception as err:
                    return Response({'message':err.error})
                return Response(json, status=status.HTTP_201_CREATED)

        return Response({"message":"email exists"}, status=status.HTTP_400_BAD_REQUEST)
    

class UserLogin(APIView):
    """
    Authenticates and logs in the user.
    """

    def post(self, request, format='json'):
        #print (request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        search_user = { "query": {
          "term": {
            "email.keyword": email
           }
          }
         }
        try:
          user = es.search(index='users',body=search_user)
        except:
            return Response({'message':'user not found signup'}, status=status.HTTP_404_NOT_FOUND)
        
        
        if user['hits']['total']['value'] > 0:
            res = user['hits']['hits'][0]['_source']
            result = {'username':res.get('username'),'email':res.get('email')}
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogout(APIView):
    """
    Logs out the authenticated user.
    """

    def post(self, request, format='json'):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

class GetUser(APIView):
    """
    get user info
    """
    
    def post(self, request, format='json'):
        print(request.data)
        email = request.data.get('id')
        password = request.data.get('password')
        search_user = { "query": {
          "term": {
            "id": email
           }
          }
         }
        user = es.search(index='users',body=search_user)
        if user:
            res = user.get('hits').get('hits')[0].get('_source')
            print (res)
            result = {'id':res.get('id'),'username':res.get('username'),'email':res.get('email'),
                      'favoritemovies':res.get('favoritemovies')}
            return Response(result, status=status.HTTP_200_OK)
        return Response({'messsage':'user not found'}, status=status.HTTP_200_OK)

class Addmovie(APIView):
     def post(self, request, format='json'):
        imdbid = request.data.get('imdb_id')
        user_id = request.data.get('id')
        print (request.data)
        add_movie = { "query": {
          "term": {
            "imdb_id.keyword": imdbid
           }
          }
         }
        user_search = { "query": {
          "term": {
            "id": user_id
           }
          }
         }
        movie_data = es.search(index='movies',body=add_movie)
        if movie_data:
            favoritemovie = movie_data.get('hits').get('hits')[0].get('_source')
        update_request = {
            'script': {
                'source': '''
                  def containsMovie = ctx._source.favoritemovies.stream().anyMatch(movie -> movie['imdb_id'] == params.imdb_id);
                  if (!containsMovie) {
                  ctx._source.favoritemovies.add(params.new_value)}
                ''',
                'lang': 'painless',
                'params': {
                    'imdb_id':imdbid,
                    'new_value': favoritemovie
                }
            }
        }
        
        user_data = es.search(index='users',body=user_search)
        
        if user_data['hits']['total']['value'] > 0:
            user_docid = user_data['hits'].get('hits')[0].get('_id')
            user_movies  = user_data['hits'].get('hits')[0].get('_source').get('favoritemovies')
            try:
              if len(user_movies)<6:
                res =  es.update(index='users',id=user_docid,body=update_request)
                return Response({'message':'successfully added movie'},status=status.HTTP_200_OK)
              else:
                  return Response({'message':'5 movies reached remove one to add another'},status=status.HTTP_200_OK)
            except Exception as err:
                return Response({'message':err.args[0]},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message':'user data not exists'},status=status.HTTP_404_NOT_FOUND)

class Deletemovie(APIView):
     def get(self, request, format='json'):
        imdbid = request.data.get('imdb_id')
        user_id = request.data.get('id')
        user_search = { "query": {
          "term": {
            "id": user_id
           }
          }
         }
        user_data = es.search(index='users',body=user_search)
        user = user_data['hits'].get('hits')[0]
        favorite_movies = user.get('_source').get('favoritemovies')
        if len(favorite_movies)>0: 
            fv_movies = [k for k in favorite_movies if k.get('imdb_id') != imdbid]
        
        update_request = {
            'doc':{
                'favoritemovies':fv_movies
            }
        }
        if user_data['hits']['total']['value'] > 0:
            try:
               es.update(index='users',id=user.get('_id'),body=update_request)
               return Response({'successfully deleted movie'},status=status.HTTP_200_OK)
            except Exception as err:
                return Response({'message':err.args[0]},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message':'user data not exists'},status=status.HTTP_404_NOT_FOUND)
