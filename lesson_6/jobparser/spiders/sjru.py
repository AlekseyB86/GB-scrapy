import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = [
        'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4',
        'https://spb.superjob.ru/vacancy/search/?keywords=python'
    ]

    def parse(self, response: HtmlResponse, **kwargs):
        if next_page := response.xpath("//a[contains(@class, 'f-test-button-dalshe')]/@href").get():
            yield response.follow(next_page, callback=self.parse)

        links_sjru = response.xpath("//a[contains(@class, '_2JivQ _1UJAN')]/@href").getall()
        for link in links_sjru:
            yield response.follow(link, callback=self.vacancy_parse_sjru)

    def vacancy_parse_sjru(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        url = response.url
        salary = response.xpath("//span[@class='_2Wp8I _3a-0Y _3DjcL _3fXVo']//text()").getall()
        yield JobparserItem(name=name, salary=salary, url=url)
