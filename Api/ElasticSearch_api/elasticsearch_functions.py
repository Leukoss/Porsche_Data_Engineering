# elasticsearch_functions.py

from .elasticsearch_app import es
from elasticsearch.helpers import bulk


def generate_data(documents):
    """
    Permet de générer les données pour l'indexation
    :param documents: issus du mongodb
    """
    for document in documents:
        yield {
            "_index": "porsches",
            "_source": {k: v if v else None for k, v in document.items()},
        }


def search_porsche_model(index_name, min_price, max_price, min_speed, max_speed,
                         min_accel, max_accel, min_l_100, max_l_100, min_power,
                         max_power) -> list:
    """
    Permet de sélectionner les documents en fonction des paramètres
    :param index_name: nom de l'index
    :param min_price: Prix minimum
    :param max_price: Prix maximum
    :param min_speed: Vitesse minimum
    :param max_speed: Vitesse maximum
    :param min_accel: Accélération minimum
    :param max_accel: Accélération maximum
    :param min_l_100: Consommation minimum (litres/100km)
    :param max_l_100: Consommation maximum (litres/100km)
    :param min_power: Puissance minimum (ch)
    :param max_power: Puissance maximum (ch)
    :return: une liste de documents filtrés
    """
    filtered_documents = []

    range_filters = [
        {"range": {"porsche_price": {"gte": min_price, "lte": max_price}}},
        {"range": {"acceleration": {"gte": min_accel, "lte": max_accel}}},
        {"range": {"top_speed": {"gte": min_speed, "lte": max_speed}}},
        {"range": {"power_ch": {"gte": min_power, "lte": max_power}}},
        {"range": {"l_100_max": {"lte": max_l_100}}},
        {"range": {"l_100_min": {"gte": min_l_100}}},
    ]

    query = {
        "query": {
            "bool": {
                "must": range_filters
            }
        }
    }

    response = es.search(index=index_name, body=query)

    for hit in response['hits']['hits']:
        filtered_documents.append(hit['_source'])

    return filtered_documents


def clear_es_client(es_client=es, index="porsches"):
    """
    Permet de clear le client elasticsearch pour de nouvelles recherches
    :param es_client: client elasticSearch
    :param index: index à clear
    """
    body_query = {
        "query": {
            "match_all": {}
        }
    }

    response = es_client.delete_by_query(index=index, body=body_query)
    es_client.indices.refresh(index=index)
    print(response)


def indexation(es_client, documents):
    """
    Permet de créer un index ElasticSearch_api
    :param es_client: client ElasticSearch_api
    :param documents: à indexer
    """
    index_name = 'porsches'

    try:
        # Si l'index existe déjà
        if not es_client.indices.exists(index=index_name):
            es_client.indices.create(index=index_name)

        # Réalise l'indexation
        response = bulk(es_client, generate_data(documents))

        # S'assure que les index sont à jour
        es_client.indices.refresh(index=index_name)
    except Exception as error:
        print(error)
