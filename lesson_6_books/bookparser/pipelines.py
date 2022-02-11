# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        client.drop_database('books1102')
        self.mongobase = client.books1102

    def process_item(self, item, spider):
        if item['price']:
            item['price'] = int(''.join(filter(str.isdigit, item['price'])))
        if item['discount_price']:
            item['discount_price'] = int(item['discount_price'])
        if spider.name == 'labirintru':
            item['rating'] = float(item['rating'])
        else:
            float(item['rating'].strip().replace(',', '.')) * 2
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item
