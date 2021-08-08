import discord
from discord.ext import commands

import pickle

import secret
import constants as c



intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '²',intents=intents)
client.remove_command('help')

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

	if reaction.message_id != role_chooser_msg_id:
		return

	emoji_name = reaction.emoji.name

	if emoji_name in c.elements.keys():

		guild = client.get_guild(reaction.guild_id)

		role_name = c.elements[emoji_name]

		role = discord.utils.get(guild.roles,name=role_name)

		await reaction.member.add_roles(role)

		print(f"Added role {role_name} to {reaction.member.name}.")


@client.event
async def on_raw_reaction_remove(reaction):

	if reaction.message_id != role_chooser_msg_id:
		return

	guild = client.get_guild(reaction.guild_id)
	member = guild.get_member(reaction.user_id)

	emoji_name = reaction.emoji.name
	role_name = c.elements[emoji_name]

	if role_name in {role.name for role in member.roles}:

		role = discord.utils.get(member.roles,name=role_name)

		await member.remove_roles(role)

		print(f"Removed role {role_name} to {member.name}.")

@client.command()
async def ping(ctx):
	print("ping")
	await ctx.send('Pong !')

@client.command()
async def kill(ctx):
	await ctx.send('Aaargh !')
	exit()

@client.command()
async def test_de_turing(ctx):
	await ctx.send('https://tenor.com/view/captcha-google-im-not-a-robot-gif-17752213')

@client.command()
async def tell_the_truth(ctx):
	await ctx.send('Les Néons best promo')

@client.command()
async def help(ctx):
	help_message = '''
	**FDV Big Bang Bot** :
	`²deploy_roles` : créé les un rôle pour chacune des 10 promos
	`²delete_roles` : supprime tout les rôles de promos
	`²deploy_chooser_msg` : créé le message avec les réaction pour choisir sa promo
	`²kill` : termine le programme python. A utiliser au cas où le bot se rebelle contre les humains
	`²github` : lien vers le code du bot
	`²test_de_turing` : à utiliser pour vérifier que le bot est bien un robot
	`²tell_the_truth` : la vérité, même si elle est difficile à accepter
	'''
	await ctx.send(help_message)

@client.command(aliases = ['source', 'github', 'code'])
async def code_source(ctx):
	await ctx.send('Mon code se trouve ici : https://github.com/drblobfish/blobfish_discord_bot')

client.run(secret.token)