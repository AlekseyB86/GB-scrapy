# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re

from itemadapter import ItemAdapter
from pymongo import MongoClient

SALARY_RE = re.compile(r'(\d+\s?\d+)')
CURRENCY_RE = re.compile(r'\d+\s+([a-zA-Zа-яА-я]+)\.*\s*[^\d]*$')

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies1102

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
        _dirty_salary = ''.join(dirty_salary).replace(u'\xa0', ' ')
        salaries = re.findall(SALARY_RE, _dirty_salary)
        min_salary, max_salary, cur = None, None, None

        if salaries:
            cur = re.search(CURRENCY_RE, _dirty_salary).group(1)
            if len(salaries) == 1:
                salary_value = int(salaries[0].replace(' ', ''))
                if 'от' in _dirty_salary or 'до' not in _dirty_salary:
                    min_salary = salary_value
                else:
                    max_salary = salary_value
            else:
                min_salary, max_salary = int(salaries[0].replace(' ', '')), int(salaries[1].replace(' ', ''))
        return min_salary, max_salary, cur
