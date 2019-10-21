import discord
from discord.ext import commands
import os
import json
# from bossNotify import BossNotify

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

if __name__ == "__main__":
    bot.run(bot_token)

