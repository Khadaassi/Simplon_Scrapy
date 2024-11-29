import scrapy
import csv
from venessens.items import ProduitItem



# class PageProduitSpider(scrapy.Spider):
#     name = "page_produit"
#     allowed_domains = ["venessens-parquet.com"]
#     start_url = ['https://venessens-parquet.com/collection/les-parquets-dinterieur/']

    
#     def parse_(self, response):

#         url = {
#             'url':response.xpath('//li[@class="product type-product post-3718 status-publish first instock product_cat-les-parquets-dinterieur product_cat-parquet-massif has-post-thumbnail purchasable product-type-simple"]/a/@href').getall()

#         }
#         yield url

import scrapy

class PageProduitSpider(scrapy.Spider):
    name = "page_produit"
    allowed_domains = ["venessens-parquet.com"]
    urls_depart = ['https://venessens-parquet.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories = self.lire_csv()

    def start_requests(self):
        for categorie in self.categories:
            yield scrapy.Request(
                url=categorie['url_categorie'], 
                callback=self.parse_pages_produits,
                meta={'nom_categorie': categorie['nom_categorie']}
            )

    def lire_csv(self):
        urls_categories = []
        with open('categorie.csv', newline='') as fichier_csv:
            lecteur = csv.DictReader(fichier_csv)
            for ligne in lecteur:
                if ligne.get('is_page_list') == 'True':
                    urls_categories.append({
                        'nom_categorie': ligne['nom_categorie'], 
                        'url_categorie': ligne['url_categorie']
                    })
        return urls_categories

    def parse_pages_produits(self, response):
        liens_pages = response.css('li a::attr(href)').getall()
        for lien_page in liens_pages:
            if 'https://venessens-parquet.com/collections' in lien_page:
                yield response.follow(lien_page, callback=self.parse_produits, meta=response.meta)
        
        lien_suivant = response.xpath('//a[@class="next page-numbers"]/@href').get()
        if lien_suivant:
            url_suivante = response.urljoin(lien_suivant)
            yield response.follow(url=url_suivante, callback=self.parse_pages_produits, meta=response.meta)

    def parse_produits(self, response):
        item = ProduitItem()
        item['nom_categorie'] = response.meta['nom_categorie']
        item['nom_produit'] = response.xpath('//h1/text()').get()
        item['prix_produit'] = response.xpath('//span[@class="prix"]/text()').get()
        item['reference_produit'] = response.xpath('//span[@class="reference"]/text()').get()
        item['url_produit'] = response.url
        yield item
