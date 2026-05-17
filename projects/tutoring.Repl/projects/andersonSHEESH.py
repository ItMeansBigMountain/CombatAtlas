# TODO LIST:
# SAVAGE QUESTS!!!!
# EVOLVE POKEMON GOTTA CATCH EM ALL!!!!!!!!!!!!!!!!!!!!!!!
# GYM LEADERS!!!!!!!!!!!!!!!!!!!!!!!!!
# GYM LEADERS NEED A SEPERATE FUNCTION!!!!!!!!!
# FIX BUG TO CHECK IF U DED!!!!!!!!!!!!!
# IF U DIE MAKE IT TELEPORT U TO A POKECENTERRRRRR

# MAKE MAX CAUGHT POKEMON 6!!!!!!
# Be able to release / store pokemon
# storing pokemon at pokecenter



# 1 / 4 / 2021
# create gym battle function
# create a simlulation battle function to put into our pokecenter "yesssir option"

#12/28/2020
# some pokemon moves are still OP

# 1 / 5 / 2021
# we need a list that will contain all the gym leader's pokemon
# we need another moves list for the leader's pokemon's moves







# DECISION 4 - WILL BE GYM BATTLE
# DECISION 5 - be able to trade an npc
  # make the npc either buy a pokemon (500 each)
  # trade u a random pokemon (1000)
  # give u a really bad pokemon (free)
# DECISION 6 - random pokemon in battle options (left , right , forward)


# NOTESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
# - pokedex stats smats
  # pokedex_call['abilities']
  # pokedex_call['height']
  # pokedex_call['location_area_encounters']
  # pokedex_call['moves']
  # pokedex_call['species']
  # pokedex_call['weight']
# -- we are now going to call decisions using our decision array index


from random import randint as randy
import time
import sys

# pokedex imports
import requests 
import json

import pprint



AllPokeBalls = [
  ['PokeBalls' , 6],
  ['UltraBalls' , 0],
  ['MasterBalls' , 0],
  100
]

caught_pokemon = []





# ABSTRACTION (ez)
def specific_PokedexGenerator(pokemon):
  pokemon = pokemon.lower()
  pokedex_call = requests.get('https://pokeapi.co/api/v2/pokemon/'+pokemon).json()

  # save pokemon stats
  name = pokedex_call['name']
  health = int(pokedex_call['stats'][0]['base_stat'])
  maxHealth = int(pokedex_call['stats'][0]['base_stat'])

  attack = int(pokedex_call['stats'][1]['base_stat'])
  defence = int(pokedex_call['stats'][2]['base_stat'])

  Poketype = pokedex_call['types'][0]['type']['name']
  moves = []
  moves_url = []
  for x in pokedex_call['moves']:
    moves.append(x['move']['name'])
    moves_url.append(x['move']['url'])
    
  for x in range(0 , 3 , 1):
    #find pokemon's moves
    randomIndex = randy(0 , len(moves) - 1)
    randomMove = moves[randomIndex]
    moveStats = requests.get(moves_url[randomIndex]).json()
    accuracy = moveStats["accuracy"]
    damage_type = moveStats["damage_class"]['name']
    pp = round(attack / 10)

    while damage_type  != "physical" or accuracy == None:
      randomIndex = randy(0 , len(moves) - 1)
      randomMove = moves[randomIndex]
      moveStats = requests.get(moves_url[randomIndex]).json()
      accuracy = moveStats["accuracy"]
      damage_type = moveStats["damage_class"]['name']
    
    damage = round(((accuracy + attack) / health) + randy(1 , defence))

    movesList.append( Attack( randomMove , damage , damage_type , pp , 0 )  )

  movesSet = [movesList[-3] , movesList[-2] , movesList[-1]]

  return Pokemon( name , health ,Poketype , movesSet  , maxHealth , attack , defence)






