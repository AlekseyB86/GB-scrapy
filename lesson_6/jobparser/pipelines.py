# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies0902

    def process_item(self, item, spider):
        salary = self.process_salary(item.get('salary'))
        item['salary_min'], item['salary_max'], item['cur'] = salary
        del item['salary']

        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, dirty_salary):
        """
        Обработка salary
        :param dirty_salary:
        :return:
        """
        min_salary, max_salary, cur = None, None, None
        if 1 < len(dirty_salary) < 6:
            cur = dirty_salary[3]
            if dirty_salary[0] == 'от ':
                min_salary = int(dirty_salary[1].replace(u'\xa0', ''))
            else:
                max_salary = int(dirty_salary[1].replace(u'\xa0', ''))
        elif len(dirty_salary) > 6:
            cur = dirty_salary[5]
            min_salary = int(dirty_salary[1].replace(u'\xa0', ''))
            max_salary = int(dirty_salary[3].replace(u'\xa0', ''))
        return min_salary, max_salary, cur
