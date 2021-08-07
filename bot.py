import discord

import secret

from discord.ext import commands

client = commands.Bot(command_prefix = '²')

@client.event
async def on_ready():
	print('Bot ready')


client.run(secret.token)