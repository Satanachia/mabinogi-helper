import json
import time
from datetime import date

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def getDriver():
    driver = webdriver.Chrome(executable_path='../../../common/tool/driver/chromedriver')     # 打开 Chrome 浏览器
    driver.set_window_size(150, 150)
    return driver

def login(driver, accounts):

    driver.get("https://event.beanfun.com/mabinogi/E20190523/index.aspx") 

    driver.find_element_by_id("btnLogin").click()

    try:
        
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID,'ifmForm1'))
        )
        driver.switch_to.frame(iframe)
        driver.find_element_by_id("t_AccountID").send_keys(accounts[0])
        driver.find_element_by_id("t_Password").send_keys(accounts[1])
        driver.find_element_by_id("btn_login").click()
        print ("login success")
    except TimeoutException:
        print('time out')
    finally:
        print('finish')
        #選擇帳號


    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ddl_service_account"))
        )
        select = Select(driver.find_element_by_id('ddl_service_account'))
        select.select_by_index(1)
        driver.find_element_by_id("btn_send_service_account").click()
    except TimeoutException:
        print('time out')

    #plant
    time.sleep(5)

def dothing():
    time.sleep(2)
    return

if __name__ == "__main__":
    
    print("=======================")
    print(date.today())
    with open('../../../common/config/accountsInfo.json') as f:
        accountsInfos = json.load(f)

    for item in accountsInfos:
        driver = getDriver()
        login(driver, [item['user'], item['pass']])
        dothing()
        driver.close()
        print("%s 完成, 骰子数目%d個"%(item['user'], 0))

# */5 * * * *  /usr/bin/python3 /home/rd/Allan/mabinogi-helper/activity/anniversary/14/demo.py >> /home/rd/Allan/mabinogi-helper/log/anniversary/14/dailyLogin.log
