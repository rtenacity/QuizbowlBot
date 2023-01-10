import qbreader
import bot_function
import discord
from discord.ext import commands
user_dict = {}

intents = discord.Intents.default()
intents.message_content = True

with open('token.txt','r') as f: #reading token from file
    token = f.read()

client = commands.Bot(command_prefix = ".", intents=intents, help_command=None)

@client.event
async def on_ready():

    await client.change_presence(activity=discord.Game('.help'))
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

@client.command()
async def help(ctx):
    embed=discord.Embed(title=".help Menu", color=0x0062ff)
    embed.add_field(name=".qb", value="Command used to start a session. Takes a difficulty argument and a categories argument.", inline=False)
    embed.add_field(name="Difficulty", value="Used to set the difficulty of the questions. Ex: 1-5, 7, 8-10, etc. Use * for all difficulties.", inline=True)
    embed.add_field(name="Categories", value="Used to set the categories of the questions. Ex: science, history, mythology, etc. USE FULL NAMES FOR CATEGORIES. For a full list of categories, see https://pastebin.com/McVDGDXg.", inline=True)
    embed.add_field(name=".end", value="Ends a session.", inline=False)
    embed.add_field(name=".kill", value="Ends all session(s) forcibly for a user. Used as a hard reset incase of duplicated sessions.", inline=False)
    embed.set_footer(text="created by rtenacity#1388")
    await ctx.send(embed=embed)



@client.command()
async def qb(ctx, *args):
    def check(m: discord.Message): 
        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id 

    if ctx.author.id not in user_dict:
        token = bot_function.generate_token()
        user_dict[ctx.author.id] = {}
        user_dict[ctx.author.id]['score'] = 0
        user_dict[ctx.author.id]['token'] = token
    else:
        await ctx.send("You are already in a game!")
        token = bot_function.generate_token()

    args_list = list(args)
    difficulty_input = bot_function.search_list(args_list)
    try:
        args_list.remove(difficulty_input[0])
    except:
        pass
    category_input = ",".join(args_list)
    run, q = True, 0; 
    difficulty_list, category_list = [], []

    if difficulty_input:
        if difficulty_input == "*":
            difficulty_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        else:
            difficulty_list = bot_function.split_difficulty(difficulty_input[0])

    if category_input:
        category_list = bot_function.split_categories(category_input)
    if token == user_dict[ctx.author.id]['token']:
        while run == True:
            try:

                user_question = bot_function.fetch_question(category_list, difficulty_list); q+=1

                embed_title=discord.Embed(title=user_question['setName'], description=user_question['leadin'], color=0x0062ff)
                embed_title.set_footer(text=f"Requested by {ctx.author} | Difficulty: {user_question['difficulty']} | Category: {user_question['category']}")
                await ctx.send(embed=embed_title)

                for i in range(len(user_question['parts'])):

                    embed_question=discord.Embed(color=0x0062ff)
                    embed_question.add_field(name=str(i+1), value=user_question['parts'][i], inline=False)
                    embed_question.set_footer(text=f"Requested by {ctx.author} | Difficulty: {user_question['difficulty']} | Category: {user_question['category']}")
                    await ctx.send(embed=embed_question)
                    answer = await client.wait_for('message', check = check)

                    if answer.content == ".qb":
                        pass

                    if answer.content == ".end":
                        ppb = user_dict[ctx.author.id]['score'] / q
                        ppb = round(ppb, 2)
                        embed_end=discord.Embed(color=0x0062ff)
                        embed_end.add_field(name="End", value=f"**{ctx.author}** has ended their session with a PPB of {ppb}", inline=False)
                        await ctx.send(embed=embed_end)
                        del user_dict[ctx.author.id]
                        print(user_dict)
                        run = False
                        break

                    if bot_function.is_close_answer(answer.content, user_question['answers'][i]):
                        user_dict[ctx.author.id]['score'] += 10
                        embed_correct=discord.Embed(color=0x4dff00)
                        embed_correct.add_field(name="Correct", value=f"{user_question['answers'][i]}", inline=False)
                        await ctx.send(embed=embed_correct)

                    else:
                        embed_incorrect=discord.Embed(color=0xff0000)
                        embed_incorrect.add_field(name="Were you correct? (y/n)", value=f"{user_question['answers'][i]}", inline=False)
                        await ctx.send(embed=embed_incorrect)
                        unsure = await client.wait_for('message', check = check)

                        if unsure.content == "y":
                            user_dict[ctx.author.id]['score'] += 10

                        elif unsure.content == ".end":
                            ppb = user_dict[ctx.author.id]['score'] / q
                            ppb = round(ppb, 2)
                            embed_end=discord.Embed(color=0x0062ff)
                            embed_end.add_field(name="End", value=f"**{ctx.author}** has ended their session with a PPB of {ppb}", inline=False)
                            await ctx.send(embed=embed_end)
                            del user_dict[ctx.author.id]
                            print(user_dict)
                            run = False
                            break
                        else:
                            pass
                        
            except KeyError:
                del user_dict[ctx.author.id]
                await ctx.send("Invalid Parameters!")
                run = False

@client.command()
async def kill(ctx):
    try:
        del user_dict[ctx.author.id]
        await ctx.send("You have ended your session(s) forcibly.")
    except KeyError:
        await ctx.send(f"<@{ctx.author.id}> has ended their session(s) forcibly.")
client.run(token)


