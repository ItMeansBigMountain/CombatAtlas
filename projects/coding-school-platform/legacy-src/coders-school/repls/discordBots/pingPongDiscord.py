


import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import discord
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    #if message was from bot, do nothing
    if message.author == client.user:
      return 




      
    if message.content.startswith('p!thwack'):


      await message.channel.send("YIKES!!!that was fast. GG")



    if message.content.startswith('p!ping'):
      
      await message.channel.send("Pong!") 


    if message.content.startswith('p!start'):
      
      await message.channel.send("Game on!")


    if message.content.startswith('p!end'):
      
      await message.channel.send("game ended!")


    if message.content.startswith('p!secret'):
      
      await message.channel.send("Discord Nitro Giveaway! ! https://www.youtube.com/watch?v=dQw4w9WgXcQ")


  
  


client.run(os.environ["PINGPONG_DISCORD_BOT_TOKEN"])