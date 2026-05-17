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
    players.append(   [name , False , 0 , [] ]   )

  print("Dealer is passing out cards...")
  # Pass around our cards




  print(len(cards))

  for roundNumber in range(howmany):
    currentPlayer = players[roundNumber][0]
    print(   '{}  '.format( currentPlayer )  )

    randomIndex = random.randint(0 , len(cards) -1 )

    players[roundNumber][3].append(  cards[randomIndex]   )

    cards.pop(randomIndex)

    pprint.pprint( players[roundNumber] )
    time.sleep(1)


  print(len(cards))


  pprint.pprint(cards)







blackjackGame()




# TODO
# -give each player a card , add card value to total hg

# -ask each player if they wanna hit or stand
# if they hit, check if they are over 21
  # if they are  = "BUST" & stand = true

# each time they hit, add to their total, check again

# once all players stand status are true either by BUST or option, let dealer play her hand (yes the dealer is a woman)

# after dealer plays her hand with casino rules
# CASINO RULES = dealer must hit if below 16 and stand if above 17

# add her info box into the players list

# check to see who won