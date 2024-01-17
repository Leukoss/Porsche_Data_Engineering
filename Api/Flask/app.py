"""
    Module permettant le lancement de l'application Flask
"""
from flask import Flask, render_template
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
    porsche_models_informations = collection.find()

    porsche_dict = {

    }

    return render_template('index.html')


@app.route('/search_model')
def search():
    """
    Permet de définir la page de recherche
    :return: render_template retourne la page html associée se trouvant dans le
    dossier 'templates'
    """
    return render_template('search_model.html')


@app.route('/comparaison')
def comparaison():
    """
    Permet de définir la page de comparaison
    :return: render_template retourne la page html associée se trouvant dans le
    dossier 'templates'
    """
    return render_template('comparaison.html')


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