gymLeaders = {
  "tiny Tim" : {
    "type" :  "Bug",
    'caught_pokemon' : [
      specific_PokedexGenerator('caterpie'),
      specific_PokedexGenerator('weedle'),
      specific_PokedexGenerator('metapod'),
      specific_PokedexGenerator('scyther'),
    ],
  },
  

  "BIG BOB" : {
    "type" :  "Fighting",
    'caught_pokemon' : [],
  },
  

  "Sassy Sally" : {
    "type" :  "Ghost",
    'caught_pokemon' : [],
  },


  "Mr Pickle" : {
    "type" :  "Water",
    'caught_pokemon' : [],
  },
  

  "Mondae Margeret" : {
    "type" :  "Physic",
    'caught_pokemon' : [],
  },


  "Beplit" : {
    "type" :  "Grass",
    'caught_pokemon' : [],
  },


  "Affan The OP" : {
    "type" :  "Electricity",
    'caught_pokemon' : [],
  },


  "Andson of the Smandson" : {
    "type" :  "Fire",
    'caught_pokemon' : [],
  },

}





def gymbattle( leader_name ,  ):
  pass
# gymBattle parameters == ( leader_name , gym leader's current pokemon ,  player's current pokemon , players caught pokemon , iteration )













#INTERNAL POKEDEX (create pokemon gotta catch em allllllll POKEMON!!!!!)
def RANDOM_INTERNALPokeDex(movesList):
  listOfAllPokemonGOTTACATCHEMALL = []
  pokedex_call =  requests.get('https://pokeapi.co/api/v2/pokemon?limit=151').json()

  for x  in pokedex_call['results']:
    listOfAllPokemonGOTTACATCHEMALL.append(x['name'])

  indexedPokemon = randy(0 , len(listOfAllPokemonGOTTACATCHEMALL) -1)
  pokemon = listOfAllPokemonGOTTACATCHEMALL[indexedPokemon]


  pokedex_call = requests.get('https://pokeapi.co/api/v2/pokemon/'+pokemon).json()

  # save pokemon stats
  name = pokedex_call['name']
  health = int(pokedex_call['stats'][0]['base_stat'])
  maxHealth = int(pokedex_call['stats'][0]['base_stat'])

  attack = int(pokedex_call['stats'][1]['base_stat'])
  defence = int(pokedex_call['stats'][2]['base_stat'])

  Poketype = pokedex_call['types'][0]['type']['name']
  moves = []
  moves_url = []
  for x in pokedex_call['moves']:
    moves.append(x['move']['name'])
    moves_url.append(x['move']['url'])
    
  for x in range(0 , 3 , 1):
    #find pokemon's moves
    randomIndex = randy(0 , len(moves) - 1)
    randomMove = moves[randomIndex]
    moveStats = requests.get(moves_url[randomIndex]).json()
    accuracy = moveStats["accuracy"]
    damage_type = moveStats["damage_class"]['name']
    pp = round(attack / 10)

    while damage_type  != "physical" or accuracy == None:
      randomIndex = randy(0 , len(moves) - 1)
      randomMove = moves[randomIndex]
      moveStats = requests.get(moves_url[randomIndex]).json()
      accuracy = moveStats["accuracy"]
      damage_type = moveStats["damage_class"]['name']
    
    damage = round(((accuracy + attack) / health) + randy(1 , defence))

    movesList.append( Attack( randomMove , damage , damage_type , pp , 0 )  )

  movesSet = [movesList[-3] , movesList[-2] , movesList[-1]]

  return Pokemon( name , health ,Poketype , movesSet  , maxHealth , attack , defence)




#USER POKEDEX
def User_PokeDex():
  pokemon = input("Please enter a pokemon that you wanna look up!: ")
  pokemon = pokemon.lower()
  pokedex_call = requests.get('https://pokeapi.co/api/v2/pokemon/'+pokemon).json()

  print()
  for key , value in pokedex_call.items():
    print(key)
  print()
  option = input('please enter a query: ')
  print()

  #cleaning data
  if option == 'moves':
    for x in pokedex_call[option]:
      print(x['move']['name'])
      # pprint.pprint(x['move'])

  elif option == 'stats':
    for x in pokedex_call[option]:
      print(str(x['stat']['name']) ,'--', str(x['base_stat']) )
      
  elif option =="abilities":
    for x in pokedex_call[option]:
      print(x["ability"]["name"])
      ability_desc = requests.get(x["ability"]["url"]).json()
      print(ability_desc['effect_entries'][1]["effect"])
      print()
  else:
    print(pokedex_call[option])



