import scrapy


class CategorieSpider(scrapy.Spider):
    name = "categorie"
    allowed_domains = ["venessens-parquet.com"]
    start_urls = ["https://venessens-parquet.com"]
    urls_visitees = set()  # Ensemble pour éviter les doublons
    urls_parent_visitees = set()

    def parse(self, response):
        elements_categories = response.xpath('//ul[@class="elementor-nav-menu sm-vertical"]//a')

        for element_categorie in elements_categories:
            url_categorie = element_categorie.xpath('@href').get()
            nom_categorie = element_categorie.xpath('text()').get()

            if url_categorie and 'https://venessens-parquet.com/collection' in url_categorie and url_categorie not in self.urls_visitees:
                self.urls_visitees.add(url_categorie)
                
                segments_url = url_categorie.rstrip('/').split('/')
                nom_collection_parent = segments_url[-2]
                url_collection_parent = "/".join(segments_url[:-1])
                nom_collection_parent_formatte = nom_collection_parent.replace('-', ' ').capitalize()

                if url_collection_parent not in self.urls_parent_visitees:
                    self.urls_parent_visitees.add(url_collection_parent)
                    yield{
                        'nom_categorie': nom_collection_parent_formatte,
                        'url_categorie': url_collection_parent,
                        'is_page_list' : False
                    }

                yield {
                    'nom_categorie': nom_categorie,
                    'url_categorie': url_categorie,
                    'is_page_list' : True
                }
