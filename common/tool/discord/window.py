import re

import discord
import win32gui
import win32process
import psutil
from discord.ext import commands
from main import Main


class Window(Main):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    @commands.command()
    async def channelStatus(self, ctx):
        checkList = self.checkChannel()
        embed = discord.Embed(title="在線情況", color=0x3678F1)
        for k,v in enumerate(checkList):
            title = '[CHANNEL%d]'%(k+1)
            value = '<:green_circle:658543856689610753>' if v else '<:red_circle:658543953557061652>' 

            embed.add_field(name=title, value=value, inline=True)
        #TODO 廣告寫到config
        embed.add_field(name='[NNcode]', value='誠收隕星體~~', inline=True)
        await ctx.send(embed=embed)

    def checkChannel(self):
        winList = []
        def get_all_hwnd(hwnd,mouse):
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                clsname = win32gui.GetClassName(hwnd)
                if (clsname == 'Mabinogi'):
                    title = win32gui.GetWindowText(hwnd)

                    tid, pid = win32process.GetWindowThreadProcessId(hwnd)
                    p = psutil.Process(pid)
                    c = p.connections()
                    connectInfo = 'No Connect'
                    if (len(c) > 0):
                        connectInfo = str(c[0].raddr)
                        winList.append(title)
                    print("hwnd:%d, Title:%s, pid:%d, conn:%s"%(hwnd, title, pid, connectInfo))

        win32gui.EnumWindows(get_all_hwnd, 0)
        # print(winList)

        checkList = []
        for i in range(0, 11):
            checkList.append(False)

        for row in winList:
            channel = re.findall('\[CHANNEL[0-9]{1,2}\]', row)[0]
            id = re.findall('[0-9]{1,2}', channel)[0]
            id = int(id)
            if (id >= 0 and id <= 11):
                checkList[id - 1] = True

        return checkList

    #TODO 另外開Tool 的Cog 
    @commands.command()
    async def getemoji(self, ctx, emoji: discord.Emoji):
        print(emoji.id)

def setup(bot):
    print('[INFO] setup <Window>')
    bot.add_cog(Window(bot))
