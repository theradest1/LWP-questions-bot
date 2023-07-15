import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents = intents)
maxQuestionLength = 17
questionsParent = "Questions"
questionsAskID = 1129651287206658070

@bot.event
async def on_ready():
    print('Bot started')

@bot.command()
async def ask(ctx, *args):
    if ctx.channel.id == questionsAskID:
        if len(' '.join(args)) <= maxQuestionLength:
            category = discord.utils.get(ctx.guild.categories, name=questionsParent)
            if not category:
                category = await ctx.guild.create_category(questionsParent)
            newChannel = await ctx.guild.create_text_channel(' '.join(args), category = category)
            
            await ctx.send("Channel created")
            await newChannel.send(ctx.message.author.mention)
            await newChannel.send("Here is your channel to ask your question and get responses. Send the command \"/answered\" in this channel to close this once done.")
        else:
            await ctx.send("Your description is too long, try to shorten it to just a few words (" + str(maxQuestionLength) + " letter maximum).")
    else:
        await ctx.send("Go to #question-bot to create a channel for your question.")
        
@bot.command()
async def answered(ctx):
    category = discord.utils.get(ctx.guild.categories, name=questionsParent)
    if ctx.channel.category == category:
        async for message in ctx.channel.history(limit=1, oldest_first=True):
            first_message = message
            break
        if first_message.content == ctx.message.author.mention or ctx.message.author.guild_permissions.administrator:
            await ctx.send("Closing channel...")
            await asyncio.sleep(1)
            await ctx.channel.delete()
        else:
            await ctx.send("You do not own this question - ask the creator or an admin to get rid of this channel")
    else:
        await ctx.send("This is not a question channel, if you have one, send it there.")

tokenFile = open("token.txt")
content = tokenFile.readlines()
bot.run(content[1])