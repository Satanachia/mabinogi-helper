

import datetime
import re

pattern = '\[.*\] +\[.*\]\:(\[CHANNEL([1-9]]|1[0-2]]))'

msg = '[11/30/19 10:43:54] [Tin]:[CHANNEL1] 阿瓦隆遺棄的野營地附近出現了赫朗格尼爾!'

channelMsg = re.findall("(.*)+\[CHANNEL[1-9]{1,2}\]+(.*)", msg)

print(channelMsg)
