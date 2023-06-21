##Initial setup
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
