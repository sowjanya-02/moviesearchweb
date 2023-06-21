#!/bin/bash
#start database container
docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.10.1

##
pipenv shell
cd backend/
python3 manage.py runserver
