import discord
from ngapain import *

client = discord.Client()

botToken = open("token.txt").read()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        print(message.author)
        print(message.content)
        print(message.channel)
        print(message.guild)

    mention = False
    
    nameTag1 = f'<@!{client.user.id}>'
    nameTag2 = f'<@{client.user.id}>'
    
    if nameTag1 in message.content:
        mention = True
    if nameTag2 in message.content:
        mention = True

    ret = jawab(message, mention)
    if ret != None:
        await message.channel.send(ret)

client.run(botToken)
