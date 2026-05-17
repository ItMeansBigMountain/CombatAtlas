#THESE IMPORT MODULES
from twilio.rest import Client #texting
import datetime #knowing what time it is

#log into the text app 
account_sid = 'AC810391b204e797b728828a5406fa26e4'
auth_token = 'f14f764251becbaaf2dfff4ab9b48b70'
client = Client(account_sid, auth_token)


#This will send A pest message
                #pArAmEatEr
def sendtexie( input_message ):
  message = client.messages.create(body= input_message,from_='+12078152450',to='6309232300')

  print(message.body)



body = input("What do you want the message to say?: ")
sendtexie( body )






#this will check what time it is and send a text when its time

while True: #infinity loop 
    now = datetime.datetime.now()

    if now.hour == 16 and now.minute == 7:
        sendtexie()
        break



