#This logs into Fortnite
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from fortnite_python import Fortnite
from fortnite_python.domain import Mode , Platform
fortnite = Fortnite(os.environ["FORTNITE_API_KEY"])

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



    #pc
    if message.content.startswith('$pc'):
      playername = str(message.content[3:])
      player = fortnite.player(playername, Platform.PC) 
      stats = player._lifetime

      statKey = []
      statValue = []

      for x in stats:
        print(x['key'])
        print(x['value'])
        print()
        statKey.append(x['key'])
        statValue.append(x['value'])
      
      await message.channel.send(   '{}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n'.format(
        player.username,
        stats[0]['key'],
        stats[0]['value'],
        stats[1]['key'],
        stats[1]['value'],
        stats[2]['key'],
        stats[2]['value'],
        stats[3]['key'],
        stats[3]['value'],
        stats[4]['key'],
        stats[4]['value'],
        stats[5]['key'],
        stats[5]['value'],
        stats[6]['key'],
        stats[6]['value'],
        stats[7]['key'],
        stats[7]['value'],
        stats[8]['key'],
        stats[8]['value'],
        stats[9]['key'],
        stats[9]['value'],
        stats[10]['key'],
        stats[10]['value'],
        stats[11]['key'],
        stats[11] ['value']
      ))




    #xbox
    elif message.content.startswith('$xbox'):
        playername = str(message.content[5:])
        player = fortnite.player(playername, Platform.XBOX)
        stats =  player._lifetime



        await message.channel.send(   '{}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n'.format(
          player.username,
          stats[0]['key'],
          stats[0]['value'],
          stats[1]['key'],
          stats[1]['value'],
          stats[2]['key'],
          stats[2]['value'],
          stats[3]['key'],
          stats[3]['value'],
          stats[4]['key'],
          stats[4]['value'],
          stats[5]['key'],
          stats[5]['value'],
          stats[6]['key'],
          stats[6]['value'],
          stats[7]['key'],
          stats[7]['value'],
          stats[8]['key'],
          stats[8]['value'],
          stats[9]['key'],
          stats[9]['value'],
          stats[10]['key'],
          stats[10]['value'],
          stats[11]['key'],
          stats[11]['value']
        ))




    #playstation
    elif message.content.startswith('$playstation'):
        playername = str(message.content[12:])
        player = fortnite.player(playername, Platform.PSN)
        stats =  player._lifetime



        await message.channel.send( '{}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n'.format(
          player.username,
          stats[0]['key'],
          stats[0]['value'],
          stats[1]['key'],
          stats[1]['value'],
          stats[2]['key'],
          stats[2]['value'],
          stats[3]['key'],
          stats[3]['value'],
          stats[4]['key'],
          stats[4]['value'],
          stats[5]['key'],
          stats[5]['value'],
          stats[6]['key'],
          stats[6]['value'],
          stats[7]['key'],
          stats[7]['value'],
          stats[8]['key'],
          stats[8]['value'],
          stats[9]['key'],
          stats[9]['value'],
          stats[10]['key'],
          stats[10]['value'],
          stats[11]['key'],
          stats[11]['value']
        ))



    #mobile
    elif message.content.startswith('$mobile'):
        playername = str(message.content[12:])
        player = fortnite.player(playername, Platform.TOUCH)
        stats =  player._lifetime



        await message.channel.send( '{}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n'.format(
          player.username,
          stats[0]['key'],
          stats[0]['value'],
          stats[1]['key'],
          stats[1]['value'],
          stats[2]['key'],
          stats[2]['value'],
          stats[3]['key'],
          stats[3]['value'],
          stats[4]['key'],
          stats[4]['value'],
          stats[5]['key'],
          stats[5]['value'],
          stats[6]['key'],
          stats[6]['value'],
          stats[7]['key'],
          stats[7]['value'],
          stats[8]['key'],
          stats[8]['value'],
          stats[9]['key'],
          stats[9]['value'],
          stats[10]['key'],
          stats[10]['value'],
          stats[11]['key'],
          stats[11]['value']
        ))




    #switch
    elif message.content.startswith('$switch'):
        playername = str(message.content[12:])
        player = fortnite.player(playername, Platform.GAMEPAD)
        stats =  player._lifetime



        await message.channel.send( '{}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n{} -> {}\n'.format(
          player.username,
          stats[0]['key'],
          stats[0]['value'],
          stats[1]['key'],
          stats[1]['value'],
          stats[2]['key'],
          stats[2]['value'],
          stats[3]['key'],
          stats[3]['value'],
          stats[4]['key'],
          stats[4]['value'],
          stats[5]['key'],
          stats[5]['value'],
          stats[6]['key'],
          stats[6]['value'],
          stats[7]['key'],
          stats[7]['value'],
          stats[8]['key'],
          stats[8]['value'],
          stats[9]['key'],
          stats[9]['value'],
          stats[10]['key'],
          stats[10]['value'],
          stats[11]['key'],
          stats[11]['value']
        ))







    if message.content.startswith('HELP'):
      
      await message.channel.send("HELP COMMAND\n*spacing and spelling are very important*\n\n\n                fortnite gamestats -- $<platform> <username>  " )





#logs into discord
client.run(os.environ["FORTNITE_DISCORD_BOT_TOKEN"])