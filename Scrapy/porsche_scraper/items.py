"""
    Module définissant les items pour le scraping

    Auteurs : Lucas SALI--ORLIANGE
    Date : janvier 2024
"""

import scrapy


class PorscheScraperItem(scrapy.Item):
    """
        Class permettant de définir les items liés au scraping
    """
    porsche_price = scrapy.Field()
    acceleration = scrapy.Field()
    porsche_name = scrapy.Field()
    top_speed = scrapy.Field()
    image_url = scrapy.Field()
    l_100 = scrapy.Field()
    power = scrapy.Field()
