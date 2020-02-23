import re
import requests
from datetime import *
import time
from Crypto.Cipher import DES
import binascii
import logging
import json
import subprocess
import os

class BeanfunLogin(object):

    def __init__(self, account, passwd):

        self.account = account
        self.passwd = passwd
        self.session = requests.Session()
        self.webtoken = None
        self.start = time.time()
        self.skey = None
        self.sacc = None

    def getSessionkey(self):
        logging.info('get Session key')

        url = "https://tw.beanfun.com/beanfun_block/bflogin/default.aspx?service=999999_T0"
        user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        res = self.session.get(url, headers = user_agent)
        uri = res.url
        regex = re.findall("skey=(.*)&display", uri)
        return regex[0]

    def regularLogin(self):
        logging.info('regularLogin')
        url = "https://tw.newlogin.beanfun.com/login/id-pass_form.aspx?skey=" + self.skey
        # user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        res = self.session.get(url)
        res = res.text

        viewstate = re.findall("id=\"__VIEWSTATE\" value=\"(.*)\" />", res)[0]
        eventvalidation = re.findall("id=\"__EVENTVALIDATION\" value=\"(.*)\" />", res)[0]
        viewstateGenerator = re.findall("id=\"__VIEWSTATEGENERATOR\" value=\"(.*)\" />", res)[0]
        samplecaptcha = re.findall("id=\"LBD_VCID_c_login_idpass_form_samplecaptcha\" value=\"(.*)\" />", res)[0]
        payload = {"__EVENTTARGET":"", "__EVENTARGUMENT":"", "__VIEWSTATE":viewstate, "__VIEWSTATEGENERATOR":viewstateGenerator, "__EVENTVALIDATION":eventvalidation, "t_AccountID":self.account, "t_Password":self.passwd, "CodeTextBox":"", "btn_login":"登入", "LBD_VCID_c_login_idpass_form_samplecaptcha":samplecaptcha}
        res = self.session.post("https://tw.newlogin.beanfun.com/login/id-pass_form.aspx?skey=" + self.skey, data = payload)
        akey = re.findall("akey=(.*)", res.url)
        return akey

    def login(self):
        logging.info('login')

        self.skey = self.getSessionkey()
        akey = self.regularLogin()
        payload = {"SessionKey":self.skey, "AuthKey":akey}
        res = self.session.post("https://tw.beanfun.com/beanfun_block/bflogin/return.aspx", data=payload, allow_redirects=False)
        res = self.session.get("https://tw.beanfun.com/"+res.headers["location"])

        self.webtoken = self.session.cookies['bfWebToken']
        return self.webtoken


    def getAccounts(self):
        logging.info('getAccounts')

        self.webtoken = self.login()
        url = "https://tw.beanfun.com/beanfun_block/auth.aspx?channel=game_zone&page_and_query=game_start.aspx%3Fservice_code_and_region%3D600309_A2&web_token=" + self.webtoken
        res = self.session.get(url)
        regex = re.findall("<div id=\"(\\w+)\" sn=\"(\\d+)\" name=\"([^\"]+)\"", res.text)
        sacc = regex[0][0]
        sotp = regex[0][1]
        sname = regex[0][2]
        self.sacc = sacc
        return {"sacc":sacc, "sotp":sotp, "sname":sname}
        
    def getOTP(self):
        logging.info('getOTP')

        acc = self.getAccounts()
        now = datetime.now()
        dt = now.strftime('%Y%m%d%H%M%S')
        url = "https://tw.beanfun.com/beanfun_block/game_zone/game_start_step2.aspx?service_code=600309&service_region=A2&sotp=%s&dt=%s"%(acc['sotp'], dt)
        res = self.session.get(url)

        longPollingKey = re.findall("GetResultByLongPolling&key=(.*)\"", res.text)[0]
        screatetime = re.findall("ServiceAccountCreateTime: \"([^\"]+)\"", res.text)[0]

        url = "https://tw.newlogin.beanfun.com/generic_handlers/get_cookies.ashx"
        res = self.session.get(url)
        secretCode = re.findall("var m_strSecretCode = '(.*)';", res.text)[0]
        
        payload = {"service_code":"600309", "service_region":"A2", "service_account_id":acc['sacc'], "service_sotp":acc['sotp'], "service_display_name":acc['sname'], "service_create_time":screatetime}
        res = self.session.post("https://tw.beanfun.com/beanfun_block/generic_handlers/record_service_start.ashx", data=payload)
        dt = "%s.%d"%(datetime.now().strftime("%Y%m%d%H%M%S"), int(datetime.now().microsecond/1000))
        res = self.session.get("https://tw.beanfun.com/generic_handlers/get_result.ashx?meth=GetResultByLongPolling&key=" + longPollingKey + "&_=" + dt)

        end = time.time() - self.start
        end = int(end*1000)
        
        params = {"SN":longPollingKey, "WebToken":self.webtoken, "SecretCode":secretCode, "ppppp":"1F552AEAFF976018F942B13690C990F60ED01510DDF89165F1658CCE7BC21DBA",
        "ServiceCode":"600309", "ServiceRegion":"A2", "ServiceAccount":acc['sacc'], "CreateTime":screatetime.replace(" ", "%20"), "d":end}
        url = "http://tw.beanfun.com/beanfun_block/generic_handlers/get_webstart_otp.ashx?SN=" + str(longPollingKey) + "&WebToken=" + str(self.webtoken) + "&SecretCode=" + str(secretCode) + "&ppppp=1F552AEAFF976018F942B13690C990F60ED01510DDF89165F1658CCE7BC21DBA&ServiceCode=600309&ServiceRegion=A2&ServiceAccount=" + str(acc['sacc']) + "&CreateTime=" + str(screatetime.replace(" ", "%20")) + "&d=" + str(end)
        res = self.session.get(url)
        res = res.text[2:]
        key = res[0:8]
        plain = res[8:]
        
        key = bytes(key, encoding = "utf8")
        plain = bytes(plain, encoding = "utf8")

        cipher = DES.new(key, DES.MODE_ECB)

        otp = cipher.decrypt(binascii.a2b_hex(plain))
        otp = otp.decode()
        return otp.strip(b'\x00'.decode())


if __name__ == "__main__":
    
    with open('./accountsInfo.json') as f:
        accountsInfos = json.load(f)

    for account in accountsInfos:
        print(account['user'], account['pass'])
        
        model = BeanfunLogin(account['user'], account['pass'])
        otp = model.getOTP()
        command = 'Client.exe code:1622 ver:298 logip:210.208.80.6 logport:11000 chatip:210.208.80.10 chatport:8004 setting:\"file://data/features.xml=Regular, Taiwan\" /N:%s /V:%s /T:gamania'%(model.sacc, otp)
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        print("end")
        time.sleep(10)