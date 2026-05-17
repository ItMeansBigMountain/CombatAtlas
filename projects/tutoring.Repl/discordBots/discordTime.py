'''
NOTES
log into discord bot
we can control the bot using file.txt


debug NOTES
click on button and it calls the sendMecMessage()
send message function has to be async so that it may send disc.message



How to fix
figure out how to send an async function from a synchronous command without using loops

https://stackoverflow.com/questions/52905284/tkinter-doesnt-want-to-work-when-using-discord-py


we can split the code into two files, have the gui start on the other file, then run the discord bot from the first
'''

from multiprocessing import Process

import json
from tkinter import *
import asyncio
from datetime import datetime
import time
import discord
import pytz
import threading

#import controller
from tkinter import ttk
import os
import sys

import tracemalloc
tracemalloc.start()

import guiRunner



#general setup
f = open('file.txt' , 'r+' , encoding='utf-8')
mecMessage = json.load(f)
f.close()

tz_NY = pytz.timezone('America/Chicago') 
datetime_NY = datetime.now(tz_NY)


client = discord.Client()



@client.event
async def on_ready():
  print("THE BOT IS ONLINE")
  print(client.user)


@client.event
async def on_message(message):
  username = message.author.name


 # if message.author == client.user:
  #  print('\n'+username+'#'+message.author.discriminator+': Today at '+datetime_NY.strftime("%H:%M")+' \n'+message.content)
   # await asyncio.sleep(1)
   # return
  
  if message.content[:6] == './help':
    print("HELP")

 # print('\n'+username+'#'+message.author.discriminator+': Today at '+datetime_NY.strftime("%H:%M")+' \n'+message.content)

  #if message.author == client.user:
   # tester = print('\n'+username+'#'+message.author.discriminator+': Today at '+datetime_NY.strftime("%H:%M")+' \n'+message.content+'\n')
  #else:
  for i in range(0,1):
    if i == 0:
      tester = input('\n'+username+'#'+message.author.discriminator+': Today at '+datetime_NY.strftime("%H:%M")+' \n'+message.content+'\n')
    if i == 1:
      tester = print('\n'+username+'#'+message.author.discriminator+': Today at '+datetime_NY.strftime("%H:%M")+' \n'+message.content+'\n')
  #+'\n'+client.user.name+'#'+client.user.discriminator+': Today at '+datetime_NY.strftime("%H:%M")+'\n')
  await message.channel.send(tester)
  print ("\033[A                             \033[A")


token = ' '
client.run(token)