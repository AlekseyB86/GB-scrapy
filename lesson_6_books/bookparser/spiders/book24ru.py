import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    page = 1
    start_urls = [f'https://book24.ru/search/page-{page}/?q=python']

    def parse(self, response: HtmlResponse, **kwargs):
        Book24ruSpider.page += 1
        next_page = f'https://book24.ru/search/page-{Book24ruSpider.page}/?q=python'
        if not response.xpath('//div[@class="not-found page-wrap__inner"]'):
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[contains(@class, 'product-card__image-link')]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    @staticmethod
    def book_parse(response: HtmlResponse):
        url = response.url
        title = response.xpath('//h1/text()').get()
        authors = response.xpath('//span[@class="product-characteristic__label"][contains(text(), "Автор")]/..//following-sibling::div//text()').get()
        discount_price = response.xpath('//meta[@itemprop="price"]/@content').get()
        price = response.xpath('//span[@class="app-price product-sidebar-price__price-old"]/text()').get() or discount_price
        rating = response.xpath('//span[@class="rating-widget__main-text"]/text()').get()

        yield BookparserItem(url=url,
                             title=title,
                             authors=authors,
                             discount_price=discount_price,
                             price=price,
                             rating=rating)
