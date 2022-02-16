# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient


class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        client.drop_database('insta1602')
        self.mongobase = client.insta1602

    def process_item(self, item, spider):
        try:
            collection = self.mongobase[f'{item["from_user"]}-{item["type"]}']
            collection.insert_one(item)
        except Exception as e:
            print(e)
        return item
