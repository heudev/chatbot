import discord
from discord.ext import commands
from chat import chatbot
from keep_alive import keep_alive
import requests
import asyncio
import os
import json

r = requests.head(url="https://discord.com/api/v1")
try:
    print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
except:
    print("No rate limit")

# -----------------------------------------

intents = discord.Intents.all()
intents.members = True
intents.presences = True

bot = commands.Bot(
    command_prefix="chatbot.",
    intents=intents,
    case_insensitivity=True,
    description="Developer: @D1STANG3R",
)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Chatting"), status=discord.Status.online)
    print("Connected to bot: {}".format(bot.user.name))
    print("Bot ID: {}".format(bot.user.id))


@bot.command(help=">>ping")
async def ping(ctx):
    await ctx.send(f"Pong! In **{round(bot.latency * 1000)}**ms")


@bot.command(help=">>privatemessage @member yourmessage")
@commands.has_permissions(administrator=True)
async def privatemessage(ctx, member: discord.Member, *, message):
    try:
        await member.send(message)
        await ctx.reply(f"The message has been sent to {member.mention} member")
    except:
        pass


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.listen("on_message")
async def on_message_listen(message):
    if message.author.bot:
        return
    
    # Direct message to a specific channel
    if str(message.channel.id) == str(1090640942685499694): # Source channel
        channel = bot.get_channel(854855502114848790) # Target channel
        if message.attachments:
            if os.path.exists("attachments") != True:
                os.mkdir("attachments")
            for attachment in message.attachments:
                await attachment.save("./attachments/" + attachment.filename)
            for filename in os.listdir("attachments"):
                await channel.send(file=discord.File("attachments/{}".format(filename)))
                os.remove("attachments/{}".format(filename))
        else:
            await channel.send(message.content)
    
    if str(message.channel.id) != str(1090640942685499694):
        with open("config.json", "r") as file:
            data = json.load(file)
            response = data['response']
            if response:
                getmessage = str(message.content).strip().lower()
                response = chatbot(getmessage)
                if response:
                    async with message.channel.typing():
                        await asyncio.sleep(len(response) / 7)
                        await message.reply(response, mention_author=True)
        

@bot.command(help=">>download")
@commands.has_permissions(administrator=True)
async def download(ctx):
    await ctx.send(file=discord.File("conversation.json"))
        

@bot.command(help=">>upload")
@commands.has_permissions(administrator=True)
async def upload(ctx):
    for attachment in ctx.message.attachments:
        if attachment.filename == "conversation.json":
            await attachment.save(attachment.filename) 
            await ctx.reply("File has been updated")
        else:
            await ctx.reply('File name must be "conversation.json"!')
    

@bot.command(help=">>respond")
@commands.has_permissions(administrator=True)
async def respond(ctx):
    with open('config.json', 'r+') as file:
        data = json.load(file)
        response = data['response']
        data['response'] = not response
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

        if data['response']:
            await ctx.reply("Bot will **respond** to messages")
        else:
            await ctx.reply("Bot will **not respond** to messages")


@bot.command(help=f">>status")
async def status(ctx):
    with open('config.json', 'r') as file:
        data = json.load(file)
        await ctx.reply(f"Response: {data['response']}\nCurrent sensitivity: {data['sensitivity']*100}\n")
    

@bot.command(help=f">>sensitivity [0,100]")
@commands.has_permissions(administrator=True)
async def sensitivity(ctx, ratio):
    ratio = float(ratio)
    if ratio >= 0 and ratio <= 100:
        with open('config.json', 'r+') as file:
            data = json.load(file)
            data['sensitivity'] = ratio/100
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            await ctx.reply(f"Sensitive has been set to {data['sensitivity']*100}")


keep_alive()
bot.run("token")