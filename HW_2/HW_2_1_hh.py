import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd
import numpy as np
import json

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

url = 'https://www.hh.ru'

prof = input('Введите наименование интересующей Вас вакансии: \n')
page_count = int(input('Введите количество страниц для анализа: \n'))
page_count_max = 40
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

if page_count > page_count_max:
    print("HH.ru выдает не более 40 страниц в результатах поиска, анализ будет произведен "
          "по всем выданным страницам")
    page_count = page_count_max

page_count_finall = 0
for page in range(page_count):
    params = {'clusters': 'true', 'area': 1, 'enable_snippets': 'true', 'salary': '', 'st': 'searchVacancy',
              'text': prof, 'from': 'suggest_post', 'page': page}
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    jobs = soup.find_all('div', {'class': 'vacancy-serp-item'})
    if (len(jobs) == 0) or (str(response) != '<Response [200]>'):
        page_count = page_count_finall
        print(f'BREAK, {response}, {len(jobs)}, {page_count}')
        break
    else:
        page_count_finall += 1
        print(f'Найдено страниц с релевантными данными: {page_count_finall}')

jobs_list = []
for page_number in range(page_count):
    params = {'clusters':'true', 'area':1, 'enable_snippets':'true', 'salary':'', 'st':'searchVacancy',
              'text':prof, 'from':'suggest_post', 'page':page_number}
    response = requests.get(url+'/search/vacancy', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    jobs = soup.find_all('div', {'class':'vacancy-serp-item'})
    print(f'Анализирую {page_number+1} страницу')
    for job in jobs:
        job_data = {}
        info1 = job.find('a', {'class':'bloko-link'})
        info2 = job.find('a', {'data-qa':'vacancy-serp__vacancy-employer'})
        name = info1.text
        link = info1['href']
        try:
            link_employer = url + info2['href']
        except:
            link_employer = None
        try:
            salary = job.find('span', {'data-qa':'vacancy-serp__vacancy-compensation'}).text.replace('\u202f','')
            if ' – ' in salary:
                ind = salary.find(' – ')
                salary_min = float(salary[:ind].replace(' ',''))
                salary_max = float(salary[ind+3:-4].replace(' ',''))
                salary_cur = salary[-4:].replace('.', '').replace(' ', '')
            elif 'от ' in salary:
                salary_min = float(salary[3:-4].replace(' ', ''))
                salary_max = None
                salary_cur = salary[-4:].replace('.', '').replace(' ', '')
            else: salary_min, salary_max = None
        except:
            salary, salary_min, salary_max, salary_cur = None, None, None, None

        job_data['name'] = name
        job_data['link'] = link
        job_data['link_employer'] = link_employer
        job_data['salary'] = salary
        job_data['salary_min'] = salary_min
        job_data['salary_max'] = salary_max
        job_data['salary_cur'] = salary_cur
        jobs_list.append(job_data)

pprint(jobs_list[1])
print(f'Собрана информация по {len(jobs_list)} вакансиям')
print(f'Проанализировано: {page_count_finall} страниц')
with open('hh.json', 'w') as f:
    json.dump(jobs_list, f)
with open('hh.csv', 'w') as f:
    pd.DataFrame(jobs_list).to_csv(f, encoding='utf-8')