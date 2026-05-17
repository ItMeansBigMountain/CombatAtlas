import discord
import requests
import random


client = discord.Client()



def memeGeneration(quote):
    #login
    username = 'TESTREPLIDK'
    password = 'YOUR_IMGFLIP_PASSWORD'

    #fetch all memes
    data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]
    
    
    # print all avail. memes
    # print('\n\nHere is the list of available memes : \n')
    # ctr = 1
    # for img in images:
    #     print(ctr,img['name'])
    #     ctr = ctr+1

    #split discord command into an array
    commands = quote.split()
    text0 = ''
    text1 = ''
    id = random.randint(0,100)

    # choose meme by random
    print('meme id number: {}'.format(id))

    #divide and loop to splitter, start next line's loop from splitter
    splitter = int(len(commands) / 2)   
    # top line
    for i in range(0 , splitter , 1):
        text0 += commands[i] + ' '
    # bottom line
    for x in range(splitter,len(commands) , 1):
        text1 += commands[x] + ' '



    #generated meme
    URL = 'https://api.imgflip.com/caption_image'
    params = {
        'username':username,
        'password':password,
        'template_id':images[id-1]['id'],
        'text0':text0,
        'text1':text1
    }
    response = requests.request('POST',URL,params=params).json()
    print(response)

    imageURL = response['data']['url']
    return imageURL

def memeGeneratiom_CommaSeperation(quote):
    #login
    username = 'TESTREPLIDK'
    password = 'YOUR_IMGFLIP_PASSWORD'

    #fetch all memes
    data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]
    
    
    # print all avail. memes
    # print('\n\nHere is the list of available memes : \n')
    # ctr = 1
    # for img in images:
    #     print(ctr,img['name'])
    #     ctr = ctr+1

    #split discord command into an array
    commands = quote.split(',')
    text0 = ''
    text1 = ''
    id = random.randint(0,100)

    # choose meme by random
    print('meme id number: {}'.format(id))

    #generated meme
    URL = 'https://api.imgflip.com/caption_image'
    params = {
        'username':username,
        'password':password,
        'template_id':images[id-1]['id'],
        'text0':commands[0],
        'text1':commands[1]
    }
    response = requests.request('POST',URL,params=params).json()
    print(response)

    imageURL = response['data']['url']
    return imageURL






#Runs code right when bot begins
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  print('YOU HAVE SUMMONED {}'.format(client))



# checking messages
@client.event
async def on_message(message):
    #if message was from bot, do nothing
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
      await message.channel.send('YOU HAVE SUMMONED SHAWN')

    if message.content.startswith('!meme'):
      try:
        quote = message.content[5:]
        image = memeGeneration(quote)
        await message.channel.send(image)
            
      except Exception as e:
          print(e)
          await message.channel.send(e)
          await message.channel.send(memeGeneration('Learn how to use me, bruh... look everyone {} has committed stupid'.format(str(message.author)[:5])) )

    # MEME GENERATION comma seperation
    if message.content.lower().startswith('!scmeme'): 
        try:
            quote = message.content[7:]
            image = memeGeneratiom_CommaSeperation(quote)
            await message.channel.send(image)

        except Exception as e:
            print(e)
            await message.channel.send(e)
            await message.channel.send(memeGeneration('Learn how to use me, bruh... look everyone {} has commited stupid'.format(str(message.author)[:5])) )



client.run(' ')
