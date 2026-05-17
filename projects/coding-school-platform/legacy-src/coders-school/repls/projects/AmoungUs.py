#create a class for crewmates.  The class should have the color, the rooms there are incomplete tasks in, if the crewmate is alive, and if they are in the middle of doing a task.

import random
import time

def checkCanKill():
  canKill = bool(random.getrandbits(1))
  return canKill
  
#A function that asks 
def moveRoom():
  if checkCanKill():
    chooseKill = input("""You see one person in this room.
    Would you like to kill them?
    1 - kill
    2 - don't kill\n""")

    #choosing to kill the player in the room... 
    if (chooseKill == "1"):
      #put in the code to kill here
      print("You chose to kill")

      caught = random.randint(0,100)
      print("\nChance : " + str(14) + "%" )
      if caught > 55 :
        print("YOU GOT CAUGHT")
        exit()
      else:
        print("\nYOU GOT AWAY WITH murder!\n")
    
  else:
    print("\n There was no one in the room, please choose another room...\n")

  roomChoice = input("""Which room would you like to choose?(Press the number)
  1 - weapons
  2 - shields
  3 - admin
  4 - medbay
  5 - electrical
  6 - reactor
  7 - O2
  8 - communications
  9 - security
  10 - upper engines
  11 - lower engines
  12 - cafeteria
  13 - navigation
  14 - storage\n""")
  if(roomChoice == "1"):
    #move to weapons
    playerRoom = 1
    print("You moved to weapons")
  elif(roomChoice == "2"):
    #move to shields
    playerRoom = 2
    print("You moved to shields")
  elif(roomChoice == "3"):
    #move to admin
    playerRoom = 3
    print("You moved to admin")
  elif(roomChoice == "4"):
    #move to medbay
    playerRoom = 4
    print("You moved to medbay")
  elif(roomChoice == "5"):
    #move to electrical
    playerRoom = 5
    print("You moved to electrical")
  elif(roomChoice == "6"):
    #move to reactor
    playerRoom = 6
    print("You moved to reactor")
  elif(roomChoice == "7"):
    #move to O2
    playerRoom = 7
    print("You moved to O2")
  elif(roomChoice == "8"):
    #move to communications
    playerRoom = 8
    print("You moved to communications")
  elif(roomChoice == "9"):
    #move to security
    playerRoom = 9
    print("You moved to security")
  elif(roomChoice == "10"):
    #move to upper engines
    playerRoom = 10
    print("You moved to upper engines")
  elif(roomChoice == "11"):
    #move to lower engines
    playerRoom = 11
    print("You moved to lower engines")
  elif(roomChoice == "12"):
    #move to cafeteria
    playerRoom = 12
    print("You moved to cafeteria")
  elif(roomChoice == "13"):
    #move to navigation
    playerRoom = 13
    print("You moved to navigation")
  elif(roomChoice == "14"):
    #move to storage
    playerRoom = 14
    print("You moved to storage")
  else:
    print("\nPlease type one of the given numbers to move")
    moveRoom()

print('WELCOME TO AMONG US')
roomList = ["weapons", "shields", "admin", "medbay", "electrical", "reactor", "O2", "communications", "security", "upper engine", "lower engine", "cafeteria", "navigation", "storage"]
playerRoom = 12

#game cycle starts here
while(True):
  moveRoom()
