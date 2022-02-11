from scrapy import crawler
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider


def start_crawler(crawler, crawler_settings=None):
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(crawler)
    process.start()


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    start_crawler(HhruSpider, crawler_settings)

    start_crawler(SjruSpider, crawler_settings)