class Pokemon:
  def __init__(self, name, health, pokeType, moves, maxHealth , attack , defence ):
    self.name = name
    self.health = health
    self.pokeType = pokeType
    self.moves = moves
    self.maxHealth = maxHealth
    self.attack = attack
    self.defence = defence

  def chooseAttack(self): 
    print("\nWhich attack would you like to use?  \n")
    count = 1
    for move in self.moves:
      print("press " + str(count) + " to use " + str(move.name) )
      count += 1
    moveChoice = input("Which number move do you want to use?  ")
    if(moveChoice == str(1)):
      return self.moves[0]
    elif(moveChoice == str(2)):
      return self.moves[1]
    elif(moveChoice == str(3)):
      return self.moves[2]
    else:
      print("Please type one of the number options to select your move. ")
      return self.chooseAttack()


class Attack:
  def __init__(self, name, damage, type, pp, heal):
    self.name = name
    self.damage = damage
    self.type = type
    self.pp = pp
    self.heal = heal


def choosePokemon():
  print("Hello this is Professor Oak! You are ten years old so you get to choose a Pokemon! You can choose from: \n")
  count = 1
  for pokemon in pokeList:
    print("Press " + str(count) + " to choose " + pokemon.name)
    count += 1
  pokeChoice = input("Which number pokemon do you want?  ")
  
  if(pokeChoice == str(1)):
    return pokeList[0]
  elif(pokeChoice == str(2)):
    return pokeList[1]
  elif(pokeChoice == str(3)):
    return pokeList[2]
  else:
    print("Please choose one of the number choices")
    return choosePokemon()

def delay_print(s):
  for c in s:
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(0.05)

def pokeCenter( pokemon , pokeBalls , caught_pokemon):
  
  delay_print('\nWelcome to the pokeCenter!!!\n')
  delay_print('\nPokeDollars: ' +'円'+ str(AllPokeBalls[3]))
  delay_print('\nPokeBalls: ' + str(pokeBalls))
  
  delay_print('\n1 - Heal All Pokemon')
  delay_print('\n2 - PokeShop') 
  delay_print('\n3 - Local Battle')
  delay_print('\n4 - Exit\n')
  option = input('Please choose an option: ')
  
  # HEAL ALL POKEMON
  if option == '1':
    # Heal
    for pokemayne in caught_pokemon:
      pokemayne.health = pokemayne.maxHealth
      print ("A nurse has replenished your pokemons health")
      print('{}\'s health is now {} HP '.format(pokemayne.name,pokemayne.health))

  # BUY POKEBALLS
  elif option == '2':
    # pokeShop
    delay_print('\n[1]:  50 - PokeBall')
    delay_print('\n[2]:  100 - UltraBall')
    delay_print('\n[3]:  1000 - MasterBall\n')

    buy = input('Please choose an option (type: no or press enter to exit): ')

    if buy == '1':
      # Pokeball
      how_many = int(input("How many PokeBalls would you like to buy?: "))
      cost = 50 * how_many
      
      if cost <= AllPokeBalls[3]:
        AllPokeBalls[3] -= cost
        AllPokeBalls[0][1] += how_many
        delay_print("\n You purchased " + str(how_many) + ' for 円'+ str(cost) )
        delay_print("\n You have " + '円'+ str(AllPokeBalls[3]) +  ' left')
        time.sleep(1)
      else:
        delay_print("\n\n you do not have enough money broke boi 😭  \n\n")
        print("You have " +'円'+ str(AllPokeBalls[3]) )


    elif buy == '2':
      # UltraBall
      how_many = int(input("How many PokeBalls would you like to buy?: "))
      cost = 100 * how_many
      if cost <= AllPokeBalls[3]:
        AllPokeBalls[3] -= cost
        AllPokeBalls[1][1] += how_many
        delay_print("\n You purchased " + str(how_many) + ' for 円'+ str(cost) )
        delay_print("\n You have " + '円'+ str(AllPokeBalls[3]) +  ' left')
        time.sleep(1)
      else:
        delay_print("\n\n you do not have enough money broke boi 😭  \n\n")
        print("You have " +'円'+ str(AllPokeBalls[3]) )
        

    elif buy == '3':
      # MasterBall
      how_many = int(input("How many PokeBalls would you like to buy?: "))
      cost = 1000 * how_many
      
      if cost <= AllPokeBalls[3]:
        AllPokeBalls[3] -= cost
        AllPokeBalls[2][1] += how_many
        delay_print("\n You purchased " + str(how_many) + ' for 円'+ str(cost) )
        delay_print("\n You have " + '円'+ str(AllPokeBalls[3]) +  ' left')
     
      else:
        delay_print("\n\n you do not have enough money broke boi 😭  \n\n")
        print("You have " +'円'+ str(AllPokeBalls[3]) )

  # LOCAL BATTLE
  elif option == '3':
    delay_print("\nWELCOME TO THE LOCAL BATTLE!!!!!!\nYESIR")

    delay_print("\nBAAAAATTTTTTTLLLLLLLEEEEEEE!!!!!!!!\n\n")

    # player1 = pokemon
    # player2 = choosePokemon()

    player1 = RANDOM_INTERNALPokeDex(movesList)
    player2 = RANDOM_INTERNALPokeDex(movesList)
    
    delay_print("\nPLAYER ONE CHOOSES: {}".format(player1.name)    )
    print('\nATK // {}'.format(player1.attack)  )
    print('DEF // {}'.format(player1.defence) ) 


    delay_print("\nPLAYER TWO CHOOSES: {}".format(player2.name)    )
    print('\nATK // {}'.format(player2.attack)  )
    print('DEF // {}'.format(player2.defence) ) 

    
    Localbattle(  player1 , player2 )

  elif option == '4': #QUIT OPTION
    print("You are exiting the PokemonCenter! Bye!!!")
    return
  

  elif option == 'yesssir': # pokemon simulator
    print("\n\n\ndat")
    pokemonSim = input("Please type in a pokemon name that you want to simulate: ")

    pokemonSim = specific_PokedexGenerator(pokemonSim)

    print(pokemonSim.name)
    print(pokemonSim.health)
    print(pokemonSim.pokeType)
    print(  [i.name for i in pokemonSim.moves]   )
    print(pokemonSim.maxHealth)
    print(pokemonSim.attack)
    print(pokemonSim.defence)

    return
  
  else:
    delay_print('\n INVALID OPTION, LEAVING POKECENTER...\n')



