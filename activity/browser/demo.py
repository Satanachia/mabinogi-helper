import json
import time
from datetime import date
import psutil
import sys

import requests
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
# from pyvirtualdisplay import Display

windows_count = 0

def getDriver():

    option = webdriver.ChromeOptions()
    option.add_argument('--user-data-dir=D:\\NNcode\\mabinogi-helper\\common\\config\\google-chrome') #设置成用户自己的数据目录
    option.add_argument('lang=zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7')

    # display = Display(visible=0, size=(800, 800))  
    # display.start()

    driver = webdriver.Chrome(executable_path='D:/NNcode/mabinogi-helper/common/tool/driver/chromedriver.exe',chrome_options=option)     # 打开 Chrome 浏览器
    # driver.set_window_size(150, 150)
    driver.implicitly_wait(30)

    return driver

def login(driver, accounts):

    driver.get('https://tw.beanfun.com/game_zone/')

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "BF_anchorLoginBtn"))
        ).click()
        
        iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID,'ifmForm1'))
        )
        driver.switch_to.frame(iframe)

        WebDriverWait(driver, 30).until(
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

    print('[INFO] Start Logout.')
    
    driver.get('https://tw.beanfun.com/game_zone/')
    
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

        # if driver.url is not in 'logout':


        print('[INFO] <%s> logout success'%(accounts))
        
    except TimeoutException:
        print('[FAIL] <%s>'%(accounts))
        return False
    except Exception as e:
        print('[ERROR] <%s>:%s'%(accounts, str(e)))
        return False

    return True

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def findProcessIdByName(processName):
    '''
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    '''
 
    listOfProcessObjects = []
 
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
 
    return listOfProcessObjects

def checkWindows():
    global windows_count
    listOfProcessIds = findProcessIdByName('Client.exe')
    if (len(listOfProcessIds) > windows_count):
        windows_count = len(listOfProcessIds)
        return True
    return False


if __name__ == "__main__":

    accountIndex = 0

    if (len(sys.argv) >= 2):
        accountIndex = int(sys.argv[1]) 

    listOfProcessIds = findProcessIdByName('Client.exe')
    windows_count = len(listOfProcessIds)

    with open('D:/NNcode/mabinogi-helper/common/config/accountsInfo.json') as f:
        accountsInfos = json.load(f)
    driver = getDriver()
    
    try:
        for accountIndex in range(accountIndex, len(accountsInfos)):
            if (login(driver, [accountsInfos[accountIndex]['user'], accountsInfos[accountIndex]['pass']]) is False):
                input('Please Login1')
                if (login(driver, [accountsInfos[accountIndex]['user'], accountsInfos[accountIndex]['pass']]) is False):
                    input('Please Login2')

            webStart(driver, accountsInfos[accountIndex]['user'], accountsInfos[accountIndex]['sotp'])

            timeout = 0
            while checkWindows() is False and timeout < 30:
                time.sleep(1)
                timeout = timeout + 1
            
            if (timeout >= 30):
                print('啟動超時')
                exit()
            
            print('[INFO] 啟動%s成功'%(accountsInfos[accountIndex]['user']))

            logout(driver, accountsInfos[accountIndex]['user'])
            driver.set_window_position(0, 0)
            
    except Exception as e:
        print(str(e))
    
    driver.close()
