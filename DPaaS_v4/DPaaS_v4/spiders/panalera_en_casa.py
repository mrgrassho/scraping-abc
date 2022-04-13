import scrapy


class PanaleraEnCasaSpider(scrapy.Spider):
    name = 'panalera_en_casa'
    allowed_domains = ['panaleraencasa.com']
    start_urls = ['https://panaleraencasa.com/?s=pa%C3%B1al&post_type=product&product_cat=0']

    def parse(self, response):
        for item in response.xpath("//div[@class='product-information']"):
            price = item.xpath(".//span[@class='price']/span/text()").get()
            yield {
                "description": item.xpath(".//a[1]/text()").get(),
                "price": float(price.replace(",",""))
            }
        next_page = response.xpath("//a[contains(@class, 'next')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

