import scrapy


class PageProduitSpider(scrapy.Spider):
    name = "page_produit"
    allowed_domains = ["venessens-parquet.com"]
    start_urls = ["https://venessens-parquet.com/collection/les-parquets-dinterieur/collection-archi/"]

    def parse(self, response):
        pages = response.css('li a::attr(href)').getall()

        for page in pages:
            if 'https://venessens-parquet.com/collections' in page:
                yield response.follow(page, callback=self.parse_page)
    
    def parse_page(self, response):
        reference = response.xpath('//span[@class="reference"]/text()').get()
        nom = response.xpath('//h1/text()').get()
        prix =response.xpath('//span[@class="prix"]/text()').get()
        yield{
            'Nom' : nom,
            'Reference' : reference,
            'Prix' : prix
        }


    
        