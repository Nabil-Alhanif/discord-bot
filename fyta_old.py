import discord
from discord.ext import commands
from discord.ext.commands import Bot
from gtts import gTTS
from io import BytesIO

client = discord.Client()

fyta_token = open('token.txt').read()

bot = commands.Bot(command_prefix = '|')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    mention = client.user.mentioned_in(message)

    owner_call = str(message.author) == "Nabil_Alhanif#2451"

    if mention and owner_call:
        voice_state = message.author.voice
        if voice_state is None:
            await message.channel.send("You must join a voice channel before pinging me")
        else:
            if message.content.lower().startswith("join"):
                await message.channel.send("Oke Nabil, aku masuk ke voice channel nya sekarang ya...")
                voice_channel = message.author.voice_channel
                await client.join_voice_channel(voice_channel)
            elif message.content.lower().startswith("leave"):
                await message.channel.send("Oke Nabil, aku bakal leabe dari voice channel nya sekarang...")
                await message.
            await message.channel.send("You mentioned me")

@client.command(pass_context = True)
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command
async def leave(ctx):
    await ctx.voice_channel.disconnect()

client.run(fyta_token)
