import scrapy
import time


class CategorieSpider(scrapy.Spider):
    name = "categorie"
    allowed_domains = ["venessens-parquet.com"]
    start_urls = ["https://venessens-parquet.com"]
    url_visiter = set() #ajout d'un set pour éviter les doublons

    def parse(self, response):
        categories= response.xpath('//ul[@class="elementor-nav-menu sm-vertical"]//a')
        # noms_url = response.xpath('//ul[@class="elementor-nav-menu sm-vertical"]//a/text()').getall()

        for categorie in categories : 
            url = categorie.xpath('@href').get()
            nom = categorie.xpath('text()').get()

            if url and 'https://venessens-parquet.com/collection' in url and url not in self.url_visiter:

                self.url_visiter.add(url)

                yield{
                    'Catégorie' : nom.strip() if nom else "nom inconnu",
                    'URL' : url
                }
                