import discord
from discord.ext import commands
import pandas as pd
client = discord.Client()





#IP GEOLOCATION
import requests #lets us request a http response
import json #convert response strings into progromatic data





TOKEN = ''
geoloaction_jey = ""


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return


    #!hello or !Hello
    if message.content.startswith('!hello') or message.content.startswith('!Hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    #!help
    if message.content.startswith('!help') or message.content.startswith('!Help'):
        msg = "```bash\n You'll want to use the '!' and then say the command.\n"  "Our commands at the moment are: \n" "!Hello \n!Locate <IpAddress> \n!Clear <amount> \n\n!Game <Option>\n**OPTIONS**\n0 - Snake\n1- 2D Platformer```".format(message)
        await message.channel.send(msg)

    #!Locate
    if message.content.startswith('!locate') or message.content.startswith('!Locate'):
    
      ipAddress = message.content[8:]

      #looking for ip ipAddress
      Request = requests.get('https://api.ipgeolocation.io/{geoloaction_jey}&ip='+ ipAddress +'&fields=city&output=json')

      #this line will turn data requested from the website url in line above into a dictionary
      sample = json.loads(Request.text)
      
      #messaging players
      msg = "{} ".format( sample["city"] )
      await message.channel.send(msg)
      # Add IP after !Locate

    # !clear <amount>
    if message.content.startswith('!clear') or message.content.startswith('!Clear') :

        try:
            amount = int(message.content[7:])
            print("Clearing {} Messages...".format(amount) )
            await message.channel.send("Clearing {} Messages".format(amount))
            await message.channel.purge(limit = amount)

        except Exception as e:
            print(e)
            await message.channel.send('ERROR: Learn how to use me you sad nerd...look everyone {} is a SAD NERD'.format(message.author) )

    # GAMES <index>
    if message.content.startswith('!game') or message.content.startswith('!Games') :
      gameName = [
        'Snake',
        '2D platformer',

      ]

      gameLinks = [
        'https://repl.it/@BrainDeadCode_B/Snake-Game-in-Python#main.py',
        'https://thepixiboiii-2d-platformer-game--saintpal.repl.co/',
      ]



      try:
        index = int(message.content[5:])
        await message.channel.send(gameName[index])
        await message.channel.send(gameLinks[index])
      
      except:
        await message.channel.send('INVALID GAME OPTION please use numbers...')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
