from itemadapter import ItemAdapter
from pymongo import MongoClient

class BooksPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        item['source'] = spider.name
        if spider.name == 'book24':
            item['name'], item['author'], item['price_main'], item['rating'] = \
                self.process_item_correct_book24(item['name'], item['author'], item['price_main'], item['rating'])
        if spider.name == 'labirint':
            item['price_main'], item['price_discont'] = \
                self.process_item_correct_labirint(item['price_main'], item['price_discont'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_item_correct_book24(self, name, author, price_main, rating):
        try:
            name = name.replace('\n', '').replace('  ', '')
        except:
            name = name
        try:
            author = author.replace('\n', '').replace('  ', '')
        except:
            author = author
        try:
            price_main = float(price_main.replace('\n','').replace(' ', '').replace('₽','').replace('\xa0',''))
        except:
            price_main = price_main
        try:
            rating = float(rating.replace('\n','').replace('  ', '').replace(',', '.'))
        except:
            rating = rating
        return name, author, price_main, rating

    def process_item_correct_labirint(self, price_main, price_discont):
        try:
            price_main, price_discont = float(price_main), float(price_discont)
        except:
            price_main, price_discont = None, None
        return price_main, price_discont
