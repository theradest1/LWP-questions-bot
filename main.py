import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
import openai

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=">>", intents = intents)
maxQuestionLength = 17
questionsParent = "Questions"
questionsAskID = 1129651287206658070

settingsFile = open("gptSettings.txt")
settings = settingsFile.readlines()
gptConversationHistory = []

#try:
#    gptMaxTokens = int(settings[0])
#except:
gptMaxTokens = 50

def resetGPTMem():
    gptConversationHistory = []
    
def setGPTMaxTokens(maxTokens):
    gptMaxTokens = maxTokens

def getGPTAnswer(question):
    #get question along with paster conversation
    #prompt = '\n'.join(gptConversationHistory + [question])
    #print(prompt)
    #print(gptMaxTokens)
    
    #use api
    print(question)
    response = openai.Completion.create(
        engine='gpt-3.5-turbo',  # Specify the engine for ChatGPT (davinci, curie, or babbage)
        prompt=question,  # Your prompt or question
        max_tokens=50,  # Maximum number of tokens in the response
        n=1,  # Number of responses to generate
        stop=None,  # Stop the completion on a specific string (optional)
    )

    #get response
    answer = response.choices[0].text.strip()
    
    #update conversation history
    #gptConversationHistory.append(question)
    #gptConversationHistory.append(answer)
    
    return answer

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
            
            await ctx.send("Channel created: " + newChannel.mention)
            await newChannel.send(ctx.message.author.mention)
            await newChannel.send("Here is your channel to ask your question and get responses. Send the command `>>answered` in this channel to close it.")
        else:
            await ctx.send("Your description is too long, try to shorten it to just a few words (" + str(maxQuestionLength) + " letter maximum).")
    else:
        await ctx.send("Go to #question-bot to create a channel for your question.")
        
@bot.command()
async def answered(ctx):
    questionsParentCatagory = discord.utils.get(ctx.guild.categories, name=questionsParent)
    if ctx.channel.category == questionsParentCatagory and ctx.channel.name != "lwp-questions":
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
        await ctx.send("This is not a question channel, run `>>info` for more info")
        
@bot.command()
async def info(ctx):
    embedVar = discord.Embed(title="How to use LWP Questions bot:", description="", color=0x0047AB)
    embedVar.add_field(name="Directions:", value="Start by running the `>>ask` command with a very quick summary of your question following it. This allows helpers to see what is being asked, and weather or not they have that area of expertise. Ex: `>>ask controller problems`\n\nSomeone will then be able to help you in that channel that has been created to keep questions from overlapping or being forgotten.\n\nAfter your question has been answered, or you just want to get rid of it, run the command `>>answered` inside your channel.\n\nIf you have any questions or problems, ask an admin (:", inline=False)
    embedVar.add_field(name="Create Question:", value="`>>ask *your question*`\nrun this command in <#" + str(questionsAskID) + ">", inline=False)
    embedVar.add_field(name="Close Question:", value="`>>answered`\nrun this command in your question channel", inline=False)
    embedVar.add_field(name="Info:", value="`>>info`\nRun this command anywhere", inline=False)
    await ctx.send(embed=embedVar)
    
@bot.command()
async def gpt(ctx, *args):
    answer = getGPTAnswer(' '.join(args))
    await ctx.send(answer)
    
@bot.command()
async def clearGPT(ctx):
    resetGPTMem()
    await ctx.send("Chat GPT's memory has been cleared")
@bot.command()
async def setGPTTokens(ctx, arg):
    setGPTMaxTokens(int(arg))
    await ctx.send("Chat GPT's max tokens has been set to " + arg)

#starting things
tokenFile = open("token.txt")
content = tokenFile.readlines()
openai.api_key = content[3]
bot.run(content[1])