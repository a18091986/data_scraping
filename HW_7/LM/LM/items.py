# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst            # Подключаемые обработчики

def process_price(value):                                           # Функция для обработки цен
    value = value.replace(' ', '')
    try:
        return int(value)
    except:
        return value

def process_describe(value):                                           # Функция для обработки цен
    value = value.replace('\n', '').replace('  ', '')
    return value



class LMparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())                        # Теперь у поля есть обработчики
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    describe = scrapy.Field(input_processor=MapCompose(process_describe))
    photos = scrapy.Field()
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
