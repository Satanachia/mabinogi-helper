import discord
from discord.ext import commands
import asyncio
import json
import requests

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

    def sethook(self, text):
        url = 'https://discordapp.com/api/webhooks/678793564028665866/O1DcBj85kxrST1A7XB2UevwUgcKYTowTFJR9nuBxPFtxUiI--x8KkMfOj9LJQGd28h34'

        data = {}
        data["content"] = text
        # data["username"] = "custom username"

        result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})