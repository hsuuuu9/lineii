from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import openpyxl
import random
import collections
from urllib.parse import urlparse
from sqlalchemy import create_engine
import pandas as pd
import MySQLdb
import pymysql
from selenium.webdriver.common.action_chains import ActionChains
import sys
db_path = "mysql://shuichi47:V3BtyW&U@172.104.91.29:3306/Line"
url_sql = urlparse(db_path)
conn = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(host = url_sql.hostname, port=url_sql.port, user = url_sql.username, password= url_sql.password, database = url_sql.path[1:]))


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--no-sandbox")
options.add_argument('--user-data-dir=/root/.config/google-chrome/')#user
num = random.choice([100+u for u in range(10000)])
options.add_argument('--profile-directory=Profile ' + str(num))
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
stealth(driver,
vendor="Google Inc.",
platform="Win32",
webgl_vendor="Intel Inc.",
renderer="Intel Iris OpenGL Engine",
fix_hairline=True,
)

word = sys.argv[1]
table = sys.argv[2]

driver.delete_all_cookies()

url = 'https://www.google.com/search?q='+word+'+site%3Ahttp%3A%2F%2Fpage.line.me'
driver.get(url)
try:
    conn.execute('create table '+table+' like beautysaron')
    conn.execute('insert into tables values("'+table+'","'+word+'") ')
except:
    print('already')


conn.execute('delete from '+table)

while True:
    time.sleep(3)
    for i in range(20):
        xpath = '/html/body/div[7]/div/div[10]/div[1]/div/div[2]/div[2]/div/div/div['+str(i+1)+']/div/div/div[1]'
        try:
            element = driver.find_element_by_xpath(xpath)
            idd = element.find_element_by_tag_name('a').get_attribute('href')
            name = element.find_element_by_tag_name('h3').text
            if len(idd) == 29:
                print(idd[21:],name.split('|')[0][:-1])
                try:
                    letter = 'insert into '+table+' values("'+idd[21:]+'","'+name.split('|')[0][:-1]+'","dummy","dummy","dummy","dummy","dummy","dummy",0)'
                    conn.execute(letter)
                except:
                    pass
        except:
            break
    try:
        driver.find_element_by_id('pnnext').click()
    except:
        break
driver.quit()
