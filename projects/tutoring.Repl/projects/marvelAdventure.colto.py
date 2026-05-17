from random import randint as randy
import time

def initMoves():
  movesList = ['']*9999

 # SPIDERMAN
  movesList[0] = Attack("SPIDER SHOCK", randy( 0 , 80 ), "normal", 0)
  movesList[1] = Attack('WEB CAGE', randy( 0 , 80 ) , "bug", 0)

  #SUPERMAN
  movesList[2] = Attack("LASER EYES", randy( 0 , 80 ), "normal", 0)
  movesList[3] = Attack("SUPER PUNCH", randy( 0 , 80 ), "normal", 0)

  #DOCTOR DOOM
  movesList[4] = Attack("DARK PULSE", randy( 0 , 80 ), "normal", 0)
  movesList[5] = Attack("MAGICAL BEAM", randy( 0 , 80 ), "grass", 0)

  #BATMAN
  movesList[6] = Attack("BAT BLADE", randy( 0 , 80 ), "normal", 0)
  movesList[7] = Attack("NIGHT STRIKE", randy( 0 , 80 ), "normal", 0)

  #ROCET RACOON
  movesList[8] = Attack("UNCONTROLLABLE EXPLOTION", randy( 0 , 80 ), "water", 0)
  movesList[9] = Attack("SHOT GUN", randy( 0 , 80 ), "poison", 0)

  #----------VILLAINS-----------
  #JOKER
  movesList[10] = Attack("UNCONTROLLABLE EXPLOTION", randy( 0 , 30 ), "Fire", 0)
  movesList[11] = Attack("SHOT GUN", randy( 0 , 30 ), "poison", 0)
  movesList[12] = Attack("BAD JOKE", randy( 0 ,32) , "phychic", 0)


  #HARLEY QUINN
  movesList[13] = Attack("HAMMER HEAD", randy(0,50), "Physical", 0)
  movesList[14] = Attack("SOB", randy(0,19), "Phych", 0)
  movesList[15] = Attack("BAD JOKE", randy(0,32), "phychic", 0)


  #TWO FACE
  movesList[16] = Attack("Legal Action", randy(0,100), "Physical", 0)
  movesList[17] = Attack("Paperwork", randy(0,20), "Phych", 0)
  movesList[18] = Attack("Goons", randy(0,50), "group", 0)


  #PENGUIN MAN
  movesList[19] = Attack("Ice ray", randy(0,100), "Physical", 0)
  movesList[20] = Attack("Penguin Peck", randy(0,20), "Phych", 0)
  movesList[21] = Attack("Goons", randy(0,50), "group", 0)


  #GREEN GOBLIN
  movesList[22] = Attack("UNCONTROLLABLE EXPLOTION", randy(0,100), "Fire", 0)
  movesList[23] = Attack("PUMKIN BOMB", randy(0,20), "Phych", 0)
  movesList[24] = Attack("GOONS", randy(0,50), "group", 0)

  return movesList 

class Attack:
  def __init__(self, name, damage, type, heal):
    self.name = name
    self.damage = damage
    self.type = type
    self.heal = heal

class Superhero:
  def __init__(self, name, health, type, moves, maxHealth):
    self.name = name
    self.health = health
    self.type = type
    self.moves = moves
    self.maxHealth = maxHealth
  
  def chooseAttack(self):
    movesList = initMoves()
    print("Which attack would you like to use?  ")
    count=0
    for move in self.moves:
      count+=1
      print("press " + str(count) + " to use " + movesList[move].name)

    moveChoice = input("Which number move do you want to use?  ")
    if(moveChoice == str(1)):
      return movesList[self.moves[0]]
    elif(moveChoice == str(2)):
      return movesList[self.moves[1]]
    elif(moveChoice == str(3)):
      return movesList[self.moves[2]]
    else:
      print("Please type one of the number options to select your move. ")
      return self.chooseAttack()



