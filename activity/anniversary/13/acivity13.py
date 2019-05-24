from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()     # 打开 Chrome 浏览器
driver.get("https://event.beanfun.com/mabinogi/E20180517/index.aspx") 


driver.find_element_by_id("i12").click()

try:
    
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,'ifmForm1'))
    )
    driver.switch_to.frame(iframe)
    driver.find_element_by_id("t_AccountID").send_keys("")
    driver.find_element_by_id("t_Password").send_keys("")
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
driver.get("https://event.beanfun.com/mabinogi/E20180517/Potted.aspx")
driver.find_element_by_id("p02").click()

