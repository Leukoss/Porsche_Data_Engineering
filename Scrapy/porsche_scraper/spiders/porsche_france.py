"""
    Module permettant le scraping du site de Porsche et la mise en relation avec
    la base de données mongo afin de stocker les données scrapées

    Auteurs : Lucas SALI--ORLIANGE
    Date : janvier 2024
"""
import scrapy
import re

from ..items import PorscheScraperItem


class PorscheFranceSpider(scrapy.Spider):
    """
        Class Docstring :
        Spider permettant le scrapping du site de Porsche afin de récupérer
        diverses informations concernant les modèles de Porsche disponibles.

        Attributes :
            name (str) : nom du spider.
            allowed_domains (list) : liste des noms de domaine à crawl.
            start_url (list) : liste des URLs de départ pour le spider.
    """
    name = "porsche_france"
    allowed_domains = ["www.porsche.com"]
    start_urls = ["https://www.porsche.com/france/models/"]

    def parse(self, response) -> None:
        """
        Permet de réaliser le parsing depuis la première page web
        :param response: lien du site contenant les modèles de porsche
        """
        # Récupère les différents types de modèles possibles
        models_dividers = response.css('.m-14-model-series-divider')

        # Pour chaque type (Modèles 718, 718 Cayman GT4 RS, etc.)
        for divider in models_dividers:
            model_type_url = divider.css('a::attr(href)').get()

            # Si le lien existe, accès à la page contenant les modèles liés
            if model_type_url:
                # Permet d'ouvrir ladite page
                yield response.follow(
                    model_type_url,
                    callback=self.parse_informations
                )

    def parse_informations(self, models_response) -> None:
        """
        Permet d'accéder aux différentes informations et stock les infos dans la
        BDD
        :param models_response: lien menant à une catégorie de porsche
        """
        # Récupère tous les conteneurs pour chaque modèle dudit type
        models = models_response.css('.m-364-module-specs-content')

        # Pour chaque modèle disponible
        for model in models:
            # On récupère toutes les informations qui nous intéressent
            dict_details = self.parse_details(model)

            yield PorscheScraperItem(
                acceleration=dict_details['acceleration'],
                top_speed=dict_details['top_speed'],
                image_url=self.parse_url_image(model),
                porsche_price=self.parse_price(model),
                porsche_name=self.parse_name(model),
                l_100_min=self.parse_l100(model),
                power_ch=dict_details['power'],
            )

    @staticmethod
    def parse_name(model_response) -> str:
        """
        Permet de récupérer le nom du modèle depuis un nom en plusieurs éléments
        :param model_response: contient la response contenant le nom
        :return: str contenant le nom du modèle
        """
        # On récupère le nom de notre modèle
        model_name_parts = model_response.css(
            '.m-364-module-headline--title *::text').getall()

        # On nettoie et récupère le nom complet
        full_model_name = ' '.join(
            part.strip() for part in model_name_parts if
            part.strip())

        return full_model_name

    @staticmethod
    def parse_price(model_response) -> str:
        """
        Permet de récupérer le prix du modèle depuis un prix en plusieurs
        éléments
        :param model_response: contient la response contenant le prix
        :return: prix du modèle
        """
        price = ''.join(re.findall(r'\d+', (model_response.css(
            '.m-364-module-headline--copy::text').get())))[:-2]

        return price

    @staticmethod
    def parse_l100(model_response) -> str:
        """
        Permet d'obtenir la valeur du nombre de litres pour 100 km
        :param model_response: contient la response contenant le l/100
        :return: str l_100
        """
        return model_response.css('span.b-eco__value::text').get()

    @staticmethod
    def parse_url_image(model_response) -> str:
        """
        Permet d'obtenir l'image de la porsche
        :param model_response: contient la response contenant l'url de l'image
        :return: str image_url
        """
        return model_response.css('img.m-364-module-image::attr(data-image-src)').get()

    @staticmethod
    def parse_details(model_response):
        """
        Permet de récupérer la puissance, l'accélération et la vitesse maximale
        :param model_response: contient les 3 informations
        :return: un dictionnaire avec les 3 valeurs
        """
        # Récupère l'ensemble des informations
        infos = model_response.css(
            '.m-364-techspecs-center .m-364-module-specs')

        return {
            # Récupère la puissance
            'power': infos.css('.m-364-module-specs-data--title::text').get(),
            # Récupère l'accélération
            'acceleration': infos.css(
                '.m-364-module-specs-data:nth-child(2) '
                '.m-364-module-specs-data--title::text').get(),
            # Récupère la vitesse maximale
            'top_speed': infos.css(
                '.m-364-module-specs-data:nth-child(3) '
                '.m-364-module-specs-data--title::text').get()
        }
