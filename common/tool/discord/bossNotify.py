import discord
from discord.ext import commands
from main import Main
import asyncio
import os
import sys
import json
import re

class BossNotify(Main):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open('D:\\NNcode\\mabinogi-helper\\common\\config\\discordToken.json') as f:
            setting = json.load(f)
        self.bwChannel = setting['bwChannel']
        self.dgChannel = setting['dgChannel']

        self.already_print_num = 0

        async def sendMsg(msg):
            self.channel = self.bot.get_channel(634646567655047178)
            await self.channel.send(msg)

        async def notify():
            await self.bot.wait_until_ready()
            await sendMsg("[INFO] Start Task")
            print("[INFO] Start Task")
            self.channel = self.bot.get_channel(self.dgChannel) # default DG
            while not self.bot.is_closed():
                msg = self.get_last_line()
                if (msg is not None):
                    await self.channel.send(msg)
                await asyncio.sleep(2)
            print('[INFO] bot is close')
        try:
            self.bg_task = self.bot.loop.create_task(notify())

        except IOError as e:
            # sendMsg('[Error] '+ str(e))
            print('[Error] '+ str(e))
        except Exception as e:
            # sendMsg('[Error] '+ str(e))
            print('[Error] '+ str(e))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} ms')

    def get_last_line(self, filepath = None):
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
            print(msg)
            self.already_print_num = self.already_print_num + 1

        readfile.close()
        return bossMsg

def setup(bot):
    print('[INFO] setup <BossNotify>')
    bot.add_cog(BossNotify(bot))