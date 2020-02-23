import logging
import os
import re

class FileReader(object):

    def get_last_line(self, already_print_num = 0, filepath = None):
        bossMsg = None

        if (filepath is None):
            filepath = "C:\\Nexon\\Mabinogi\\Tin_log.txt"

        if not os.path.exists(filepath):
            logging.warning('[Error] no such file %s' % filepath)
            return 
        with open(filepath, 'r', encoding = 'utf16') as readfile:
            lines = readfile.readlines()

        readfile.close()

        if len(lines) > 1 and already_print_num == 0:
            #首次输出最多输出 n 行
            already_print_num = len(lines) - 1 #n = 1

        if already_print_num < len(lines):
            print_line = lines[already_print_num]

            #notify 
            msg = print_line.replace('\n','')
            if re.search('出現了', msg):
                bossMsg = msg[msg.find('[CHANNEL'):len(msg)]# 字串處理

            if (re.findall("消滅了|擊退了", msg)):
                bossMsg = msg[msg.find('[CHANNEL'):len(msg)]# 字串處理

            logging.info(bossMsg)
            already_print_num = already_print_num + 1

            return already_print_num, bossMsg

    def main(self):
        index, msg = self.get_last_line()
        print(msg)
