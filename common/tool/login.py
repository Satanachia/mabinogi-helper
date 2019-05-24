from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


url = 'https://tw.beanfun.com/index.aspx'
driver = webdriver.Chrome()     # 打开 Chrome 浏览器
driver.get(url) 

