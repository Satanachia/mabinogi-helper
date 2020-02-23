import asyncio
import json
import os
import time

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

with open('D:\\NNcode\\mabinogi-helper\\common\\config\\discordToken.json') as f:
    setting = json.load(f)
bot_token = setting['token']

@bot.event
async def on_ready():
    print("[INFO] Bot is online.")

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'{extension}')
    await ctx.send(f'[INFO] Load {extension} success')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'{extension}')
    await ctx.send(f'[INFO] UnLoad {extension} success')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'{extension}')
    await ctx.send(f'[INFO] ReLoad {extension} success')

# for filename in os.listdir('./'):
#     if filename.endswith('.py'):
#         bot.load_extension(f'cmds.{filename[:-3]}')

bot.load_extension('bossNotify')
bot.load_extension('heartBeat')
bot.load_extension('window')

if __name__ == "__main__":

    retryIndex = 0
    while True:    
        try:
            bot.run(bot_token)
            print("重新連線....")
            time.sleep(5)
        except Exception as e:

            url = 'https://discordapp.com/api/webhooks/679313398957080586/vh2QK-Ka17x6pgNoMqq2O7ffZdTR6aAQ0gA8IYeLDVvc07NwUwZm-AFRRQ5qhdA5It-O'
            data = {}
            data["content"] = '機器人斷線啦~'
            # data["username"] = "custom username"

            result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
            retryIndex = retryIndex + 1
            print('[Error] %s'%(str(e)))
            if (retryIndex > 3):
                break

    url = 'https://discordapp.com/api/webhooks/679313398957080586/vh2QK-Ka17x6pgNoMqq2O7ffZdTR6aAQ0gA8IYeLDVvc07NwUwZm-AFRRQ5qhdA5It-O'
    data = {}
    data["content"] = '機器人斷線啦~~~'
    # data["username"] = "custom username"

    result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})