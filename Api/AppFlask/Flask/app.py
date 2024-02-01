"""
    Module for launching the Flask application
"""
import flask_pymongo
import plotly.graph_objs as go
import plotly
import json

from ..ElasticSearch_api.elasticsearch_functions import *
from flask import Flask, render_template, request
from flask_pymongo import PyMongo


def connect_mongodb(flask_app) -> flask_pymongo.wrappers.Collection:
    """
    Connects to the database from web scraping
    :param flask_app: Flask application
    :return: collection
    """
    try:
        # Configure Flask_Pymongo to connect to localhost:27017 and the
        # 'porsche' database
        flask_app.config['MONGO_URI'] = 'mongodb://localhost:27017/porsche'
        mongo = PyMongo(flask_app)

        # On Retrieve the 'porsche_models' collection
        return mongo.db.porsche_models
    except Exception as error:
        print(f"Exception while connecting to the mongodb... Error : {error}")


def get_mongodb_data(flaskapp) -> list:
    """
    Retrieves the dataset excluding '_id'
    :param flaskapp: Flask application
    :return: list of data
    """
    # Returns all fields of all documents in the collection as a list,
    # excluding the 'field_to_exclude'
    return list(collection.find({}, {'_id': 0}))


def create_es(es_client, porsche_collection):
    """
    Instantiates our Elasticsearch by indexing our collection
    :param es_client: Elasticsearch client
    :param porsche_collection: Collection of Porsche data
    """
    # We retrieve the documents
    documents = get_mongodb_data(porsche_collection)

    # Next, we index our data with the elasticsearch client
    indexation(es_client, documents)


# Instantiate our Flask application
app = Flask(__name__)

# Retrieve the collection
collection = connect_mongodb(app)

# Index our collection
create_es(es_client=es, porsche_collection=collection)


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Defines the home page
    :return: render_template returns the associated HTML page located in the 'templates' folder
    """
    porsche_models_list = []

    filter_params = {
        "min_price": request.args.get('price-min', default='0'),
        "max_price": request.args.get('price-max', default='310000'),
        "min_speed": request.args.get('speed-min', default='0'),
        "max_speed": request.args.get('speed-max', default='350'),
        "min_accel": request.args.get('accel-min', default='0'),
        "max_accel": request.args.get('accel-max', default='10'),
        "min_l_100": request.args.get('l-100-min', default='0'),
        "max_l_100": request.args.get('l-100-max', default='20'),
        "min_power": request.args.get('power-min', default='0'),
        "max_power": request.args.get('power-max', default='800')
    }

    porsche_models_list = search_porsche_model('porsches', **filter_params)

    return render_template('index.html', porsche_models=porsche_models_list)


@app.route('/visualisation')
def visualisation():
    """
    Defines the visualization page (graphs)
    :return: render_template returns the associated HTML page located in the
    'templates' folder
    """
    # Retrieving all elements
    porsche_models_informations = get_mongodb_data(collection)

    # Initializing lists to store information
    data = {
        "acceleration": [], "top_speed": [], "porsche_price": [],
        "porsche_name": [], "l_100_min": [], "l_100_max": [], "power_ch": [],
        "power_kw": []
    }

    # Building lists of information about Porsche models
    for info in porsche_models_informations:
        for key in data.keys():
            data[key].append(info.get(key))

    # Creating graphs
    graphs = {}

    graph_info = [
        ("Prix vs Accélération", "Accélération (0-100 km/h en secondes)",
         "Prix (en EUR)", "acceleration", "porsche_price"),
        ("Prix vs Vitesse", "Vitesse (km/h)", "Prix (en EUR)", "top_speed",
         "porsche_price"),
        ("Prix vs l_100_max", "l_100_max (litres/100 km)", "Prix (en EUR)",
         "l_100_max", "porsche_price"),
        ("Prix vs Puissance", "Puissance (ch)", "Prix (en EUR)", "power_ch",
         "porsche_price"),
        (
            "Puissance vs Vitesse", "Vitesse (km/h)", "Puissance (ch)",
            "top_speed",
            "power_ch"),
        ("Puissance vs Accélération", "Accélération (0-100 km/h en secondes)",
         "Puissance (ch)", "acceleration", "power_ch"),
        ("Puissance vs Litres/100 km", "l_100_max (litres/100 km)",
         "Puissance (ch)", "l_100_max", "power_ch"),
        ("Vitesse vs Accélération", "Accélération (0-100 km/h en secondes)",
         "Vitesse (km/h)", "acceleration", "top_speed")
    ]

    for title, x_title, y_title, x_data, y_data in graph_info:
        fig = go.Figure(data=[
            go.Scatter(
                x=data[x_data],
                y=data[y_data],
                mode='markers',
                marker=dict(color='#1A1A1A')
            )
        ])
        fig.update_layout(
            title=title,
            xaxis_title=x_title,
            yaxis_title=y_title,
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor='#c7c7c7',
            legend=dict(font=dict(color='#1A1A1A'))
        )
        graphs[f"graph_{x_data}_{y_data}"] = json.dumps(fig,
                                                        cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('visualisation.html', graphs=graphs)
