from linebot import LineBotApi
from linebot.models import TextSendMessage
import sys
import time
import requests
import json
from model import Boss

notify_token = ''
bot_token = ''

def record():
    model = Boss()
    model.insert()
    print('[INFO] 新增資料成功')

#Line notify
def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code

#Line Bot
def lineThismonthLimit(token):
    headers = {
        "Authorization": "Bearer " + '{'+token+'}', 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    r = requests.get("https://api.line.me/v2/bot/message/quota/consumption", headers = headers)
    return json.loads(r.text)

def main():
    toGroup = sys.argv[1]
    message = ""

    groupID = {
        "none":"none"
    }

    if (toGroup not in groupID or toGroup is None):
        exit()

    #TODO 判斷是否曾經發送


    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    print("[%s][INFO] Send message to group [%s] with message [%s]"%(now, toGroup, message))

    res = lineThismonthLimit(bot_token)

    if (res['totalUsage'] < 450 and False):
        line_bot_api = LineBotApi(bot_token)
        #push message to one user
        line_bot_api.push_message(groupID[toGroup], TextSendMessage(text=message))

    else:
        lineNotifyMessage(notify_token, message)