movesList = ['']*999
movesList[0] = Attack("scratch", 10, "normal", 10, 0) #0
movesList[1] = Attack("ember", 30 , "fire", 5, 0) #1
movesList[2] = Attack("slash", 20, "normal", 5, 0) #2
movesList[3] = Attack("bite", 20, "normal", 5, 0) #3
movesList[4] = Attack("ram", 10, "normal", 10, 0) #4
movesList[5] = Attack("razor leaf", 30, "grass", 5, 0) #5
movesList[6] = Attack("bite", 10, "normal", 10, 0) #6
movesList[7] = Attack("tackle", 20, "normal", 5, 0) #7
movesList[8] = Attack("skull bash", 30, "water", 5, 0) #8
movesList[9] = Attack("poison sting", 30, "poison", 5, 0) #9
movesList[10] = Attack("bug bite", 20, "bug", 5, 0) #10
movesList[11] = Attack("gnaw", 20,"normal", 5, 0) #11
movesList[12] = Attack("string shot",30,"bug", 5, 0 ) #12
movesList[13] = Attack("peck",10,"flying", 5, 0 ) #13
movesList[14] = Attack("gust",20,"flying", 5, 0 ) #14
movesList[15] = Attack("quick attack",40,"normal", 5, 0 ) #15
movesList[16] = Attack("bite",10,"normal", 5, 0 ) #16
movesList[17] = Attack("snarl",50,"normal", 5, 0 ) #17
movesList[18] = Attack("fury swipes",10,"normal", 5, 0 ) #18
movesList[19] = Attack("wing attack",20,"flying", 5, 0) #19
movesList[20] = Attack("razor wind",40,"flying", 5, 0) #20
movesList[21] = Attack("bind",10,"normal", 5, 0) #21
movesList[22] = Attack("wrap",40,"normal", 5, 0) #22

