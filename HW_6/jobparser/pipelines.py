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
        self.mongo_base = client.vacancy0309

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salary_hh(item['salary'])
        if spider.name == 'sjru':
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salary_sjru(item['salary'])
        item['source'] = spider.name
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, salary):
        try:
            salary = salary.replace('\u202f', '')
            salary = salary.replace('\xa0', '')
            if 'до' in salary and 'от' in salary:
               salary_min = float([x for x in salary.split(' ')][1])
               salary_max = float([x for x in salary.split(' ')][3])
               salary_cur = [x for x in salary.split(' ')][4]
            elif 'от ' in salary:
                salary_min = float([x for x in salary.split(' ')][1])
                salary_max = None
                salary_cur = [x for x in salary.split(' ')][2]
            elif 'до ' in salary:
                salary_min = None
                salary_max = float([x for x in salary.split(' ')][1])
                salary_cur = [x for x in salary.split(' ')][2]
            else:
                salary_min, salary_max, salary_cur = None
        except:
            salary_min, salary_max, salary_cur = None, None, None
        return  salary_min, salary_max, salary_cur

    def process_salary_sjru(self, salary):
        # salary = ' '.join(salary)
        try:
            # salary = salary.replace('\xa0', '')
            # salary = salary.replace(' ', '')
            if '—' in salary:
               salary_min = float(''.join(i for i in salary[0] if i.isdigit()))
               salary_max = float(''.join(i for i in salary[4] if i.isdigit()))
               salary_cur = ''.join(i for i in salary[6] if not i.isdigit()).replace('\xa0', '')
            elif 'от' in salary:
                salary_min = float(''.join(i for i in salary[2] if i.isdigit()))
                salary_max = None
                salary_cur = ''.join(i for i in salary[2] if not i.isdigit()).replace('\xa0', '')
            elif 'до' in salary:
                salary_min = None
                salary_max = float(''.join(i for i in salary[2] if i.isdigit()))
                salary_cur = [x for x in salary.split(' ')][2]
            else:
                salary_min, salary_max, salary_cur = None
        except:
            salary_min, salary_max, salary_cur = None, None, None
        return salary_min, salary_max, salary_cur