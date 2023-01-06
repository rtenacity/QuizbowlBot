import discord
from discord.ext import commands
import random
import aiohttp
import praw
import copy
from threading import Timer
import time


intents = discord.Intents.default()
intents.message_content = True


client = commands.Bot(command_prefix = "!", intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('!dankmeme'))
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

@client.command()
async def dankmeme(ctx):
    try:
        if ctx.author not in user_dict:
            user_dict[ctx.author] = copy.copy(all_subs_sort)
        
        name = user_dict[ctx.author][0].title
        url1 = user_dict[ctx.author][0].url

        embed = discord.Embed(
            color = discord.Color.red(),
            title = name,
            url = url1
        )

        embed.set_image(url = url1)
        embed.set_footer(text=f"from r/dankmemes | requested by {ctx.author}")
        await ctx.send(embed = embed)
        user_dict[ctx.author].pop(0)
    except:
        embed1 = discord.Embed(
            color = discord.Color.red(),
            title = "No more memes! Check back later" 
        )
        embed1.set_image(url = "https://media.tenor.com/dahUZmCkbAcAAAAM/agony.gif")
        embed1.set_footer(text=f"No more memes for {ctx.author}. Please check back later")
        await ctx.send(embed = embed1)

                

client.run("MTAzMDUzMzE4OTUwMTk3NjYzNg.G7EgBp.4mDALKKkmJrEGxOaQ8f7XIq6Xp3ZDSnYD9GkHs")