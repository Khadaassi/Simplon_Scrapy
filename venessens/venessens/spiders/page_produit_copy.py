import scrapy
import csv


class PageProduitSpider(scrapy.Spider):
    name = "page_produit_copy"
    allowed_domains = ["venessens-parquet.com"]
    start_url = ['https://venessens-parquet.com']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories = self.read_csv()

    def start_requests(self):
        for categorie in self.categories:
            yield scrapy.Request(
                url=categorie['URL'], 
                callback= self.parse_page_produits,
                meta= {'nom' : categorie['Catégorie']}
            )

    def read_csv(self):
        urls = []
        with open('categorie.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                urls.append({'Catégorie': row['Catégorie'], 'URL': row['URL']})
        return urls
    
    def parse_page_produits(self, response):
        pages = response.css('li a::attr(href)').getall()
        for page in pages:
            if 'https://venessens-parquet.com/collections' in page:
                yield response.follow(page, callback=self.parse_produits, meta=response.meta)

            next = response.xpath("//a[@class='next page-numbers']/@href").get()
            if next :
                new_url = response.urljoin(next)
                yield scrapy.Request(url = new_url, callback= self.parse_page_produits, meta=response.meta)
    
    def parse_produits(self, response):
        reference = response.xpath('//span[@class="reference"]/text()').get()
        nom = response.xpath('//h1/text()').get()
        prix =response.xpath('//span[@class="prix"]/text()').get()
        produits = {
            'Catégorie' : response.meta['nom'],
            'Nom': nom.strip() if nom and nom.strip() else "Nom inconnu",
            'Prix': prix.strip() if prix else "Prix non disponible",
            'Reference': reference.strip() if reference else "Référence inconnue",
            'URL' : response.url
        }
        yield produits
