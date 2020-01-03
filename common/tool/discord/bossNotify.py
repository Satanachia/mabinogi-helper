import discord
from discord.ext import commands
from main import Main
import asyncio
import os
import sys
import json
import datetime
from datetime import timedelta
import re

class BossNotify(Main):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = self.bot.get_channel(self.dgChannel) # default DG

        async def sendMsg(msg):
            self.channel = self.bot.get_channel(self.debugChannel)  
            await self.channel.send(msg)

        self.already_print_num = 0
        self.lastMsg = None

        async def notify():
            await self.bot.wait_until_ready()
            await sendMsg("[INFO] Start Task")
            print("[INFO] Start Task")
            while not self.bot.is_closed():
                try:
                    msg = await self.get_last_line()
                except IOError as e:
                    print('[Error] '+ str(e))
                except Exception as e:
                    print('[Error] '+ str(e))

                if (msg is not None and msg != self.lastMsg):
                    self.lastMsg = msg
                    await self.channel.send(msg)
                await asyncio.sleep(2)
            print('[INFO] bot is close')

        self.bg_task = self.bot.loop.create_task(notify(), name='notify')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} ms')

    @commands.command()
    async def cancelTask(self, ctx):
        tasks = asyncio.all_tasks()
        print("[INFO] Task count %d"%(len(tasks)))
        for task in tasks:
            taskName = task.get_name()
            if (taskName == 'notify'):
                task.cancel()
        await ctx.send("[INFO] 關閉所有報線任務, 重啟請下 >reload bossNotify ")

    async def getLastMessage(self, msg):
        #判斷 CHANNEL
        channelMsg = re.findall("\[CHANNEL[1-9]{1,2}\]", msg)[0]
        tailMsg = re.findall("森林巨龍|赫朗格尼爾|黑龍|白龍", msg)[0]

        now = datetime.datetime.utcnow() - timedelta(hours = 1)
        thisHour = now.strftime("%Y-%m-%d %H:%M:%S")
        thisHour = datetime.datetime.strptime(thisHour, '%Y-%m-%d %H:%M:%S')

        # self.channel = self.bot.get_channel(self.debugChannel)
        # TODO after=datetime.datetime
        async for message in self.channel.history(after=thisHour):
            content = message.content
            channelContent = re.findall("\[CHANNEL[1-9]{1,2}\]", content)[0]
            tailContent = re.findall("森林巨龍|赫朗格尼爾|黑龍|白龍", content)[0]
            if (message.author.id == self.botID and channelMsg == channelContent and tailMsg == tailContent):
                # print('[INFO] Try to edit message, id:%d, content:%s, keyword:%s'%(message.id, message.content, msg))
                await message.edit(content='~~%s~~'%(message.content))


    async def get_last_line(self, filepath = None):
        bossMsg = None
        if (filepath is None):
            filepath = "C:\\Nexon\\Mabinogi\\Tin_log.txt"

        if not os.path.exists(filepath):
            print ('[Error] no such file %s' % filepath)
            # await self.channel.send('系統錯誤請聯繫管理員')
            return 
        with open(filepath, 'r', encoding = 'utf16') as readfile:
            lines = readfile.readlines()

        if len(lines) > 1 and self.already_print_num == 0:
            #首次输出最多输出 n 行
            self.already_print_num = len(lines) - 1 #n = 1

        if self.already_print_num < len(lines):
            print_line = lines[self.already_print_num]

            #notify 
            msg = print_line.replace('\n','')
            if re.search('出現了', msg):
                bossMsg = msg[msg.find('[CHANNEL'):len(msg)]# 字串處理

                if re.search('阿瓦隆', msg):
                    self.channel = self.bot.get_channel(self.dgChannel)

                if re.search('白龍', msg) or re.search('黑龍', msg):
                    self.channel = self.bot.get_channel(self.bwChannel)

            if (re.search('消滅了', msg) or re.search('擊退了', msg)):
                if (re.search('赫朗格尼爾', msg) or re.search('森林巨龍', msg)):
                    self.channel = self.bot.get_channel(self.dgChannel)
                    await self.getLastMessage(msg)

                if (re.search('黑龍', msg) or re.search('白龍', msg)):
                    self.channel = self.bot.get_channel(self.bwChannel)
                    await self.getLastMessage(msg)

            print(msg)
            self.already_print_num = self.already_print_num + 1

        readfile.close()
        return bossMsg

def setup(bot):
    print('[INFO] setup <BossNotify>')
    bot.add_cog(BossNotify(bot))