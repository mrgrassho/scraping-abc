import re

import scrapy


class BotigaSpider(scrapy.Spider):
    name = 'botiga'
    start_urls = ['https://www.botiga.com.uy/panales-en-oferta-bebes.html?dir=asc&order=price']

    def parse(self, response):
        data = re.search("var impressionData = \{(.*)\}", response.text).group(1)
        descriptions = re.findall("\"name\":\"([^,]+)\"", data)
        prices = re.findall("\"price\":([0-9\.]+)", data)
        for description, price in zip(descriptions, prices):
            yield {
                "description": description.strip(),
                "price": float(price)
            }
