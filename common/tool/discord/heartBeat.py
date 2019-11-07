import asyncio

import discord
from discord.ext import commands

from main import Main


class HeartBeat(Main):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def sendMsg(msg):
            self.channel = self.bot.get_channel(self.debugChannel)  
            await self.channel.send(msg)

        async def notifyHeartBeat():
            await self.bot.wait_until_ready()
            await sendMsg("[INFO] Start HeartBeat Task")
            print("[INFO] Start HeartBeat Task")
            self.chatChannel = self.bot.get_channel(self.chatChannel)
            while not self.bot.is_closed():
                await asyncio.sleep(30)
                hasTask = False
                tasks = asyncio.all_tasks()
                # print("[INFO] Task count %d"%(len(tasks)))
                for task in tasks:
                    taskName = task.get_name()
                    if (taskName == 'notify'):
                        hasTask = True
                if (hasTask is False):
                    await self.chatChannel.send("[INFO] 報縣任務已死, 請下 ```>reload bossNotify```")
                    self.heartBeat_task.cancel()
                    self.hasHeartBeat = False

        self.heartBeat_task = self.bot.loop.create_task(notifyHeartBeat(), name='heartBeatTask')
        self.hasHeartBeat = True

    @commands.command()
    async def getTasks(self, ctx):
        hasTask = False
        tasks = asyncio.all_tasks()
        print("[INFO] Task count %d"%(len(tasks)))
        for task in tasks:
            # print(task)
            taskName = task.get_name()
            if (taskName == 'notify' and task.done()):
                await ctx.send("[INFO] 等的就是這個BUG 解決這個就沒問題了 快去叫NN")

            if (taskName == 'notify'):
                hasTask = True
                await ctx.send("[INFO] 我還活著, 真的是Boss還沒出QAQ")
                # break

            if (taskName == 'heartBeatTask'):
                self.hasHeartBeat = True

        if (self.hasHeartBeat is False):
            await ctx.send("[INFO] 守護程序已死, 請下 ``` >reload heartBeat ```")
            
        if (hasTask is False):
            await ctx.send("[INFO] 目前沒有任何任務喔")


def setup(bot):
    print('[INFO] setup <HeartBeat>')
    bot.add_cog(HeartBeat(bot))
