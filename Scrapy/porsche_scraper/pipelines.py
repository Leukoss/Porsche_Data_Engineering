"""
    Module définissant les pipelines pour le scraping

    Auteurs : Lucas SALI--ORLIANGE
    Date : janvier 2024
"""
from typing import Tuple, Any

from scrapy.exceptions import DropItem
import pymongo
import re


def get_power(power_string) -> tuple[int, int]:
    """
    Permet d'obtenir la puissance en kW et en ch
    :param power_string: '200 kW/300 ch'
    :return: (200, 300)
    """
    list_power = power_string.split(sep='/')

    list_to_return = []

    for power in list_power:
        power_value = re.findall(r'\d+', power)
        for number in power_value:
            list_to_return.append(int(number))

    return list_to_return[0], list_to_return[1]


def get_l100(l100_string) -> tuple[float, float]:
    """
    Permet de récupérer les valeurs min et max du l/100
    :param l100_string: '8.5 - 9.3'
    :return: (8.5, 9.3)
    """
    list_l_100 = re.findall(r'\d+,\d+', l100_string)

    list_to_return = []
    list_to_return = [float(value.replace(',', '.')) for value in list_l_100]

    if '-' in l100_string:
        return list_to_return[0], list_to_return[0],

    return list_to_return[0], list_to_return[1]


def get_top_speed(top_speed_string) -> int:
    """
    Permet de récupérer la valeur de la vitesse maximale en int
    :param top_speed_string: '275 km/h'
    :return: 275
    """
    return int(re.findall(r'\d+', top_speed_string)[0])


def get_acceleration(acceleration_string) -> float:
    """
    Permet de récupérer les valeurs min et max du l/100
    :param acceleration_string: '5,1 s'
    :return: 5,1
    """
    return float(re.findall(r'\d+,\d+', acceleration_string)[0].replace(',', '.'))


class TextPipeline(object):
    """
    Permet d'edit les champs des items dans le pipeline
    """
    def process_item(self, item, spider):
        if item['power_ch']:
            item['power_kw'], item['power_ch'] = get_power(item['power_ch'])
        else:
            raise DropItem({item})

        if item['l_100_min']:
            item['l_100_min'], item['l_100_max'] = get_l100(item['l_100_min'])
        else:
            raise DropItem({item})

        if item['porsche_price']:
            item['porsche_price'] = int(item['porsche_price'])
        else:
            raise DropItem({item})

        if item['top_speed']:
            item['top_speed'] = get_top_speed(item['top_speed'])
        else:
            raise DropItem({item})

        if item['acceleration']:
            item['acceleration'] = get_acceleration(item['acceleration'])
        else:
            raise DropItem({item})

        return item


class MongoPipeline(object):
    """
    Permet de traiter les données qui passent dans les pipelines pour les
    transmettre dans la base de données
    """
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
        self.client = pymongo.MongoClient('mongo', 27017)
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
