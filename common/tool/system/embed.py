import discord

embed=discord.Embed()
embed.add_field(name="[CHANNEL1]", value="SUCCESS", inline=True)

await self.bot.say(embed=embed)