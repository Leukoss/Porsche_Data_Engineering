from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

# On tente d'instancier notre ElasticSearch et en cas d'échec, on signale
try:
    # On instancie ElasticSearch à l'adresse localhost au port 9200
    es = Elasticsearch(hosts=['http://localhost:9200'])

    # Afin de s'assurer que la connexion est établie on ping notre ElasticSearch
    if es.ping():
        print('Connexion établie')
except ConnectionError as error:
    print(f'Erreur - {error}')