def initPokemon():
  pokeList = ['']*3
  pokeList[0] = Pokemon("Charmander", 60,  "fire", [ movesList[0], movesList[1], movesList[2] ] , 60 , 30 , 50 )
  pokeList[1] = Pokemon("Bulbasaur", 60, "grass", [ movesList[3], movesList[4], movesList[5] ] , 60 , 50 , 30)
  pokeList[2] = Pokemon("Squirtle", 60, "water", [ movesList[6], movesList[7], movesList[8] ] , 60 , 50 , 30)
  return pokeList

#return true if the battle is won,  return false if the battle is lost
def battle(currentPokemon, versusPokemon , caught_pokemon , iteration):

  delay_print("\n\nCURRENTLY CAUGHT POKEMON!\n")
  for x in range(len(caught_pokemon)):
    print('{}  //HP: {}'.format( caught_pokemon[x].name , caught_pokemon[x].health))

  if iteration == 0:
    delay_print('\nA wild {} has appeared!'.format(versusPokemon.name))


  delay_print("\n... I CHOOSE YOU {} !!!".format(currentPokemon.name))

  #start the loop here
  while currentPokemon.health > 0 and versusPokemon.health > 0:

    # changing pokemon
    
    print()
    wannaChange = input("Do you want to change your pokemonnnnnnn?? (yes/no)")
    wannaChange = wannaChange.lower()
    if wannaChange == "yes":
      print()
      for x in range( 0 , len(caught_pokemon) , 1):
        print('{} : {}'.format(x , caught_pokemon[x].name ) )
      choose = int(input("Please choose a pokemon"))
      try:
        currentPokemon = caught_pokemon[choose]
        delay_print("\n YOU CHOSE " + str(currentPokemon.name)+ '\n')
      except Exception as e:
        #DEBUGGERRRRRRRRRRyezir
        print(e)
        print("no")

    # catching pokemon
    decision = input("\n\nDo you want to atempt catch this pokemon? (y/n):  ")
    decision = decision.lower()
    #CATCH POKEMON QUESTION YESIR!!!!!
    if decision == 'y' or decision == 'yes' or decision == 'yesir':
      print()
      for x in range(len(AllPokeBalls)):
        print(f' {x} : {AllPokeBalls[x]}')

      try:
        choice = int(input('Please choose a pokeball to use : '))
        # CHOOSE POKEball
        
          #Regular pokeball
        if choice == 0:
          if AllPokeBalls[choice][1] > 0:
            AllPokeBalls[choice][1] -= 1

            delay_print(f'\nYou throw a { AllPokeBalls[choice][0][:-1]  }')

            # BETATESTING!!!!!!!!!!!! OMG WOWOWOWWOWOWOWO
            catchHealthPercentage = versusPokemon.health / versusPokemon.maxHealth
            randomness = randy (0,100)
            catchRate = 100*(1 - catchHealthPercentage)
            ballModifier = 0
            # low hp catch rate = 0.025
            # high hp catch rate = 0.03125
            
            # CHECK IF YOUR RANDOM NUMBER IS HIGH ENOUGH TO CATCH
            if randomness < catchRate + ballModifier:
              delay_print("\nYou caught " + versusPokemon.name + "!")
              caught_pokemon.append(versusPokemon)
              return
              #end the battle
            else:
              delay_print("\nThe " + versusPokemon.name + " broke free!")
              
          else:
            delay_print('\nYOU DONT HAVE ENOUGH POKEBALLS continuing the battle...\n')


          #Ultra pokeball
        elif choice == 1:
          if AllPokeBalls[choice][1] > 0:
            AllPokeBalls[choice][1] -= 1
            delay_print(f'\nYou throw a { AllPokeBalls[choice][0][:-1]  }')
            # HANDLING CATCH
          
            catchHealthPercentage = versusPokemon.health / versusPokemon.maxHealth
            randomness = randy (0,100)
            catchRate = 100*(1 - catchHealthPercentage)
            ballModifier = 30
            
            # CHECK IF YOUR RANDOM NUMBER IS HIGH ENOUGH TO CATCH
            if randomness < catchRate + ballModifier:
              delay_print("\nYou caught " + versusPokemon.name + "!")
              caught_pokemon.append(versusPokemon)
              return
              #end the battle
            else:
              delay_print("\nThe " + versusPokemon.name + " broke free!")

          else:
            delay_print('\nYOU DONT HAVE ENOUGH POKEBALLS continuing the battle...\n')


          #Master pokeball
        elif choice == 2:
          if AllPokeBalls[choice][1] > 0:
            delay_print(f'\nYou throw a { AllPokeBalls[choice][0][:-1]  }')
            # HANDLING CATCH

            catchHealthPercentage = versusPokemon.health / versusPokemon.maxHealth
            randomness = randy (0,100)
            catchRate = 100*(1 - catchHealthPercentage)
            ballModifier = 70
            
            # CHECK IF YOUR RANDOM NUMBER IS HIGH ENOUGH TO CATCH
            if randomness < catchRate + ballModifier:
              delay_print("\nYou caught " + versusPokemon.name + "!\n")
              caught_pokemon.append(versusPokemon)
              return
              #end the battle
            else:
              delay_print("\nThe " + versusPokemon.name + " broke free!")
              
          else:
            delay_print('\nYOU DONT HAVE ENOUGH POKEBALLS continuing the battle...\n')

      except:
        delay_print('\n\nInvalid option, Carrying on with the battle...\n')


    attack = currentPokemon.chooseAttack()

    delay_print('\n {} \nused\n {}\n'.format(currentPokemon.name, attack.name ,"!"))

    time.sleep(1)
    #pokemon logic
    versusPokemon.health = versusPokemon.health - attack.damage

    delay_print('\n {} has {} hp left!'.format(versusPokemon.name , versusPokemon.health) )

    if attack.heal > 0:
        currentPokemon.health = currentPokemon.health + attack.heal
        if(currentPokemon.health > currentPokemon.maxHealth):
            currentPokemon.health = currentPokemon.maxHealth
            delay_print(str(currentPokemon.name) , 'has' , str(currentPokemon.health) + ' hp left!' )
    if versusPokemon.health <= 0:
        delay_print ( '\n' + versusPokemon.name + " fainted!\n")
        return False #WE WIN THE BATTLE!!! Get wrecked u derpy mouse!!!!!

    #versus's turn
    versusAttack = versusPokemon.moves[randy(0,2)] #BUG

    delay_print('\n{}\n used\n {} !\n'.format(versusPokemon.name  , versusAttack.name ))

    time.sleep(1)
    currentPokemon.health = currentPokemon.health - versusAttack.damage
    delay_print('\n {} has {} hp left!'.format(currentPokemon.name , currentPokemon.health) )

    if versusAttack.heal > 0:
        versusPokemon.health = versusPokemon.health + versusAttack.heal
        if(versusPokemon.health > versusPokemon.maxHealth):
            versusPokemon.health = versusPokemon.maxHealth
            delay_print(str(versusPokemon.name) , 'has' , str(versusPokemon.health) + ' hp left!' )


    #WE LOST THE BATTLE
    if(currentPokemon.health <= 0):
        delay_print( "\n{} fainted!\n\n".format(currentPokemon.name))
        #Change pokemon here!!!
        healthyPokemon = 0
        for x in range( 0 , len(caught_pokemon) , 1):
          if caught_pokemon[x].health > 0 :
            healthyPokemon += 1
            print('{} : {}'.format(x , caught_pokemon[x].name ) )
        if healthyPokemon > 0:
          choose = int(input("Please choose a pokemon"))
          try:
            currentPokemon = caught_pokemon[choose]
            delay_print("\n YOU CHOSE " + str(currentPokemon.name)+ '\n')
          except Exception as e:
            #DEBUGGERRRRRRRRRRyezir
            print(e)
            print("no")
          iteration += 1
          battle(currentPokemon , versusPokemon , caught_pokemon , iteration)
        else:
          return True


