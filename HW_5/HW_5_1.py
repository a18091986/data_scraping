from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import json
import selenium.common.exceptions as s_exc
import hashlib
from pymongo import MongoClient


client = MongoClient('127.0.0.1', 27017)
db = client['test_db']
goods = db.goods

chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome('C:\chromedriver.exe', options=chrome_options)
driver.get('https://www.mvideo.ru/')

nova = driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]/../../..")

actions = ActionChains(driver)
actions.move_to_element(nova)
actions.perform()

while True:
    try:
        button = nova.find_element_by_xpath(".//a[@class='next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right']")
        button.click()
    except s_exc.NoSuchElementException:
        break

nova_all = driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]/../../..")
items = nova_all.find_elements_by_xpath(".//li[contains(@class, 'gallery-list-item')]")
for item in items:
    good = json.loads(item.find_elements_by_xpath('.//a[@data-product-info]')[1].get_attribute('data-product-info'))
    good['_id'] = hashlib.sha1(json.dumps(good).encode()).hexdigest()
    print(good)
    goods.update_one({'_id': good['_id']}, {'$set': good}, upsert=True)