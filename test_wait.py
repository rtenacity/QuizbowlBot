import qbreader
import bot_function
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True


client = commands.Bot(command_prefix = "!", intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('!dankmeme'))
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))


import asyncio
import discord


@client.command()
async def message_check(ctx): # waiting for message here
    await ctx.send(f"**{ctx.author}**, send anything in 60 seconds!")



    msg = await client.wait_for('message', check = check)
    await ctx.send(f"**{ctx.author}**, you responded with {msg.content}!")


client.run("MTA0ODAwMjAzOTM0ODc0NDIxMg.G1oBSe.I8NiiAvm6HH4vxv2PZFO1MnFFPhU8OR3UJDJMY")
#MTA0ODAwMjAzOTM0ODc0NDIxMg.G1oBSe.I8NiiAvm6HH4vxv2PZFO1MnFFPhU8OR3UJDJMY
