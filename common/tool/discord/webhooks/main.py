import json
import logging
import os
import time
import requests

from tail import FileReader


class WebhooksBotify(object):
    def __init__(self):
        self.index = 0
        
        logging.basicConfig(level=logging.INFO,format='[%(asctime)s][%(levelname)-4s] %(message)s',
                    datefmt='%m-%d %H:%M:%S', handlers = [logging.FileHandler('webhookslog.log', 'a+', 'utf-8'),])

        with open('./config.json') as f:
            setting = json.load(f)
        
        if (not setting.__contains__('url') or not setting.__contains__('path')):
            input("設定檔錯誤，按任意鍵退出")
            logging.warning("設定檔錯誤")
            exit()

        self.path = setting['path']
        self.url = setting['url']

        if not os.path.exists(self.path):
            input("找不到log，按任意鍵退出")
            logging.warning("找不到log")
            exit()

    def sendhooks(self, msg):
        url = self.url
        data = {}
        data["content"] = msg

        result = requests.post(url,  data=json.dumps(data), headers={"Content-Type": "application/json"})

    def main(self):

        print("開始執行webhooks")
        logging.info("開始執行webhooks")
        reader = FileReader()

        while True:
            try:
                self.index, msg = reader.get_last_line(self.index, self.path)

                if msg is not None:
                    logging.info(msg)
                    self.sendhooks(msg)
                time.sleep(1)
            except IOError as e:
                logging.warning(str(e))
            except Exception as e:
                logging.error(str(e))       

if __name__ == "__main__":

    model = WebhooksBotify()
    model.main()
