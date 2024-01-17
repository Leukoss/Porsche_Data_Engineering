"""
    Module permettant le lancement de l'application Flask
"""
from flask import Flask, render_template
from flask_pymongo import PyMongo

# On importe toutes les fonctions de recherches notamment pour les filtres
from ..ElasticSearch.elasticsearch_functions import *


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


# def create_es(es_client, collection):
#     """
#     On instancie notre elasticsearch en indexant notre collection
#     :param es_client: client elasticsearch
#     :param collection: collection de documents
#     """
#     # Dans un premier temps, on réinitialise le précédent elasticsearch
#     clear_es_client(es_client)
#
#     # Dans un second temps, on indexe nos données
#     create_index(es_client, )


# On instancie notre application Flask
app = Flask(__name__)

# On récupère la collection
collection = log_mongodb(app)


@app.route('/')
def home():
    """
    Permet de définir la page d'accueil
    :return: render_template retourne la page html associée se trouvant dans le
    dossier 'templates'
    """
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


@app.route('/comparaison')
def comparaison():
    """
    Permet de définir la page de comparaison (besoin de GET/POST, car
    l'utilisateur sélectionne des données et nous en envoyons
    :return: render_template retourne la page html associée se trouvant dans le
    dossier 'templates'
    """
    # Dans un premier temps, on définit un dictionnaire qui contiendra tous les
    # paramètres dont nous aurons besoin dans 'search_porsche_model'

    return render_template('comparaison.html')


@app.route('/search_model')
def search():
    """
    Permet de définir la page de recherche
    :return: render_template retourne la page html associée se trouvant dans le
    dossier 'templates'
    """
    return render_template('search_model.html')


@app.route('/visualisation')
def visualisation():
    """
    Permet de définir la page de visualisation (graphique)
    :return: render_template retourne la page html associée se trouvant dans le
    dossier 'templates'
    """
    return render_template('visualisation.html')


if __name__ == '__main__':
    app.run()
