## Initial setup
  1. Need Docker for database

## Tech stack
Frontend- React\
Backend -Django\
Database- Elastic search

## commands to run the app
1. docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.10.1 \
2. For backend:\
     pipenv shell\
     cd backend\
     python3 manage.py runserver
3. Frontend:\
   npm install\
   npm start

## Description
1. Initially database container starts we didnt get data as its not persistent volume
2. Able to add movie from search query to user favorite movies list
3. Movies will add asynchronously to data base and results will appear in Home page
4. Delete Movie from Home page that will automatically update the database movies list
5. We can able to add five movies for users favorite list