def Localbattle(PlayerOne_Pokemon, versusPokemon):

  delay_print('\nYou have beeen challenged!!!!!\nYESIRRRRRRR\n'.format(versusPokemon.name))


  #start the loop here
  while PlayerOne_Pokemon.health > 0 and versusPokemon.health > 0:
    
    # NOTE!!!!! PLACE pokemon HERE
    
    
    # PLAYER ONE'S TURN
    #--------------------------------------------------
    attack = PlayerOne_Pokemon.chooseAttack()

    delay_print('\n{} used {}'.format(PlayerOne_Pokemon.name, attack.name ,"!"))

    time.sleep(1)
    #pokemon logic
    versusPokemon.health = versusPokemon.health - attack.damage

    delay_print('\n {} has {} hp left!'.format(versusPokemon.name , versusPokemon.health) )

    if attack.heal > 0:
        PlayerOne_Pokemon.health = PlayerOne_Pokemon.health + attack.heal
        if(PlayerOne_Pokemon.health > PlayerOne_Pokemon.maxHealth):
            PlayerOne_Pokemon.health = PlayerOne_Pokemon.maxHealth
            delay_print(str(PlayerOne_Pokemon.name) , 'has' , str(PlayerOne_Pokemon.health) + ' hp left!' )
    if versusPokemon.health <= 0:
        delay_print (versusPokemon.name + " fainted!\n")
        
        # Payout if player 1 wins
        cashMoneyBankOMG = randy(1 , 20)
        AllPokeBalls[3] += cashMoneyBankOMG
        delay_print("\nYou received 円" + str(cashMoneyBankOMG)) 
        delay_print("\nYou have 円" + str(AllPokeBalls[3])  )
        return True


    #            PLAYER TWO'S TURN
    #-----------------------------------------------------
    versusAttack = versusPokemon.chooseAttack()

    delay_print('\n{}used {} !'.format(versusPokemon.name  , versusAttack.name ))

    time.sleep(1)
    PlayerOne_Pokemon.health = PlayerOne_Pokemon.health - versusAttack.damage
    delay_print('\n {} has {} hp left!'.format(PlayerOne_Pokemon.name , PlayerOne_Pokemon.health) )

    if versusAttack.heal > 0:
        versusPokemon.health = versusPokemon.health + versusAttack.heal
        if(versusPokemon.health > versusPokemon.maxHealth):
            versusPokemon.health = versusPokemon.maxHealth
            delay_print(str(versusPokemon.name) , 'has' , str(versusPokemon.health) + ' hp left!' )
    if(PlayerOne_Pokemon.health <= 0):
        delay_print( "\n{} fainted!\n".format(PlayerOne_Pokemon.name))

        # Money lost if player 1 loses
        cashMoneyBankOMG = randy(1 , 20)
        AllPokeBalls[3] -= cashMoneyBankOMG
        delay_print("\nYou lost  円" + str(cashMoneyBankOMG)) 
        delay_print("\nYou have 円" + str(AllPokeBalls[3]) + ' left...'  )
        return True


        return False



    #-----------------END OF LOCAL BATTLE--------------
    #             STILL UNDA CONSTRUCTSIONESS

