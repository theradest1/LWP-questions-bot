import discord
from discord.ext import commands
from discord.ext import tasks

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents = intents)

@bot.event
async def on_ready():
    print('Bot started')

@bot.command()
async def ask(ctx, arg):
    await ctx.send(arg)


tokenFile = open("token.txt")
content = tokenFile.readlines()
bot.run(content[1])