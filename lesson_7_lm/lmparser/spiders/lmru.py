import scrapy
from scrapy.http import HtmlResponse
from lmparser.items import LmparserItem
from scrapy.loader import ItemLoader


class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse, **kwargs):
        if next_page := response.xpath('//a[@data-qa-pagination-item="right"]/@href').get():
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//a[@data-qa="product-image"]')
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LmparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photos', "*//img[@alt='product image']/@src")
        loader.add_value('url', response.url)
        yield loader.load_item()
