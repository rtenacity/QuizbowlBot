import qbreader
import bot_function
import discord
from discord.ext import commands
from fuzzywuzzy import fuzz

def is_close(string1, string2, threshold=80):
    distance = fuzz.ratio(string1, string2)
    return distance >= threshold

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix = "!", intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('!dankmeme'))
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))


@client.command()
async def qb(ctx, difficulty_input="", category_input=""):
    def check(m: discord.Message):  # m = discord.Message.
        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id 
    run = True
    difficulty_list = []
    category_list = []
    if difficulty_input:
        if difficulty_input == "*":
            difficulty_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        else:
            difficulty_list = bot_function.split_difficulty(difficulty_input)
    if category_input:
        category_list = bot_function.split_categories(category_input)
    user_question = bot_function.fetch_question(category_list, difficulty_list)
    print(category_list)
    embed_title=discord.Embed(title=user_question['setName'], description=user_question['leadin'], color=0x4dff00)
    await ctx.send(embed=embed_title)
    answer = await client.wait_for('message', check = check)

client.run("MTA0ODAwMjAzOTM0ODc0NDIxMg.G1oBSe.I8NiiAvm6HH4vxv2PZFO1MnFFPhU8OR3UJDJMY")
#MTA0ODAwMjAzOTM0ODc0NDIxMg.G1oBSe.I8NiiAvm6HH4vxv2PZFO1MnFFPhU8OR3UJDJMY

