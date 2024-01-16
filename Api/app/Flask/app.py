"""
    Module permettant le lancement de l'application Flask
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    """
    Permet de définir la page d'accueil
    :return: render_template retourne la page html associée se trouvant dans le
    dossier 'templates'
    """
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
