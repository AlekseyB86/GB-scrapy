# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def clean_float(value):
    value = value.strip().replace(' ', '')
    try:
        value = float(value)
    except ValueError:
        pass
    return value


class LmparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(input_processor=MapCompose())
    price = scrapy.Field(input_processor=MapCompose(clean_float), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
