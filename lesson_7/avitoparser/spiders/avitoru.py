import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from avitoparser.items import AvitoparserItem


class AvitoruSpider(scrapy.Spider):
    name = 'avitoru'
    allowed_domains = ['avito.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.avito.ru/rossiya?cd=1&q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-marker='item-title']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoparserItem(), response=response)
        loader.add_xpath('name', "//h1/span/text()")
        loader.add_xpath('price', "//span[@class='js-item-price']/text()")
        loader.add_xpath('photos', "//div[contains(@class,'gallery-img-frame')]/@data-url")
        loader.add_value('url', response.url)
        yield loader.load_item()

        # name = response.xpath("//h1/span/text()").get()
        # price = response.xpath("//span[@class='js-item-price']/text()").get()
        # url = response.url
        # photos = response.xpath("//div[contains(@class,'gallery-img-frame')]/@data-url").getall()
        # yield AvitoparserItem(name=name, price=price, url=url, photos=photos)

