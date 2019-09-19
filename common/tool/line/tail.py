import sys
import time
import  os
import bossNotify
import json

already_print_num = 0
notify_token = 'GHPM2e20SaEhBf6NJkqRtJMZzARrj7WHuaLMHFf87XJ'

def get_last_line(filepath):
    '''
    获取未输入的行
    '''
    global already_print_num
    global notify_token
    if not os.path.exists(filepath):
        print ('no such file %s' % filepath)
        sys.exit()
        return
    readfile = open(filepath, 'r')
    lines = readfile.readlines()
    if len(lines) > 1 and already_print_num == 0:
        #last_num = 20  #首次输出最多输出20行
        already_print_num = len(lines) - 1

    if already_print_num < len(lines):
        print_lines = lines[already_print_num - len(lines):]

        with open('../../config/lineNotifyToken.json') as f:
            token = json.load(f)

        for line in print_lines:
            #notify 
            bossNotify.lineNotifyMessage(token['token'], line.replace('\n',''))
            print(line.replace('\n',''))
            # print len(lines), already_print_num, line.replace('\n','')
        already_print_num = len(lines)
    readfile.close()

def timer(filename):
    '''
    每隔1秒执行一次
    '''
    while True:
        get_last_line(filename)
        time.sleep(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('illegal params')
    else:
        filename = sys.argv[1]
        timer(filename)