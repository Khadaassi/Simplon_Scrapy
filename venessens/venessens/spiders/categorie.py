import scrapy
import time


class CategorieSpider(scrapy.Spider):
    name = "categorie"
    allowed_domains = ["venessens-parquet.com"]
    start_urls = ["https://venessens-parquet.com"]
    url_visiter = set() #ajout d'un set pour éviter les doublons

    def parse(self, response):
        categories_url = response.xpath('//ul[@class="elementor-nav-menu sm-vertical"]//a/@href').getall()
        noms_url = response.xpath('//ul[@class="elementor-nav-menu sm-vertical"]//a/text()').getall()

        for categorie_url in categories_url:
            if 'https://venessens-parquet.com/collection' in categorie_url:
                for nom_url in noms_url:
                    if categorie_url not in self.url_visiter:
                        self.url_visiter.add(categorie_url)
                        yield{
                            'Nom' : nom_url,
                            'URL' : categorie_url
                        }
                    
    def parse_categorie(self, response):
        # url/collection + /sous_cat
        pass