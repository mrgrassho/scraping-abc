import scrapy


class PanaleraEnCasaSpider(scrapy.Spider):
    name = 'panalera_en_casa'
    allowed_domains = ['panaleraencasa.com']
    start_urls = ['https://panaleraencasa.com/?s=pa%C3%B1al&post_type=product&product_cat=0']
    custom_settings = {
        # 'LOG_FILE': 'logs/panalera_en_casa.log',
        'LOG_LEVEL': 'DEBUG'
    }

    def parse(self, response):
        for item in response.xpath("//div[@class='product-information']"):
            price = item.xpath(".//span[@class='price']/span/text()").get()
            yield {
                "description": item.xpath(".//a[1]/text()").get(),
                "price": float(price.replace(",","")),
                "image": item.xpath("./..//img/@src").get(),
                "url": item.xpath(".//a[1]/@href").get(),
                "website": self.allowed_domains[0],
            }
        next_page = response.xpath("//a[contains(@class, 'next')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

