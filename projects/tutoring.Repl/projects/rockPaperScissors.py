#a list is a variable that stores multiple values
#this is list syntax: listName = [item1, item2, item3]
#item1 = 0, item2 = 1, item3 = 2
import random
options = ["rock", "paper", "scissors"]

print("1 rock")
print("2 paper")
print("3 scissors")
user_input=input("please chose a option: ")

if user_input == '1':
  robot=random.randint(0,2)
  choice=options[robot]
  print('Robot chose: '+ choice)
  
  if choice==options[0]: #rock
    print("TIE GAME")

  if choice==options[1]: #paper
    print("you lose")

  if choice==options[2]: #scissors
    print("YOU WIN!!!!!!")


if user_input == '2':
  robot=random.randint(0,2)
  choice=options[robot]
  print('Robot chose: '+ choice)
  
  if choice==options[0]: #rock
    print("YOU WIN!!!!!!!")

  if choice==options[1]: #paper
    print("TIE GAME")

  if choice==options[2]: #scissors
    print("you lose")

if user_input == '3':
  robot=random.randint(0,2)
  choice=options[robot]
  print('Robot chose: '+ choice)
  
  if choice==options[0]: #rock
    print("you lose")

  if choice==options[1]: #paper
    print("YOU WIN!!!!!")

  if choice==options[2]: #scissors
    print("TIE GAME")


#next class, you should learn how to use a loop to re run the game over and over again



