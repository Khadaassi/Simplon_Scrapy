import scrapy
import csv


class PageProduitSpider(scrapy.Spider):
    name = "page_produit"
    allowed_domains = ["venessens-parquet.com"]
    start_url = ['https://venessens-parquet.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categorie = self.read_csv()

    def start_requests(self):
        for url in self.categorie:
            yield scrapy.Request(
                url = url, 
                callback= self.parse_page_produits
            )

    def read_csv(self):
        urls = {}
        with open('categorie.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                urls['Catégorie']=['URL']
            
        return urls

    def parse_page_produits(self, response):
        pages = response.css('li a::attr(href)').getall()

        for page in pages:
            if 'https://venessens-parquet.com/collections' in page:
                yield response.follow(page, callback=self.parse_produits)
    
    def parse_produits(self, response):
        reference = response.xpath('//span[@class="reference"]/text()').get()
        nom = response.xpath('//h1/text()').get()
        prix =response.xpath('//span[@class="prix"]/text()').get()
        produits = {
            'Nom': nom.strip() if nom and nom.strip() else "Nom inconnu",
            'Reference': reference.strip() if reference else "Référence inconnue",
            'Prix': prix.strip() if prix else "Prix non disponible",
        }
        yield produits