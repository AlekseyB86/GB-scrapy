import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    # 1 - moscow, 2 - piter
    start_urls = [
        'https://hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&items_on_page=20&text=python',
        'https://hh.ru/search/vacancy?area=2&search_field=name&search_field=company_name&search_field=description&items_on_page=20&text=python']

    def parse(self, response: HtmlResponse, **kwargs):
        if next_page := response.xpath("//a[@data-qa='pager-next']/@href").get():
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
