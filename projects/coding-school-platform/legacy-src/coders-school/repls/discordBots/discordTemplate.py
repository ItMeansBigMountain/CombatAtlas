#Discord BOT
#what are some ideas that the bot can do?

# Generate sentences saying like new videos and stuff and music

#a bot that reports admins people to ban from the discord server

import discord.py

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('your token here')