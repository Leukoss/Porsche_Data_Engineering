"""
    Module permettant le lancement de l'application Flask
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    """
    Permet de définir la page d'accueil
    :return: render_template retourne la page html associée se trouvant dans le
    dossier 'templates'
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
