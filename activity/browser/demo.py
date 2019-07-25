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

    option = webdriver.ChromeOptions()
    option.add_argument('--user-data-dir=../../common/config/google-chrome') #设置成用户自己的数据目录

    # display = Display(visible=0, size=(800, 800))  
    # display.start()

    driver = webdriver.Chrome(executable_path='../../common/tool/driver/chromedriver',chrome_options=option)     # 打开 Chrome 浏览器
    driver.set_window_size(150, 150)
    driver.implicitly_wait(10)

    return driver

def login(driver, accounts):

    driver.get('https://tw.beanfun.com/index.aspx')

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "BF_anchorLoginBtn"))
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

        driver.switch_to.default_content()

        print('[INFO]<%s>login success'%(accounts[0]))

    except TimeoutException:
        print('[FAIL] <%s>login time out'%(accounts[0]))
        return False
    except Exception as e:
        print('[ERROR] <%s>login error:%s'%(accounts[0], str(e)))
        return False

def webStart(driver, accounts, sotp):

    url = 'https://tw.beanfun.com/game_zone/?service_code=600309&service_region=A2&sotp=%d'%(sotp)
    driver.get(url)

    return True

def logout(driver, accounts):
    driver.get('https://tw.beanfun.com/index.aspx')
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "BF_btnLogout"))
        ).click()

        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID,'fbContent'))
        )
        driver.switch_to.frame(iframe)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="divConfirmButton"]/ul/li[1]/a'))
        ).click()

        print('[INFO] <%s> logout success'%(accounts))
        
    except TimeoutException:
        print('[FAIL] <%s>'%(accounts))
        return False
    except Exception as e:
        print('[ERROR] <%s>:%s'%(accounts, str(e)))
        return False

    return True

if __name__ == "__main__":

    with open('/home/rd/Allan/mabinogi-helper/common/config/accountsInfo.json') as f:
        accountsInfos = json.load(f)
    driver = getDriver()
    
    try:
        for item in accountsInfos:
            if (login(driver, [item['user'], item['pass']]) is False):
                driver.close()
                driver = getDriver()
                print("[WARN] 重新登入")
                if (login(driver, [item['user'], item['pass']]) is False):
                    print("[ERROR] 第二次登入失敗")
            webStart(driver, item['user'], item['sotp'])
            input('任意鍵繼續...')
            logout(driver, item['user'])
            
    except Exception as e:
        print(str(e))