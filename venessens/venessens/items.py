import scrapy

class CategorieItem(scrapy.Item):
    """
    Classe représentant une catégorie extraite par le spider.
    Chaque objet `CategorieItem` contient les informations nécessaires pour décrire une catégorie.
    """
    nom_categorie = scrapy.Field()  # Nom de la catégorie 
    url_categorie = scrapy.Field()  # URL associée à la catégorie
    is_page_list = scrapy.Field()  # Indique si la catégorie est une page de liste (booléen)

class ProduitItem(scrapy.Item):
    """
    Classe représentant un produit extrait par le spider.
    Chaque objet `ProduitItem` contient les informations nécessaires pour décrire un produit.
    """
    nom_categorie = scrapy.Field()  # Nom de la catégorie à laquelle le produit appartient
    nom_produit = scrapy.Field()  # Nom du produit 
    prix_produit = scrapy.Field()  # Prix du produit 
    reference_produit = scrapy.Field()  # Référence du produit 
    url_produit = scrapy.Field()  # URL de la page du produit
