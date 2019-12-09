import sys
import time
import  os
import bossNotify
import json
import re

already_print_num = 0

def get_last_line(filepath):
    global already_print_num
    if not os.path.exists(filepath):
        print ('no such file %s' % filepath)
        sys.exit()
        return
    readfile = open(filepath, 'r',encoding = 'utf16')
    lines = readfile.readlines()
    if len(lines) > 1 and already_print_num == 0:
        #首次输出最多输出 n 行
        already_print_num = len(lines) - 1#n = 1

    if already_print_num < len(lines):
        print_lines = lines[already_print_num - len(lines):]

        with open('../../config/lineNotifyToken.json') as f:
            token = json.load(f)

        for line in print_lines:
            #notify 
            msg = line.replace('\n','')
            if re.search('出現了', msg):
                msg = msg[msg.find('[CHANNEL'):len(msg)]# 字串處理
                bossNotify.lineNotifyMessage(token['token'], msg)
            print(msg)            
        already_print_num = len(lines)
    readfile.close()

def timer(filename):
    while True:
        try:
            get_last_line(filename)
            time.sleep(1)
        except Exception as e:
            print('[Error] '+ str(e))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = "C:\\Nexon\\Mabinogi\\Tin_log.txt"
        # print('illegal params')
    else:
        filename = sys.argv[1]
    timer(filename)