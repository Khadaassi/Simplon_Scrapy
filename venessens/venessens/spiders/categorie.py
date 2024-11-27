import scrapy


class CategorieSpider(scrapy.Spider):
    name = "categorie"
    allowed_domains = ["venessens-parquet.com"]
    start_urls = ["https://venessens-parquet.com"]
    url_visiter = set() # set pour éviter les doublons

    def parse(self, response):

        categories = response.xpath('//ul[@class="elementor-nav-menu sm-vertical"]//a')

        for categorie in categories:
            url = categorie.xpath('@href').get()
            nom = categorie.xpath('text()').get()

            if url and 'https://venessens-parquet.com/collection' in url and url not in self.url_visiter:
                self.url_visiter.add(url)

                yield {
                    'Catégorie': nom.strip() if nom else "Nom inconnu",
                    'URL': url
                }

                #yield response.follow(url, callback=self.parse_page_produits)

