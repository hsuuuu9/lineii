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
conn = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(host = url_sql.hostname, port=url_sql.port, user = url_sql.username                                                                                                                                                                                                                                                                               , password= url_sql.password, database = url_sql.path[1:]))

def line(messege_i):
    token = "L0ceBizfHFMWESeszVF8cmtr1fOy1jNww2NA1hFkNJ6"
    url = "https://notify-api.line.me/api/notify"
    headers = {'Authorization': 'Bearer ' + token}
    payload = {'message': messege_i}
    r = requests.post(url, headers=headers, params=payload,)


table = sys.argv[1]

user = sys.argv[2]

prefecture = sys.argv[3]

messege = sys.argv[4]


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
time.sleep(2)
pg.click(200,200)

try:
    letter = 'insert into stock values("'+user+'","'+table+'","'+prefecture+'") '
    conn.execute(letter)
except:
    pass

if prefecture == '全部':
    letter = 'select * from ' + table
else:
    letter = 'select * from ' + table + ' where prefecture = "'+prefecture+'" '
df = pd.read_sql(letter,conn)
letter = 'select * from user_'+user+' where job = "'+table+'"'
my_df = pd.read_sql(letter,conn)

df_t = pd.read_sql('select * from tables where table_name = "'+table+'" ',conn)
jap = df_t['japanese'][0]



my_list = []
for i in range(len(my_df)):
    my_list.append(my_df['id'][i])
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

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'_chat_list_body')))
time.sleep(2)
for i in range(100):
    chats = driver.find_element_by_id('_chat_list_body').find_elements_by_tag_name('li')
    driver.execute_script("arguments[0].scrollIntoView();", chats[-1])

chats_all = driver.find_element_by_id('_chat_list_body').find_elements_by_tag_name('li')
driver.execute_script("arguments[0].scrollIntoView();", chats[0])

line(prefecture+'の'+jap+'に送信開始 完了するまでは次の操作を行わないでください')
for chat in chats_all:
    store_name = chat.get_attribute('title')
    dd = df[df['line_name'] == store_name]
    try:
        pre = dd['prefecture'][dd.index[0]]
        idid = dd['id'][dd.index[0]]
    except:
        pre = 'kkk'
        idid = 'jjj'
    driver.execute_script("arguments[0].scrollIntoView();", chat)
    time.sleep(0.1)
    if idid in my_list:
        chat.click()
        time.sleep(1)
        check = driver.find_elements_by_css_selector('.MdRGT07Cont.mdRGT07Own')
        if len(check) == 0:
            element = driver.find_element_by_id('_chat_room_input')
            element.click()
            cv(messege.replace('{store}',store_name).replace('{place}',pre).replace('{job}',jap))
            actions = ActionChains(driver)
            actions.key_down(Keys.ALT)
            actions.key_down(Keys.ENTER)
            actions.perform()
            now = int(time.time())
            letter = 'update user_'+user+' set send_unix = '+str(now) + ' where id = "'+idid+'" '
            conn.execute(letter)
        else:
            pass
line(prefecture+'の'+jap+'に送信完了')
driver.quit()

letter = 'update server set status = "free" where IP = "'+IP+'"'
conn.execute(letter)
