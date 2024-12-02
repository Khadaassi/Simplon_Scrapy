import scrapy
from venessens.items import CategorieItem

class CategorieSpider(scrapy.Spider):
    """
    Spider pour extraire les catégories de produits depuis le site Venessens.
    Ce spider collecte à la fois les collections parentes et les collections enfants, en évitant les doublons.
    """
    name = "categorie"  # Nom unique du spider
    allowed_domains = ["venessens-parquet.com"]  # Domaine autorisé pour éviter les requêtes externes
    start_urls = ["https://venessens-parquet.com"]  # URL de départ pour le scraping
    urls_visitees = set()  # Ensemble des URLs visitées pour éviter les doublons
    urls_parent_visitees = set()  # Ensemble des URLs des collections parentes visitées

    def parse(self, response):
        """
        Méthode principale pour analyser la réponse HTTP.
        Elle identifie les catégories et génère des items correspondant aux collections parentes et enfants.

        Args:
            response (scrapy.http.Response): Réponse HTTP obtenue après la requête initiale.

        Yields:
            CategorieItem: Objet représentant une catégorie ou une collection extraite.
        """
        # Localiser les éléments des catégories dans le menu vertical
        elements_categories = response.xpath('//ul[@class="elementor-nav-menu sm-vertical"]//a')

        for element_categorie in elements_categories:
            # Extraire l'URL et le nom de la catégorie
            url_categorie = element_categorie.xpath('@href').get()
            nom_categorie = element_categorie.xpath('text()').get()

            # Vérifier si l'URL appartient à une collection et n'a pas encore été visitée
            if url_categorie and 'https://venessens-parquet.com/collection' in url_categorie and url_categorie not in self.urls_visitees:
                self.urls_visitees.add(url_categorie)  # Marquer l'URL comme visitée

                # Analyser l'URL pour identifier les informations sur la collection parente
                segments_url = url_categorie.rstrip('/').split('/')
                nom_collection_parent = segments_url[-2]  # Segment représentant le nom de la collection parente
                url_collection_parent = "/".join(segments_url[:-1])  # URL de la collection parente
                nom_collection_parent_formatte = nom_collection_parent.replace('-', ' ').capitalize()  # Mise en forme du nom

                # Si la collection parente n'a pas encore été visitée, générer un item pour celle-ci
                if url_collection_parent not in self.urls_parent_visitees:
                    self.urls_parent_visitees.add(url_collection_parent)  # Marquer l'URL parente comme visitée

                    # Créer un item pour la collection parente
                    item_parent = CategorieItem(
                        nom_categorie=nom_collection_parent_formatte,
                        url_categorie=url_collection_parent,
                        is_page_list=False  # Indique que c'est une page parente
                    )
                    yield item_parent

                # Créer un item pour la catégorie enfant
                item_enfant = CategorieItem(
                    nom_categorie=nom_categorie,
                    url_categorie=url_categorie,
                    is_page_list=True  # Indique que c'est une page enfant
                )
                yield item_enfant
