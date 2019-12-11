import discord
from discord.ext import commands
import asyncio
import json

class Main(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

        with open('D:\\NNcode\\mabinogi-helper\\common\\config\\discordToken.json') as f:
            setting = json.load(f)
        self.bwChannel = setting['bwChannel']
        self.dgChannel = setting['dgChannel']
        self.chatChannel = setting['chatChannel']
        self.debugChannel = setting['debugChannel']
        self.botID = setting['botID']
        self.hasHeartBeat = False
