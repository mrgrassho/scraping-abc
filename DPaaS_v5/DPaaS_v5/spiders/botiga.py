import re

import scrapy


class BotigaSpider(scrapy.Spider):
    name = 'botiga'
    allowed_domains = ['www.botiga.com.uy']
    start_urls = ['https://www.botiga.com.uy/panales-en-oferta-bebes.html?dir=asc&order=price']

    def parse(self, response):
        data = re.search("var impressionData = \{(.*)\}", response.text).group(1)
        descriptions = re.findall("\"name\":\"([^,]+)\"", data)
        prices = re.findall("\"price\":([0-9\.]+)", data)
        images = response.xpath("//li[contains(@class, 'item')]//img/@src").getall()
        urls = response.xpath("//h3[@class='product-name']/a/@href").getall()
        for description, price, image, url in zip(descriptions, prices, images, urls):
            yield {
                "description": description.strip(),
                "price": float(price),
                "image": image,
                "url": url,
                "website": self.allowed_domains[0],
            }