def askStart():
  goodChoice = False
  while not goodChoice:
    outsideChoice = input("Do you want to go outside to start your journey(yes/no)?")
    if(outsideChoice == "no"):
      delay_print("\nOK, I'll be waiting here to start your journey.\n")
    elif(outsideChoice == "yes"):
      delay_print("\nOK, let's get started!")
      goodChoice = True
    else:
      delay_print("\nPlease say either \"yes\" or \"no\": ")




#________________MAIN_GAME_________________________
def main():
  # PUT ALL FUNCTIONS INTO ARRAY FOR functionController()
  allDecisions = []
  for x in globals():
    if x.startswith("decision"):
      # print( type( globals()[x]  ) )
      allDecisions.append( globals()[x]  )


  currentPokemon = choosePokemon()
  caught_pokemon.append(currentPokemon)

  death = False

  delay_print("\nYou chose " + currentPokemon.name + " as your pokemon")
  delay_print("\nProffesor Oak gave you 6 PokeBalls and 円100! \n")



  # DECISIONS
  LevelIndex = 0
  while True:
    try:
      LevelIndex = allDecisions[LevelIndex](currentPokemon , LevelIndex)
    except Exception as e:
      # print(e)
      break




# DECISION FUNCTIONS!!!!!!!!!!!!!!!
def decision_One(currentPokemon , LevelIndex):
  death = False
  while death == False:
      # DECISION ONE ----------------------------------------------
      delay_print('\n\nRound 1\n')
      D = input("Do you want to go Left, Right, Forward?: ")

      if D.lower() == 'forward':
        #pokemon encounter Caterpie
        Caterpie = Pokemon("Caterpie", 50 ,"Bug",[movesList[10], movesList[11], movesList[12] ], 50 , 20 , 60)
        death = battle(currentPokemon , Caterpie , caught_pokemon , 0)
        LevelIndex += 1
        break
        

      elif D.lower() == 'right':
        #finding a pokemon center
        delay_print('\n You have found the PokemonCenter!')
        pokeCenter( currentPokemon , AllPokeBalls , caught_pokemon)
       
        
      elif D.lower() == 'left':
        #pokemon encounter Weedle
        weedle = Pokemon("Weedle", 50 ,"Bug",[movesList[9], movesList[10], movesList[11] ], 50 , 30 , 40)
        battle(currentPokemon , weedle , caught_pokemon , 0  )
        LevelIndex += 1
        break

      elif D.lower() == 'pokedex':
        User_PokeDex()
        decision_One(currentPokemon)
  return LevelIndex
    
