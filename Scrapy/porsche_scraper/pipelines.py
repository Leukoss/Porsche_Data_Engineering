"""
    Module définissant les pipelines pour le scraping

    Auteurs : Lucas SALI--ORLIANGE
    Date : janvier 2024
"""
import pymongo


class MongoPipeline(object):
    # Définit le nom de la table 'porsche_models'
    collection_name = "porsche_models"

    def __init__(self):
        """
        Permet d'instancier le client mongo ainsi que la future base de données
        """
        self.client = None
        self.db = None

    def open_spider(self, spider) -> None:
        """
        Fonction appelée à l'ouverture du spider
        :param spider: de notre scraper porsche_france
        """
        # Instanciation de MongoClient sur le port 27017 à l'adresse 'mongo'
        self.client = pymongo.MongoClient()
        # Sélectionne la Base de Données 'porsche'
        self.db = self.client['porsche']

    def close_spider(self, spider) -> None:
        """
        Fonction appelée à la fermeture du spider
        :param spider: de notre scraper porsche_france
        """
        # Fermeture du mongo
        self.client.close()

    def process_item(self, item, spider) -> object:
        """
        Méthode appelée à chaque fois qu'un item passe dans le mécanisme interne
        de scrapy
        :param item: objet contenant plusieurs scrapy.Field()
        :param spider: de notre scraper porsche_france
        :return: item
        """
        # Ajoute dans la collection les données
        self.db[self.collection_name].insert_one((dict(item)))
        return item
