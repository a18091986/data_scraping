import scrapy


class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    price_main = scrapy.Field()
    price_discont = scrapy.Field()
    rating = scrapy.Field()
    source = scrapy.Field()
    _id = scrapy.Field()
