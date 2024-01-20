"""
    Module permettant le lancement de l'application Flask
"""
import plotly.graph_objs as go
import plotly
import json

from Api.ElasticSearch_api.elasticsearch_functions import *
from flask import Flask, render_template, request
from flask_pymongo import PyMongo


def log_mongodb(flask_app):
    """
    Permet de se connecter à la base de données issue du scraping
    :param flask_app: application flask
    :return: collection
    """
    try:
        # Configuration du Flask_Pymongo pour se connecter au localhost27017 et
        # à la base de données 'porsche'
        flask_app.config['MONGO_URI'] = 'mongodb://localhost:27017/porsche'
        mongo = PyMongo(flask_app)

        # On récupère la collection 'porsche_models'
        return mongo.db.porsche_models
    except Exception as error:
        print(f"Exception while connecting to the mongodb... Error : {error}")


def get_mongodb_data(flaskapp) -> list:
    """
    Permet de récupérer le jeu de données en excluant '_id'
    :param flaskapp: application
    :return: liste de données
    """
    field_to_exclude = {'_id': 0}

    # Sous forme de liste, retourne tous les fields de tous les documents de la
    # collection excepté le 'field_to_exclude'
    return list(collection.find({}, field_to_exclude))


def create_es(es_client, porsche_collection):
    """
    On instancie notre elasticsearch en indexant notre collection
    :param es_client: client elasticsearch
    :param porsche_collection: parlant
    """
    # Dans un premier temps, on réinitialise le précédent elasticsearch
    clear_es_client(es_client)

    # On récupère les documents
    documents = get_mongodb_data(porsche_collection)

    # Dans un second temps, on indexe nos données
    indexation(es_client, documents)


# On instancie notre application Flask
# On récupère la collection
# On indexe notre collection
app = Flask(__name__)
collection = log_mongodb(app)
create_es(es_client=es, porsche_collection=collection)


@app.route('/', methods=['GET'])
def home():
    """
    Permet de définir la page d'accueil
    :return: render_template retourne la page html associée se trouvant dans le
    dossier 'templates'
    """
    # Récupération des paramètres pour le filtrage
    min_price = request.args.get('price-min', type=str)
    max_price = request.args.get('price-max', type=str)
    min_speed = request.args.get('speed-min', type=str)
    max_speed = request.args.get('speed-max', type=str)
    min_accel = request.args.get('accel-min', type=str)
    max_accel = request.args.get('accel-max', type=str)
    min_l_100 = request.args.get('l-100-min', type=str)
    max_l_100 = request.args.get('l-100-max', type=str)
    min_power = request.args.get('power-min', type=str)
    max_power = request.args.get('power-max', type=str)

    print('min-price:', min_price)
    print('max-price:', max_price)
    print('min-speed:', min_speed)
    print('max-speed:', max_speed)
    print('min-accel:', min_accel)
    print('max-accel:', max_accel)
    print('min-l-100:', min_l_100)
    print('max-l-100:', max_l_100)
    print('min-power:', min_power)
    print('max-power:', max_power)

    dict_params = {
        'min-price': min_price,
        'max-price': max_price,
        'min-speed': min_speed,
        'max-speed': max_speed,
        'min-accel': min_accel,
        'max-accel': max_accel,
        'min-l-100': min_l_100,
        'max-l-100': max_l_100,
        'min-power': min_power,
        'max-power': max_power
    }

    # hits = search_porsche_model(index_name='porsches', **dict_params)

    render_params = {

    }

    # Récupération de tous les éléments
    porsche_models_informations = get_mongodb_data(collection)

    # On définit une liste que l'on passera plus tard en paramètre pour render
    porsche_models_list = []

    # Pour chaque élément de la base de données, on récupère des informations
    # précises
    for model in porsche_models_informations:
        model_data = {
            'porsche_price': model.get('porsche_price'),
            'porsche_name': model.get('porsche_name'),
            'image_url': model.get('image_url')
        }
        porsche_models_list.append(model_data)

    return render_template('index.html', porsche_models=porsche_models_list)


@app.route('/visualisation')
def visualisation():
    """
    Permet de définir la page de visualisation (graphique)
    :return: render_template retourne la page html associée se trouvant dans le
    dossier 'templates'
    """
    # Récupération de tous les éléments
    porsche_models_informations = get_mongodb_data(collection)

    # Initialise les listes pour stocker les informations
    data = {
        "acceleration": [],
        "top_speed": [],
        "porsche_price": [],
        "porsche_name": [],
        "l_100_min": [],
        "l_100_max": [],
        "power_ch": [],
        "power_kw": []
    }

    # On constitue les listes d'informations sur les modèles de Porsche
    for info in porsche_models_informations:
        for key in data.keys():
            data[key].append(info.get(key))

    # Création des graphiques
    graphs = {}

    graph_info = [
        ("Prix vs Accélération", "Accélération (0-100 km/h en secondes)", "Prix (en EUR)", "acceleration", "porsche_price"),
        ("Prix vs Vitesse", "Vitesse (km/h)", "Prix (en EUR)", "top_speed", "porsche_price"),
        ("Prix vs l_100_max", "l_100_max (litres/100 km)", "Prix (en EUR)", "l_100_max", "porsche_price"),
        ("Prix vs Puissance", "Puissance (ch)", "Prix (en EUR)", "power_ch", "porsche_price"),
        ("Puissance vs Vitesse", "Vitesse (km/h)", "Puissance (ch)", "top_speed", "power_ch"),
        ("Puissance vs Accélération", "Accélération (0-100 km/h en secondes)", "Puissance (ch)", "acceleration", "power_ch"),
        ("Puissance vs Litres/100 km", "l_100_max (litres/100 km)", "Puissance (ch)", "l_100_max", "power_ch"),
        ("Vitesse vs Accélération", "Accélération (0-100 km/h en secondes)", "Vitesse (km/h)", "acceleration", "top_speed")
    ]

    for title, x_title, y_title, x_data, y_data in graph_info:
        fig = go.Figure(data=[
            go.Scatter(
                x=data[x_data],
                y=data[y_data],
                mode='markers',
                marker=dict(color='#f9f9f9')
            )
        ])
        fig.update_layout(
            title=title,
            xaxis_title=x_title,
            yaxis_title=y_title,
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor='#1A1A1A',
            legend=dict(font_color='#1A1A1A')
        )
        graphs[f"graph_{x_data}_{y_data}"] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('visualisation.html', graphs=graphs)


if __name__ == '__main__':
    app.run()
