import random


# defining a function!
def favoriteFood():
  name= 'Dev'
  age=8
  print(age)
  print(name)
  food=input('what is your favorite food? ')
  if food == 'hot dogs':
    print("wowowowowow mine too!!!!")
  else:
    print("thats cool.... i like hot dogs ")


def functionTwo():
  dev = 'dev the smartest boy in the world'
  print(dev)



def NumberGuessingGame():

  # generate random number to play with 
  number = random.randint( 1 , 100 )
  guess = input('Guess a number between 1 --> 100? ')
  live = 5
  # check if guess was right loop
  while int(guess) != number and live > 0:
    print("you have " + str(live) + " left...")
    if int(guess) < number:
      live = live - 1 
      print("too low!!!!")
    elif int(guess) > number:
      live = live - 1
      print("too high!!!!")
    guess = input('Guess a number between 1 --> 100? ')
  

  # check if player was out of lives
  if live < 1:
    print("YOU ARE 0UT NUMBERED")
    print(   'the number is ' +  str(number)   )
  else:
    print( "  G00000000D JOB!  "  )





# calling functions down here
NumberGuessingGame()

