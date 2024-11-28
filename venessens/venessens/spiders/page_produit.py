# import scrapy



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
    start_urls = ['https://venessens-parquet.com/collection/les-parquets-dinterieur/']

    def parse(self, response):
        urls = response.xpath('//li[contains(@class, "product")]/a/@href').getall()
        for url in urls:
            yield {'url': url}

