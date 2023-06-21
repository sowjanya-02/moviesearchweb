from elasticsearch import Elasticsearch

# create an instance of Elasticsearch
es = Elasticsearch([{"host":"localhost", "port":9200}])