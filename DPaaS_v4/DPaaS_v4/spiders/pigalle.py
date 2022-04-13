import scrapy


class PigalleSpider(scrapy.Spider):
    name = 'pigalle'
    allowed_domains = ['www.pigalle.com.uy']
    start_urls = ['https://www.pigalle.com.uy/bebes_panales-y-toallitas']

    def parse(self, response):
        for item in response.xpath("//div[contains(@class, 'item-box')]"):
            price = item.xpath(".//div[contains(@class, 'prod-box__current-price')]/text()").get()
            yield {
                "description": item.xpath(".//h2/text()").get().strip(),
                "price": float(price.strip().replace(".", "").replace("$",""))
            }
        next_page = response.xpath("//li[@class='next-page']/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
