import random
from collections import namedtuple
import pprint
import time

def blackjackGame():
  print("Welcome to my table..." )

  # generates a deck of cards
  Card = namedtuple(  'Card'  ,  ['value', 'suit']  )    
  suits = ['hearts', 'diamonds', 'spades', 'clubs']
  cards = [Card(value, suit) for value in range(1, 14) for suit in suits]

  # how many players in the game
  howmany = input("How many players are sitting at the table?: ")
  howmany = int(howmany) # CONVERTING DATA TYPE INTO A NUMBER
  print( str(howmany) + " players are going to play..."  )

  # empty box that will hold all the players later
  players = []

  # for loops are a way to make the computer count numbers
  for counter in range(howmany):
    print("\n" + str(counter)  )
    name = input("NAME: ")
    players.append(   [name , False , 0 , [] , False , False ]   ) 




  # players[0] = # (name , stand , total , cards , blackjack , ace)
  print("Dealer is passing out cards...")
  for roundNumber in range(howmany):
    while players[roundNumber][1] == False:
        randomIndex = random.randint(0 , len(cards) -1 )
        currentPlayer =  players[roundNumber][0]
        givenCard = cards[randomIndex]
        cards.pop(randomIndex)
        if givenCard.value > 10:
            players[roundNumber][2] += 10
        else:
            players[roundNumber][2] += givenCard.value
        players[roundNumber][3].append(   givenCard  )
        
        print(   '\n{} recieved a {}. TOTAL : {} '.format( currentPlayer , givenCard.value , players[roundNumber][2]  )  )
        
        if players[roundNumber][2] >21:
            players[roundNumber][1] = True 
            print("BUST")
        elif players[roundNumber][2] == 21:
            print("BLACKJACK!")
            players[roundNumber][1] = True
            players[roundNumber][3] = True
        else:
            whatsGood = input("PRESS 'H' for hit\nanything else to stand : ")
            if whatsGood.lower().startswith('h'):
                continue
            else:
                players[roundNumber][1] = True


    time.sleep(1)



  # pprint.pprint(cards)







blackjackGame()




# TODO


# once all players stand status are true either by BUST or option, let dealer play her hand (yes the dealer is a woman)

# after dealer plays her hand with casino rules
# CASINO RULES = dealer must hit if below 16 and stand if above 17

# add her info box into the players list

# check to see who won