#battle computer
def battle(versus1 , versus2):
  movesList = initMoves()
  dead = False

  print(versus2.name +' has appeared! You must destroy them.')
  time.sleep(3)
  print('\nATTTTAAAAAACKKKKKKK!!!!!!!\n')

  while versus1.health>0 and versus2.health>0:

    #PLAYER ONE ATTACK
    print('\n{} Please choose attack'.format(versus1.name))
    attack1 = versus1.chooseAttack()
    print('\n You chose {}\n'.format(attack1.name))
    versus2.health -= attack1.damage
    print('you inflicted {} damage to {}'.format(attack1.damage , versus2.name )   )
    print('{} has {} health left.\n'.format(versus2.name , versus2.health ))
    time.sleep(2)


    #PLAYER TWO ATTACK
    print('\n{}\'s turn  to attack! '.format(versus2.name))
    attack2Random = versus2.moves[randy(1 , len(versus2.moves) -1 )]

    attack2 = movesList[attack2Random]

    if versus2.name == 'HARLEY QUINN':
      print('She chose {}'.format(attack2.name))
    
    else:
      print('He chose {}'.format(attack2.name))
    

    versus1.health -= attack2.damage
    print( '{} inflicted {} damage to {}'.format(versus2.name , attack2.damage , versus1.name  )   )
    print('{} has {} health left.\n'.format(versus1.name , versus1.health ))
    time.sleep(2)

  if versus1.health < 0 :
    print('\nYOU DIE!!!!!😵')
    print('{} KILLED YOU!'.format(versus2.name))
    dead = True
    return dead
  
  elif versus2.health < 0 :
    print('\nquangwajolashons!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    dead = False
    return dead

# Local Battle
def LocalBattle(superherosList , player1):
  movesList = initMoves()
  print('\n\nPLAYER TWO')
  print('what superhero do you want to be?')
  print('press 0 for Batman')
  print('press 1 for Spiderman')
  print('press 2 for Super Man')
  print('press 3 for Doctor Doom')
  print('press 4 for Rocket Racoon')

  while True:
    option = input('Please choose a character using the numbers!: ')
    try:
        number = int(option)
        player2 = superherosList[number]
        break
    except:
        print('INVALID OPTION TRY AGAIN')


  print()
  print(player1.name)
  print('VS')
  print(player2.name)
  time.sleep(3)
  print("FIGHT!")

  # this is where the fight begins!
  
  while player1.health>0 and player2.health>0:

    #PLAYER ONE ATTACK
    print('\n\nPLAYER ONE HP: ' + str(player1.health))
    print('\n{} Please choose attack'.format(player1.name))
    attack1 = player1.chooseAttack()
    print('\n You chose {}\n'.format(attack1.name))
    player2.health -= attack1.damage
    print('PLAYER 1 has inflicted {} damage to PLAYER 2 {}'.format(attack1.damage , player2.name )   )
    print('{} has {} health left.\n'.format(player2.name , player2.health ))
    time.sleep(2)


    #PLAYER TWO ATTACK
    print('\n\nPLAYER TWO HP: ' + str(player2.health) )
    print('\n{} Please choose attack'.format(player2.name))
    attack2 = player2.chooseAttack()
    print('\n You chose {}\n'.format(attack1.name))
    player1.health -= attack2.damage
    print('PLAYER 2 inflicted {} damage to PLAYER 1 {}'.format(attack2.damage , player1.name )   )
    print('{} has {} health left.\n'.format(player1.name , player1.health ))
    time.sleep(2)

    # handle death of players
    if player1.health < 0 :
      print('PLAYER 2 WINS!!!!')
    if player2.health < 0 :
          print('PLAYER 1 WINS!!!!')


#STORY MODE P.S Colton was here😃
def storyMode(superherosList , chosenHero):
  print('WELCOME TO THE STORY MODE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

  dead = False

  # BATMANS STORY
  if chosenHero.name == 'BATMAN':
    # Fighting Joker
    print("Batman was running after the Joker!")
    print("he got his crew and robbed the resturaunt")
    print('Robin tracked where Joker\'s hideout is and told batman!')
    print('Batman immediately went over to Joker\'s hideout and confronted him... ')
    time.sleep(7)
    dead = battle(chosenHero, superherosList[5] )
    if dead == True:
      print("GAME OVER")
      return



    # Fighting Harley Quinn
    print("After Batman almost destroyed Joker\'s face, Harley Quinn flew in on her motercycle and slapped Batman in the face!")
    time.sleep(3)
    print("  'NOT MY PUDDIN!!!!\t' - Harley Quinn\n\n ")
    time.sleep(1)
    dead = battle(chosenHero, superherosList[6] )
    if dead == True:
      print("GAME OVER")
      return

    time.sleep(2)
    print("Robin swings in and slaughters both of the Hooligans.")
    print("'That was a little too much dude...' - Batman")
    time.sleep(1)
    print("'YOU CANT HANDLE THE TRUTH' - Robin...")


  # SPIDERMAN'S STORY
  elif chosenHero.name=='SPIDER MAN':
      print(chosenHero.name)
      print("Peter parker was a normal teenager")
      print('one day on a feild trip he got bit by a radioactive spider!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
      print('after some training he faced dun dun dun THE GREEN GOBLIN!!!!!!!!!!!')
      dead = battle(chosenHero, superherosList[9] )
      if dead == True:
        print("GAME OVER")
        return 

 

  elif chosenHero.name=='SUPER MAN':
      print(chosenHero.name)

  elif chosenHero.name=='DOCTER DOOM':
      print(chosenHero.name)

  elif chosenHero.name=='rocket RACOON':
      print(chosenHero.name)

  elif chosenHero.name=='JOKER':
      print(chosenHero.name)

  elif chosenHero.name=='HARLEY QUINN':
      print(chosenHero.name)

  elif chosenHero.name=='Two Faced':
      print(chosenHero.name)

  elif chosenHero.name=='Penguin Man':
      print(chosenHero.name)





'''
STORY MODE NOTES
-Each hero has a different story battles
-unlock characters
'''











def main():

  #choose super hero !
  print('welcome to marvel adventures')

  superherosList=[

  Superhero("BATMAN", 312,  "dark", [6, 7], 312),

  Superhero("SPIDER MAN", 312,  "BUG", [0,1], 312),

  Superhero("SUPER MAN", 312,  "ALIEN", [2,3], 312),

  Superhero("DOCTER DOOM", 312,  "PLASMA", [4,5], 312),

  Superhero("ROCKET RACOON", 312,  "GUN", [8,9], 312),

  #VILLAINS
  
  Superhero("JOKER", 312,  "GUN", [10,11,12], 312),

  Superhero("HARLEY QUINN", 250,  "GUN", [13,14,15], 312),

  Superhero("Two Faced", 300,  "UGLY", [16,17,18], 312),
  
  Superhero("Penguin Man", 300,  "ICE", [19,20,21], 312),

  Superhero("GREEN GOBLIN", 300,  "FIRE", [22,23,24], 312),
 
  ]
  
  
  print('what superhero do you want to be?')
  print('press 0 for Batman')
  print('press 1 for Spiderman')
  print('press 2 for Super Man')
  print('press 3 for Doctor Doom')
  print('press 4 for Rocket Racoon')

  while True:
    option = input('Please choose a character using the numbers!: ')
    try:
        number = int(option)
        chosenHero = superherosList[number]
        break
    except:
        print('INVALID OPTION TRY AGAIN')




  #the adventure begins!
  print('You have chosen '+  str(chosenHero.name ))

  print('1 : fight RANDOM Villain ')
  print('2 : fight Random any dude ')
  print('3 : LOCAL BATTLE!!!!!')
  print('4 : story mode')
  print('5 : Exit the game or else😡')

  option = input('Please chose an option ')

  if option=='1' :
      battle(chosenHero , superherosList[ randy(5 , 8) ] ) 
  elif option=='2':
      battle(chosenHero , superherosList[len(superherosList) - 1] ) 
  elif option == '3':
    LocalBattle(superherosList , chosenHero)
  elif option == '4':
    storyMode( superherosList , chosenHero )
  elif option == '5':
    pass

#calling functions here
main()