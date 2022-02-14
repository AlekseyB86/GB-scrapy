import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoparserItem


class AvitoruSpider(scrapy.Spider):
    name = 'avitoru'
    allowed_domains = ['avito.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.avito.ru/rossiya?cd=1&q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse):
        print()
