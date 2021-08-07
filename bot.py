import discord
from discord.ext import commands

import pickle

import secret
import constants as c



intents = discord.Intents.default()

client = commands.Bot(command_prefix = '²',intents=intents)


role_chooser_msg_id=0


@client.event
async def on_ready():

	with open('cache.pick','rb') as cache_file:
		global role_chooser_msg_id

		role_chooser_msg_id = pickle.load(cache_file)

	print('Bot ready')

@client.event
async def on_disconnect():
	print('Bot disconnected')

@client.command()
async def deploy_roles(ctx):
	await ctx.message.delete()

	for elem in c.elements.values():
		await ctx.guild.create_role(name=elem)

@client.command()
async def delete_roles(ctx):
	for role in ctx.guild.roles:
		if role.name in c.elements.values():
			await role.delete()

@client.command()
async def deploy_chooser_msg(ctx):
	await ctx.message.delete()

	role_chooser_msg = await ctx.send('Choisissez votre promo en cliquant sur les emotes')

	global role_chooser_msg_id
	role_chooser_msg_id = role_chooser_msg.id

	with open('cache.pick','wb') as cache_file:
		pickle.dump(role_chooser_msg_id,cache_file)
	
	for elem in c.elements.keys():
		await role_chooser_msg.add_reaction(discord.utils.get(ctx.message.guild.emojis,name=elem))


@client.event
async def on_raw_reaction_add(reaction):

	print("")
	print(reaction.message_id)
	print(role_chooser_msg_id)

	if reaction.message_id != role_chooser_msg_id:
		print("someone added a reaction in the wrong place")
		return

	print("someone added a reaction in the right place")
	'''if reaction.emoji == "🏃":
		Role = discord.utils.get(user.server.roles, name="YOUR_ROLE_NAME_HERE")
		await client.add_roles(user, Role)'''


@client.command()
async def ping(ctx):
	print("ping")
	await ctx.send('Pong !')

@client.command(aliases = ['source', 'github', 'code'])
async def code_source(ctx):
	await ctx.send('Mon code se trouve ici : https://github.com/drblobfish/blobfish_discord_bot')

client.run(secret.token)