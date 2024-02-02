from .elasticsearch_app import es
from elasticsearch.helpers import bulk


def generate_data(documents):
    """
    Generate data for indexing
    :param documents: Data from MongoDB
    """
    for document in documents:
        yield {
            "_index": "porsches",
            "_source": {k: v if v else None for k, v in document.items()},
        }


def clear_es_client(es_client=es, index="porsches"):
    """
    Clear the Elasticsearch client for new searches
    :param es_client: Elasticsearch client
    :param index: Index to clear
    """
    response = es_client.delete_by_query(
        index=index,
        body={"query": {"match_all": {}}}
    )

    es_client.indices.refresh(index=index)


def indexation(es_client, documents):
    """
    Create an Elasticsearch index
    :param es_client: Elasticsearch client
    :param documents: Documents to index
    """
    index_name = 'porsches'

    try:
        if not es_client.indices.exists(index=index_name):
            # Create the indices if it does not exist
            es_client.indices.create(index=index_name)

        # Allows the indexing for all documents in a single action and refresh
        response = bulk(es_client, generate_data(documents))
        es_client.indices.refresh(index=index_name)
    except Exception as error:
        print(f"Exception - {error}")


def search_porsche_model(index_name, min_price, max_price, min_speed, max_speed,
                         min_accel, max_accel, min_l_100, max_l_100, min_power,
                         max_power) -> list:
    """
    Select documents based on parameters
    :param index_name: Index name
    :param min_price: Minimum price
    :param max_price: Maximum price
    :param min_speed: Minimum speed
    :param max_speed: Maximum speed
    :param min_accel: Minimum acceleration
    :param max_accel: Maximum acceleration
    :param min_l_100: Minimum consumption (liters/100km)
    :param max_l_100: Maximum consumption (liters/100km)
    :param min_power: Minimum power (hp)
    :param max_power: Maximum power (hp)
    :return: A list of filtered documents
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

    query = {"query": {"bool": {"must": range_filters}}, "size": 100}

    try:
        response = es.search(index=index_name, body=query)

        # Retrieve only the data we need
        filtered_documents = [hit['_source'] for hit in
                              response.get('hits', {}).get('hits', [])]
    except Exception as error:
        print(f"Error - {error}")

    return filtered_documents
