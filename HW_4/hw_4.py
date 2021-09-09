from lxml import html
from pprint import pprint
import requests
from pymongo import MongoClient
import hashlib
import json

client = MongoClient('127.0.0.1', 27017)
db = client['test_db']
news = db.news

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

items_list = []

def scraper(web):
    response = requests.get(web, headers=header)
    dom = html.fromstring(response.text)

    if web == 'https://news.mail.ru/':
        print('mail')
        items = dom.xpath("//td[@class='daynews__main'] | //div[@class='daynews__item'] "
                          "| //ul[@class='list list_type_square list_half js-module']/li[@class = 'list__item']")
        for item in items:
            items_data = {}
            link = item.xpath(".//a/@href")[0]
            response = requests.get(link, headers=header)
            dom = html.fromstring(response.text)
            time = dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0]
            source = dom.xpath("//span[@class = 'breadcrumbs__item']//span[@class = 'link__text']/text()")[0]
            name = dom.xpath("//h1/text()")[0]
            items_data['link'] = link
            items_data['time'] = time
            items_data['source'] = source
            items_data['name'] = name
            items_data['_id'] = hashlib.sha1(json.dumps(items_data).encode()).hexdigest()
            items_list.append(items_data)
            news.update_one({'_id' : items_data['_id']}, {'$set' : items_data}, upsert = True )
    if web == 'https://lenta.ru/':
        print('lenta')
        items = dom.xpath("//div[contains(@class, 'yellow-box')]/div[@class][position()>1]")
        for item in items:
            items_data = {}
            link = web + item.xpath(".//a/@href")[0]
            source = 'Lenta.ru'
            name = item.xpath(".//a/text()")[0]
            response = requests.get(link, headers=header)
            dom = html.fromstring(response.text)
            time = dom.xpath("//div[contains(@class, 'b-topic__info')]//@datetime")[0]
            items_data['link'] = link
            items_data['time'] = time
            items_data['source'] = source
            items_data['name'] = name
            items_data['_id'] = hashlib.sha1(json.dumps(items_data).encode()).hexdigest()
            items_list.append(items_data)
            news.update_one({'_id': items_data['_id']}, {'$set': items_data}, upsert=True)
    if web == 'https://yandex.ru/news':
        print('yandex')
        items = dom.xpath("//div[contains(h1, 'Москва и область')]/following::article[contains(@class, 'mg-card_flexible')][position()<6]")
        for item in items:
            items_data = {}
            link = item.xpath(".//div[@class = 'mg-card__text']/a/@href")[0]
            source = item.xpath(".//a/text()")[0]
            name = item.xpath(".//div[@class = 'mg-card__text']/a//text()")[0]
            time = item.xpath(".//span[@class='mg-card-source__time']/text()")[0]
            items_data['link'] = link
            items_data['time'] = time
            items_data['source'] = source
            items_data['name'] = name
            items_data['_id'] = hashlib.sha1(json.dumps(items_data).encode()).hexdigest()
            items_list.append(items_data)
            news.update_one({'_id': items_data['_id']}, {'$set': items_data}, upsert=True)

scraper('https://news.mail.ru/')
print(len(items_list))
scraper('https://lenta.ru/')
print(len(items_list))
scraper('https://yandex.ru/news')
print(len(items_list))