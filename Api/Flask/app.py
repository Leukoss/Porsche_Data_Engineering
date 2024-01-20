"""
    Module permettant le lancement de l'application Flask
"""
import plotly
from plotly.offline import plot
import plotly.graph_objs as go
import json
from flask import Flask, render_template, request
from flask_pymongo import PyMongo

# On importe toutes les fonctions de recherches notamment pour les filtres
from Api.ElasticSearch_api.elasticsearch_functions import (indexation,
                                                           clear_es_client,
                                                           search_porsche_model,
                                                           es)


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


def create_es(es_client, collection):
    """
    On instancie notre elasticsearch en indexant notre collection
    :param es_client: client elasticsearch
    :param collection: collection de documents
    """
    # Dans un premier temps, on réinitialise le précédent elasticsearch
    clear_es_client(es_client)

    # On récupère les documents
    documents = get_mongodb_data(collection)

    # Dans un second temps, on indexe nos données
    indexation(es_client, documents)


# On instancie notre application Flask
app = Flask(__name__)
# On récupère la collection
collection = log_mongodb(app)
# On indexe notre collection
create_es(es_client=es, collection=collection)


@app.route('/', methods=['GET'])
def home():
    """
    Permet de définir la page d'accueil
    :return: render_template retourne la page html associée se trouvant dans le
    dossier 'templates'
    """
    # Récupération des paramètres pour le filtrage
    initial_min_price = request.args.get('initial-price-min')
    initial_max_price = request.args.get('initial-price-max')

    print('min', initial_min_price)

    dict_params = {

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
    acceleration = []
    top_speed = []
    porsche_price = []
    porsche_name = []
    l_100_min = []
    l_100_max = []
    power_ch = []
    power_kw = []

    # Dictionnaire des figures
    figs = {}

    # On constitue les listes d'informations sur les modèles de Porsche
    for info in porsche_models_informations:
        acceleration.append(info.get('acceleration'))
        top_speed.append(info.get('top_speed'))
        porsche_price.append(info.get('porsche_price'))
        porsche_name.append(info.get('porsche_name'))
        l_100_min.append(info.get('l_100_min'))
        l_100_max.append(info.get('l_100_max'))
        power_ch.append(info.get('power_ch'))
        power_kw.append(info.get('power_kw'))

    # Prix vs Accélération
    fig_price_acc = go.Figure(data=[
        go.Scatter(
            x=acceleration,
            y=porsche_price,
            mode='markers',
            marker=dict(color='#f9f9f9')
        )
    ])
    fig_price_acc.update_layout(
        title='Prix vs Accélération',
        xaxis_title='Accélération (0-100 km/h en secondes)',
        yaxis_title='Prix (en EUR)',
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='#1A1A1A',
        legend=dict(font_color='#1A1A1A')
    )
    graph_price_acc = json.dumps(fig_price_acc, cls=plotly.utils.PlotlyJSONEncoder)

    # Prix vs Vitesse
    fig_price_speed = go.Figure(data=[
        go.Scatter(
            x=top_speed,
            y=porsche_price,
            mode='markers',
            marker=dict(color='#f9f9f9')
        )
    ])
    fig_price_speed.update_layout(
        title='Prix vs Vitesse',
        xaxis_title='Vitesse (km/h)',
        yaxis_title='Prix (en EUR)',
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='#1A1A1A',
        legend=dict(font_color='#1A1A1A')
    )
    graph_price_speed = json.dumps(fig_price_speed, cls=plotly.utils.PlotlyJSONEncoder)

    # Prix vs l_100_max
    fig_price_100 = go.Figure(data=[
        go.Scatter(
            x=acceleration,
            y=l_100_max,
            mode='markers',
            marker=dict(color='#f9f9f9')
        )
    ])
    fig_price_100.update_layout(
        title='Prix vs l_100_max',
        xaxis_title='l_100_max (litres/100 km)',
        yaxis_title='Prix (en EUR)',
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='#1A1A1A',
        legend=dict(font_color='#1A1A1A')
    )
    graph_price_100 = json.dumps(fig_price_100, cls=plotly.utils.PlotlyJSONEncoder)

    # Prix vs Puissance
    fig_price_power = go.Figure(data=[
        go.Scatter(
            x=power_ch,
            y=porsche_price,
            mode='markers',
            marker=dict(color='#f9f9f9')
        )
    ])
    fig_price_power.update_layout(
        title='Prix vs Puissance',
        xaxis_title='Puissance (ch)',
        yaxis_title='Prix (en EUR)',
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='#1A1A1A',
        legend=dict(font_color='#1A1A1A')
    )
    graph_price_power = json.dumps(fig_price_power, cls=plotly.utils.PlotlyJSONEncoder)

    # Puissance vs Vitesse
    fig_power_speed = go.Figure(data=[
        go.Scatter(
            x=top_speed,
            y=power_ch,
            mode='markers',
            marker=dict(color='#f9f9f9')
        )
    ])
    fig_power_speed.update_layout(
        title='Puissance vs Vitesse',
        xaxis_title='Vitesse (km/h)',
        yaxis_title='Puissance (ch)',
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='#1A1A1A',
        legend=dict(font_color='#1A1A1A')
    )
    graph_power_speed = json.dumps(fig_power_speed, cls=plotly.utils.PlotlyJSONEncoder)

    # Puissance vs Acceleration
    fig_power_acc = go.Figure(data=[
        go.Scatter(
            x=acceleration,
            y=power_ch,
            mode='markers',
            marker=dict(color='#f9f9f9')
        )
    ])
    fig_power_acc.update_layout(
        title='Puissance vs Accélération',
        xaxis_title='Accélération (0-100 km/h en secondes)',
        yaxis_title='Puissance (ch)',
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='#1A1A1A',
        legend=dict(font_color='#1A1A1A')
    )
    graph_power_acc = json.dumps(fig_power_acc, cls=plotly.utils.PlotlyJSONEncoder)

    # Puissance vs Litre/100
    fig_power_100 = go.Figure(data=[
        go.Scatter(
            x=l_100_max,
            y=power_ch,
            mode='markers',
            marker=dict(color='#f9f9f9')
        )
    ])
    fig_power_100.update_layout(
        title='Puissance vs Litres/100 km',
        xaxis_title='l_100_max (litres/100 km)',
        yaxis_title='Puissance (ch)',
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='#1A1A1A',
        legend=dict(font_color='#1A1A1A')
    )
    graph_power_100 = json.dumps(fig_power_100, cls=plotly.utils.PlotlyJSONEncoder)

    # Vitesse vs Acceleration
    fig_speed_acc = go.Figure(data=[
        go.Scatter(
            x=acceleration,
            y=top_speed,
            mode='markers',
            marker=dict(color='#f9f9f9')
        )
    ])
    fig_speed_acc.update_layout(
        title='Vitesse vs Accélération',
        xaxis_title='Accélération (0-100 km/h en secondes)',
        yaxis_title='Vitesse (km/h)',
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='#1A1A1A',
        legend=dict(font_color='#1A1A1A')
    )
    graph_speed_acc = json.dumps(fig_speed_acc, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('visualisation.html',
                           graph_power_acc=graph_power_acc,
                           graph_power_speed=graph_power_speed,
                           graph_speed_acc=graph_speed_acc,
                           graph_power_100=graph_power_100,
                           graph_price_power=graph_price_power,
                           graph_price_100=graph_price_100,
                           graph_price_speed=graph_price_speed,
                           graph_price_acc=graph_price_acc)


if __name__ == '__main__':
    app.run()
