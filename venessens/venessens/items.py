# Define here the models for your scraped items
#
# See documentation in:
#https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CategorieItem(scrapy.Item):
    # define the fields for your item here like:
    nom_categorie = scrapy.Field()
    url_categorie = scrapy.Field()
    is_page_list = scrapy.Field()

class ProduitItem(scrapy.Item):
    nom_categorie = scrapy.Field()
    nom_produit = scrapy.Field()
    prix_produit = scrapy.Field()
    reference_produit = scrapy.Field()
    url_produit = scrapy.Field()
