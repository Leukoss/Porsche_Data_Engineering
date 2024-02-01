from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

# We attempt to instantiate our Elasticsearch API, and in case of failure,
# we report it
try:
    # We instantiate the Elasticsearch API at the address localhost on port 9200
    es = Elasticsearch(hosts=["http://elasticsearch:9200"])

    # To ensure that the connection is established, we ping our Elasticsearch
    # API
    if es.ping():
        print('Connection established')
except ConnectionError as error:
    print(f'Error - {error}')

