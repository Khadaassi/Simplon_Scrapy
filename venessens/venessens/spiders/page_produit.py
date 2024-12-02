import scrapy
import csv
from venessens.items import ProduitItem


class PageProduitSpider(scrapy.Spider):
    """
    Spider pour extraire les informations des produits depuis les pages d'une catégorie
    du site Venessens. Il utilise un fichier CSV pour obtenir les URLs des catégories 
    et navigue entre les pages pour collecter les données produit.
    """
    name = "page_produit"  # Nom unique du spider
    allowed_domains = ["venessens-parquet.com"]  # Domaine autorisé pour le scraping
    urls_depart = ['https://venessens-parquet.com']  # URL(s) de départ (non utilisée directement ici)

    def __init__(self, *args, **kwargs):
        """
        Initialisation du spider. Lit les catégories depuis un fichier CSV pour 
        préparer la liste des URL de départ.
        """
        super().__init__(*args, **kwargs)
        self.categories = self.lire_csv()  # Liste des catégories extraites du CSV

    def start_requests(self):
        """
        Démarre les requêtes Scrapy pour chaque URL de catégorie extraite du fichier CSV.

        Yields:
            scrapy.Request: Requête initiale vers une catégorie.
        """
        for categorie in self.categories:
            yield scrapy.Request(
                url=categorie['url_categorie'], 
                callback=self.parse_pages_produits,  # Callback pour gérer les pages de produits
                meta={'nom_categorie': categorie['nom_categorie']}  # Métadonnées pour les produits
            )

    def lire_csv(self):
        """
        Lit un fichier CSV contenant les informations des catégories et filtre celles
        correspondant aux listes de produits.

        Returns:
            list: Liste de dictionnaires contenant les noms et URLs des catégories.
        """
        urls_categories = []
        with open('categorie.csv', newline='') as fichier_csv:
            lecteur = csv.DictReader(fichier_csv)
            for ligne in lecteur:
                # Filtrer uniquement les catégories marquées comme pages de liste
                if ligne.get('is_page_list') == 'True':
                    urls_categories.append({
                        'nom_categorie': ligne['nom_categorie'], 
                        'url_categorie': ligne['url_categorie']
                    })
        return urls_categories

    def parse_pages_produits(self, response):
        """
        Analyse une page de catégorie pour extraire les liens des pages de produits
        et naviguer entre les pages si nécessaire.

        Args:
            response (scrapy.http.Response): Réponse de la requête HTTP.

        Yields:
            scrapy.Request: Requêtes pour les pages de produits ou la page suivante.
        """
        # Extraire les liens des produits de la catégorie
        liens_pages = response.css('li a::attr(href)').getall()
        for lien_page in liens_pages:
            if 'https://venessens-parquet.com/collections' in lien_page:
                # Suivre les liens pour extraire les produits
                yield response.follow(lien_page, callback=self.parse_produits, meta=response.meta)

        # Gérer la pagination en suivant le lien "suivant"
        lien_suivant = response.xpath('//a[@class="next page-numbers"]/@href').get()
        if lien_suivant:
            url_suivante = response.urljoin(lien_suivant)
            yield response.follow(url=url_suivante, callback=self.parse_pages_produits, meta=response.meta)

    def parse_produits(self, response):
        """
        Analyse une page de produit pour extraire les détails du produit et les 
        stocker dans un item.

        Args:
            response (scrapy.http.Response): Réponse de la requête HTTP.

        Yields:
            ProduitItem: Objet contenant les informations sur un produit.
        """
        item = ProduitItem()
        item['nom_categorie'] = response.meta['nom_categorie']  # Récupérer la catégorie depuis les métadonnées
        item['nom_produit'] = response.xpath('//h1/text()').get()  # Nom du produit
        item['prix_produit'] = response.xpath('//span[@class="prix"]/text()').get()  # Prix du produit
        item['reference_produit'] = response.xpath('//span[@class="reference"]/text()').get()  # Référence du produit
        item['url_produit'] = response.url  # URL de la page produit
        yield item
