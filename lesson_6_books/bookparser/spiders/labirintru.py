import scrapy


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['http://labirint.ru/']

    def parse(self, response):
        pass
