import discord
import os
import time
import requests
import random
from discord.ext import commands
import discord.ext




'''
REMEMBER FOR AFTER PROJECT
#hack using usb (rubber ducky)



NOTES
Track Cursing
Auto Mod
Meme Generator ✓
lvl System
Server Stats
Sentiment
Live Announcements
Tell Joke ✓
Play music from youtube in vc
Purge chat with a limit
Mute
Ban
Temp Ban
Kick
Assign Nickname
Warnings/Infractions
Interactive Role Creation
Ticket Creation System




RULES
create 'elite' role when bot joins server
  only way to use commands admin commands is the elite role






discord objects...
GUILD --> id , name , member - count


'''



# SET UP VARIABLES
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = commands.Bot(command_prefix='.')



elite_role = 'Elite'








# this block checks the user that says something or does something if they have the correct permissions to do so
def check_roles(user , guild):
  for x in range( 0 , len(user.roles)  , 1  ):
    print(  user.roles[x]   )
    if elite_role == user.roles[x].name :
      return True
  return False








# runs code right when the bot starts...
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print( client.guilds[0].members   )
    print('-------------------------------------------')




jokes = ["I'm afraid for the calendar. Its days are numbered.", "My wife said I should do lunges to stay in shape. That would be a big step forward.", "Why do fathers take an extra pair of socks when they go golfing?" "In case they get a hole in one!", "Singing in the shower is fun until you get soap in your mouth. Then it's a soap opera.", "What do a tick and the Eiffel Tower have in common?" "They're both Paris sites.", "What do you call a fish wearing a bowtie?" "Sofishticated.", "How do you follow Will Smith in the snow?" "You follow the fresh prints.", "If April showers bring May flowers, what do May flowers bring?" "Pilgrims.", "I thought the dryer was shrinking my clothes. Turns out it was the refrigerator all along.", ]







# this function runs when someone sends a message!
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # if user has admin commands
    if check_roles(message.author , message.guild):

      if message.content.startswith('.hello'):
        await message.channel.send('Hello!')
        
      if message.content.startswith('server'):
        await message.channel.send(message.guild.name)

      if message.content.startswith('.joke'):
        await message.channel.send(jokes[random.randint(0, len(jokes))])


    # MEME CMD
      if message.content.startswith('.meme'):

      # SPLITS UP THE ARGUMENTS OF THE CMD
        arguments = message.content.split(",")
        first_row = arguments[0].strip(".meme")
        second_row = arguments[1]



        # SENDS MEME TO USER
        output = memeGeneration(first_row  , second_row )
        await message.channel.send( output['data']['url']  )








""""
@client.command()
async def kick(ctx, member : discord.Member, *, reason = None):
  await member.kick(reason = reason)
"""

@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f'User {member} has been kick')









# MEME GENERATION
def memeGeneration(t1 , t2):
  # SETUP VARIABLES
  username = ' '
  password = ' '

  # FETCH TOP 100 MEMES
  data = requests.get( 'https://api.imgflip.com/get_memes' ).json()
  images = [ 
     {
       'name' : image['name'],
       'url' : image['url'],
       'id' : image['id']
     }
     for image in data['data']['memes']
     ]

  # RANDOMLY CHOSEN MEME
  meme =  images[ random.randint(0, 99)]
  
  # POST TO IMGFLIP TO CREATE MEME
  URL = 'https://api.imgflip.com/caption_image'
  params = {
      'username': username,
      'password': password,
      'template_id': meme['id'],
      'text0': t1,
      'text1': t2
  }


  # FINAL OUTPUT
  response = requests.request('POST',URL,params=params).json()

  return response


  
  









client.run(" ")