#YESIRRRRRRR!!!!!!!!!!!
def decision_Two(currentPokemon , LevelIndex):
  while True:
      delay_print('\n\nRound 2\n')
      D = input("Do you want to go Left, Right, Forward?: ")

      if D.lower() == 'forward':
        #pokemon encounter Caterpie
        Pidgey = Pokemon("Pidgey", 50 ,"Flying",[movesList[13], movesList[14], movesList[15] ], 60 , 40 , 60)
        battle(currentPokemon , Pidgey , caught_pokemon , 0)
        LevelIndex += 1
        break
        

      elif D.lower() == 'right':
        #finding a pokemon center
        delay_print('\n You have found the PokemonCenter!')
        pokeCenter(currentPokemon , AllPokeBalls , caught_pokemon)
        

      elif D.lower() == 'left':
        #pokemon encounter Weedle
        Ratatta = Pokemon("Ratatta", 50 ,"Normal",[movesList[16], movesList[17], movesList[18] ], 50 , 30 , 40)
        battle(currentPokemon , Ratatta , caught_pokemon , 0)
        LevelIndex += 1
        break

      elif D.lower() == 'pokedex':
        User_PokeDex() 
        decision_Two(currentPokemon)
  return LevelIndex


def decision_Three(currentPokemon , LevelIndex):
  while True:
      delay_print('\n\nRound 3\n')
      D = input("Do you want to go Left, Right, Forward?: ")

      if D.lower() == 'right':
        #pokemon encounter Spearow
        Spearow = Pokemon("Spearow", 60 ,"Flying",[movesList[13], movesList[19], movesList[20] ], 60 , 40 , 60)
        battle(currentPokemon , Spearow , caught_pokemon , 0)
        LevelIndex += 1
        break
        

      elif D.lower() == 'forward':
        #finding a pokemon center
        delay_print('\n You have found the PokemonCenter!')
        pokeCenter(currentPokemon , AllPokeBalls , caught_pokemon)
        

      elif D.lower() == 'left':
        #pokemon encounter Ekans
        Ekans = Pokemon("Ekans", 40 ,"Poison",[movesList[9], movesList[21], movesList[22] ], 40 , 50 , 40)
        battle(currentPokemon , Ekans , caught_pokemon , 0)
        LevelIndex += 1
        break

      elif D.lower() == 'pokedex':
        User_PokeDex() 
        decision_Two(currentPokemon)
  return LevelIndex




def decision_Four(currentPokemon , LevelIndex):

  delay_print('\n\nGYM BATTLE!!\n')


  return LevelIndex + 1





#_________________________________________________



#THIS IS WHERE THE CODE GETS IMPORTANTE SO NO TOCHIES PEEPS!!!!!!       
# Initialization
pokeList = initPokemon()
#THIS IS THE MAIN GAME!!!!!!
main()
delay_print("\n YOU CAUGHT THESE POKEMON DURING YOUR JOURNEY\n")
for pokemon in caught_pokemon:
  delay_print(pokemon.name)
  print()

