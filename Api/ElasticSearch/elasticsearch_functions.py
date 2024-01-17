from .elasticsearch_app import es
from elasticsearch.helpers import bulk


def search_porsche_model(index_name, l_100_min, l_100_max, power_ch_min,
                         power_ch_max, top_speed_min, top_speed_max,
                         acceleration_min, acceleration_max, porsche_price_min,
                         porsche_price_max):

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
        body=query,
        size=10)

    hits = results.get('hits', {}).get('hits', [])

    print(hits)

    return None