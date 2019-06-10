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
from pyvirtualdisplay import Display

def getDriver():

    display = Display(visible=0, size=(800, 800))  
    display.start()

    driver = webdriver.Chrome(executable_path='/home/rd/Allan/mabinogi-helper/common/tool/driver/chromedriver')     # 打开 Chrome 浏览器
    driver.set_window_size(150, 150)
    return driver

def login(driver, accounts):

    driver.get("https://event.beanfun.com/mabinogi/E20190523/index.aspx") 

    try:

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btnLogin"))
        ).click()
        
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID,'ifmForm1'))
        )
        driver.switch_to.frame(iframe)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "t_AccountID"))
        )

        driver.find_element_by_id("t_AccountID").send_keys(accounts[0])
        driver.find_element_by_id("t_Password").send_keys(accounts[1])
        driver.find_element_by_id("btn_login").click()
    except TimeoutException:
        print('[FAIL] <%s>login time out'%(accounts[0]))
        return False
    except Exception as e:
        print('[ERROR] <%s>login error:%s'%(accounts[0], str(e)))
        return False

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "ddl_service_account"))
        )
        select = Select(driver.find_element_by_id('ddl_service_account'))
        select.select_by_index(1)
        driver.find_element_by_id("btn_send_service_account").click()
    except TimeoutException:
        print('[FAIL] <%s>select time out'%(accounts[0]))
        return False
    except Exception as e:
        print('[ERROR] <%s>select error:%s'%(accounts[0], str(e)))
        return False

    return True

def dothing(accounts):
    #lbInfoDice
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "lbInfoDice"))
        )
    except TimeoutException:
        print('[FAIL] <%s>get dice time out'%(accounts))
    except:
        print('[ERROR] <%s>get dice error'%(accounts))
    return element.text

if __name__ == "__main__":
    
    print("==============================================")
    print(date.today())
    with open('/home/rd/Allan/mabinogi-helper/common/config/accountsInfo.json') as f:
        accountsInfos = json.load(f)

    try:
        for item in accountsInfos:
            driver = getDriver()
            if (login(driver, [item['user'], item['pass']]) is False):
                driver.close()
                driver = getDriver()
                print("[WARN] 重新登入")
                if (login(driver, [item['user'], item['pass']]) is False):
                    print("[ERROR] 第二次登入失敗")
                    continue
            
            lbInfoDice = dothing(item['user'])
            driver.close()
            print("[INFO] <%s> 完成, 骰子数目%s個"%(item['user'], str(lbInfoDice)))
    except Exception as e:
        print(str(e))


#*/5 * * * *