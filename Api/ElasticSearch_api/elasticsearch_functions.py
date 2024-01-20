from .elasticsearch_app import es
from elasticsearch.helpers import bulk


def generate_data(documents):
    """
    Permet de générer les données pour l'indexation
    :param documents: issus du mongodb
    """
    for document in documents:
        yield {
            # Définit le nom de l'index
            "_index": "porsches",
            # Définit le type de document
            "_types": "porsche",
            # Définit le document avec les données qui sera indexé
            "_source": {k: v if v else None for k, v in document.items()},
        }


def search_porsche_model(index_name, l_100_min, l_100_max, power_ch_min,
                         power_ch_max, top_speed_min, top_speed_max,
                         acceleration_min, acceleration_max, porsche_price_min,
                         porsche_price_max) -> dict:
    """
    Permet de sélectionner les documents en fonction des paramètres
    :param index_name: nom de l'index
    :param l_100_min: parlant
    :param l_100_max: parlant
    :param power_ch_min: parlant
    :param power_ch_max: parlant
    :param top_speed_min: parlant
    :param top_speed_max: parlant
    :param acceleration_min: parlant
    :param acceleration_max: parlant
    :param porsche_price_min: parlant
    :param porsche_price_max: parlant
    :return: un dictionnaire avec le contenu des données filtrées
    """
    # Définit selon les paramètres d'entrée la range pour chaque filtre
    range_filter = [
        {"range": {"l_100": {"gte": l_100_min,
                             "lte": l_100_max}}},
        {"range": {"power_ch": {"gte": power_ch_min,
                                "lte": power_ch_max}}},
        {"range": {"top_speed": {"gte": top_speed_min,
                                 "lte": top_speed_max}}},
        {"range": {"acceleration": {"gte": acceleration_min,
                                    "lte": acceleration_max}}},
        {"range": {"porsche_price": {"gte": porsche_price_min,
                                     "lte": porsche_price_max}}}
    ]

    # Définit ici la requête conformément aux ranges des filtres
    query = {
        "query": {
            "bool": {
                "must": range_filter
            }
        }
    }

    # Permet d'effectuer la recherche elasticsearch
    results = es.search(
        index=index_name,
        body=query
    )

    hits = results.get('hits', {}).get('hits', [])

    return hits


def clear_es_client(es_client=es, index="porsches"):
    """
    Permet de clear le client elasticsearch pour de nouvelles recherches
    :param es_client: client elasticSearch
    :param index: index à clear
    """
    # Check if the index exists before attempting to delete documents
    if es_client.indices.exists(index=index):
        body_query = {
            "query": {
                "match_all": {}
            }
        }

        # delete_by_query afin de supprimer tous les éléments
        response = es_client.delete_by_query(
            index=index,
            body=body_query
        )

        # Rafraîchissement de l'index pour s'assurer que les modifications
        # soient faites
        es_client.indices.refresh(index=index)
    else:
        print(f"The index '{index}' does not exist.")


def indexation(es_client, documents):
    """
    Permet de créer un index ElasticSearch_api
    :param es_client: client ElasticSearch_api
    :param documents: à indexer
    """
    index_name = 'porsches'

    try:
        # Si l'index existe déjà
        if not es.indices.exists(index=index_name):
            es_client.indices.create(index=index_name)

        # Réalise l'indexation
        response = bulk(es_client, generate_data(documents))

        # S'assure que les index sont à jour
        es_client.indices.refresh(index=index_name)
    except Exception as error:
        print(error)
