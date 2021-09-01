from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import json
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions as s_exceptions
import pprint
import hashlib
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['test_db']

letters = db.letters


def letter_to_dict():
    letter_dict = {}

    time.sleep(1)

    wait = WebDriverWait(driver, 10)
    subj = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'thread__subject'))).text
    date = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class = 'letter__date']"))).text
    sender = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'letter-contact')]"))).get_attribute('title')
    text = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class = 'letter__body']"))).text

    letter_dict['subj'] = subj
    letter_dict['date'] = date
    letter_dict['sender'] = sender
    letter_dict['text'] = text
    letter_dict['_id'] = hashlib.sha1(json.dumps(letter_dict).encode()).hexdigest()
    letters.update_one({'_id':letter_dict['_id']}, {'$set':letter_dict}, upsert = True)

    return letter_dict

chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome('C:\chromedriver.exe', options=chrome_options)
driver.get('https://www.mail.ru/')

elem = driver.find_element_by_name("login")
elem.send_keys('test_for_parcer@mail.ru')

elem = driver.find_element_by_xpath("//button[@data-testid='enter-password']")
elem.click()

time.sleep(1)

elem = driver.find_element_by_name("password")
elem.send_keys('gfhcbyulfyys[')
elem.send_keys(Keys.ENTER)

letter_list = []

wait = WebDriverWait(driver, 10)
letter = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@class = 'llc js-tooltip-direction_letter-bottom js-letter-list-item llc_normal']")))
letter.click()

all_letters = []

while True:
    try:
        wait = WebDriverWait(driver, 10)
        next_but = wait.until(EC.element_to_be_clickable((By.XPATH, ".//span[contains(@class, 'arrow-down')]")))
        letter_list.append(letter_to_dict())
        next_but.click()
    except s_exceptions.ElementClickInterceptedException:
        print('Все письма перебраны')
        break



