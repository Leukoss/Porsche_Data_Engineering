from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

# On tente d'instancier notre ElasticSearch_api et en cas d'échec, on signale
try:
    # On instancie ElasticSearch_api à l'adresse localhost au port 9200
    es = Elasticsearch(hosts=['http://localhost:9200'])

    # Afin de s'assurer que la connexion est établie on ping notre ElasticSearch_api
    if es.ping():
        print('Connexion établie')
except ConnectionError as error:
    print(f'Erreur - {error}')