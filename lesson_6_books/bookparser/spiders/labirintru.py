import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = [f'https://www.labirint.ru/search/python/?stype=0']

    def parse(self, response: HtmlResponse, **kwargs):
        if next_page := response.xpath("//a[@class= 'pagination-next__text']/@href").get():
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@class= 'cover']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    @staticmethod
    def book_parse(response: HtmlResponse):
        url = response.url
        title = response.xpath('//h1//text()').get()
        authors = response.xpath('//a[@data-event-label="author"]//text()').get()
        discount_price = response.xpath('//span[@class="buying-pricenew-val-number"]//text()').get()
        price = response.xpath('//span[@class="buying-priceold-val-number"]//text()').get() or discount_price
        rating = response.xpath('//div[@id="rate"]//text()').get()
        yield BookparserItem(url=url, title=title, authors=authors, price=price,
                             discount_price=discount_price, rating=rating)
