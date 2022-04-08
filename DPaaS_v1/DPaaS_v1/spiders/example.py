import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = ['http://example.com/']

    def parse(self, response):
        return {
            "title": response.xpath("//h1/text()").get(),
            "description": response.xpath("//p[1]/text()").get(),
        }
