from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import random
import collections
from urllib.parse import urlparse
from sqlalchemy import create_engine
import pandas as pd
import pymysql
from selenium.webdriver.common.action_chains import ActionChains
import sys
import pyautogui as pg
import pyperclip
import requests

pymysql.install_as_MySQLdb()

db_path = "mysql://shuichi47:V3BtyW&U@172.104.91.29:3306/Line"
url_sql = urlparse(db_path)
conn = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(host = url_sql.hostname, port=url_sql.port, user = url_sql.username , password= url_sql.password, database = url_sql.path[1:]))


table = sys.argv[1]

user = sys.argv[2]

prefecture1 = sys.argv[3]

try:
    prefecture2 = sys.argv[4]
except:
    prefecture2 = ''
if prefecture2 == '':
    prefecture = prefecture1
else:
    prefecture = prefecture1 + ' ' + prefecture2

def line(messege_i):
    token = "L0ceBizfHFMWESeszVF8cmtr1fOy1jNww2NA1hFkNJ6"
    url = "https://notify-api.line.me/api/notify"
    headers = {'Authorization': 'Bearer ' + token}
    payload = {'message': messege_i}
    r = requests.post(url, headers=headers, params=payload,)


def send_keys_work(element, string):
    for s in string:
        if s== '5':
            element.send_keys(Keys.NUMPAD5)
        elif s== '6':
            element.send_keys(Keys.NUMPAD6)
        else:
            element.send_keys(s)

def cv(letter):
    time.sleep(1)
    pyperclip.copy(letter)
    pg.keyDown('ctrl')
    pg.press('v')
    pg.keyUp('ctrl')
    time.sleep(1)

df_user = pd.read_sql('select * from user_list where userid = "'+user+'"',conn)
mail = df_user['LINE_ID'][0]
password = df_user['LINE_PASS'][0]
IP = df_user['SERVER_IP'][0]

letter = 'update server set status = "using" where IP = "'+IP+'"'
conn.execute(letter)

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument("--no-sandbox")
options.add_argument('--user-data-dir=/root/.config/google-chrome/')#user
options.add_argument('--profile-directory=Default')
#options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
stealth(driver,
vendor="Google Inc.",
platform="Win32",
webgl_vendor="Intel Inc.",
renderer="Intel Iris OpenGL Engine",
fix_hairline=True,
)



driver.get('chrome-extension://ophjlpahpchlmihnnnihgmmeilfjmjjc/index.html#')
time.sleep(1)
pg.click(200,200)



if prefecture == '全部':
    letter = 'select * from ' + table
    df = pd.read_sql(letter,conn)
    for pre in pre_list:
        try:
            letter = 'insert into stock values("'+user+'","'+table+'","'+pre+'") '
            conn.execute(letter)
        except:
            pass
    try:
        letter = 'create table user_'+user+' like user_sample'
        conn.execute(letter)
    except:
        pass
else:
    letter = 'select * from ' + table + ' where prefecture = "'+prefecture+'" '
    df = pd.read_sql(letter,conn)
    try:
        letter = 'insert into stock values("'+user+'","'+table+'","'+prefecture+'") '
        conn.execute(letter)
    except:
        pass
    try:
        letter = 'create table user_'+user+' like user_sample'
        conn.execute(letter)
    except:
        pass

print(df)

letter = 'select * from user_'+user+' where job = "'+table+'" '
df_my = pd.read_sql(letter,conn)

already = []
for i in range(len(df_my)):
    already.append(df_my['id'][i])

df_t = pd.read_sql('select * from tables where table_name = "'+table+'" ',conn)
jap = df_t['japanese'][0]


WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID,'line_login_email')))
driver.find_element_by_id('line_login_email').clear()
driver.find_element_by_id('line_login_email').click()
element = driver.find_element_by_id('line_login_email')
send_keys_work(element,'')
cv(mail)
driver.find_element_by_id('line_login_pwd').clear()
driver.find_element_by_id('line_login_pwd').click()
element = driver.find_element_by_id('line_login_pwd')
send_keys_work(element,'')
cv(password)

driver.find_element_by_id('login_btn').click()

line(prefecture+'の'+jap+'を追加開始 完了するまでは次の操作を行わないでください')
time.sleep(4)
for i in range(len(df)):
    while True:
        try:
            print('a')
            driver.find_elements_by_css_selector('[title="Add Friends"]')[-1].click()
            break
        except:
            pass
    ID = df['id'][i]
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID,'recommend_search_input')))
    driver.find_element_by_id('recommend_search_input').clear()
    element = driver.find_element_by_id('recommend_search_input')
    send_keys_work(element,'@')
    cv(ID)
    time.sleep(1)
    driver.find_element_by_id('recommend_search_input').send_keys(Keys.ENTER)
    try:
        time.sleep(1)
        store_name = driver.find_element_by_id('recommend_search_result_view').text.split('\n')[0]
        letter = 'update '+table+'  set line_name = "'+store_name+'" where id = "'+ID+'" '
        conn.execute(letter)
        if not ID in already:
            letter = 'insert into user_'+user+' values("'+ID+'","'+table+'",0)'
            conn.execute(letter)
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID,'recommend_add_contact')))
        driver.find_element_by_id('recommend_add_contact').click()
        time.sleep(1)
    except:
        pass
driver.quit()
line(prefecture+'の'+jap+'を追加完了')

letter = 'update server set status = "free" where IP = "'+IP+'"'
conn.execute(letter)
