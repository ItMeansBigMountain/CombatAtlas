import random

def forloop():
  #             (START,END,ITERATION)
  for x in range(0,100,10):
    print (x)


def Yloop():
  #WHILE LOOP
  count = 100
  while count > 0:
    print(count)
    print(random.randint(1,999999999))
    count = count - 1


def infiniteLoop():
  while True:
    print(random.randint(1,999999999))


def mainMenu():
  print('Welcome to the functions app')
  print('1 : forLoop')
  print('2 : WhileLoop')
  print('3 : InfiniteLoop')
  option = int(input('Please choose an option!: '))
  if option == 1:
    forloop()
  if option == 2:
    Yloop()
  if option == 3:
    infiniteLoop()
  mainMenu()
  


#CALLING FUNCTIONS
mainMenu()


#THIS APP CONTAINS
#for loop
#while loop
#infinite loop
#defining functions
#assigned a variable
#if statments