# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import scrapy
import hashlib
from scrapy.utils.python import to_bytes
from pymongo import MongoClient



class InstagramPipeline:

    def __init__(self):

        client = MongoClient('localhost', 27017)
        self.mongobase = client['Instagram']

    def process_item(self, item, spider):
        try:
            collections = self.mongobase[spider.name]
            collections.update_one({'_id': {'$eq': item['_id']}}, {'$set': item}, upsert=True)
        except:
            pass
        return item