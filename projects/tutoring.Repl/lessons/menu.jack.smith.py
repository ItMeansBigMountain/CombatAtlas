import random

answer = 'rap'
print("what is a elfise favrit tipe of music")
riddle = input("please answer the riddle: ")

if riddle == answer:
  print("YOU WIN!")
else:
  print("YOU LOSE TRY AGAIN!")



print("YOU WALK INTO A ROOM WITH THREE DOORS")

option = input("which one will you to go to?: ")

  

if option == "1":
  print('YOU CHOSE: door one!')
  print("The door lead you to a room filled with lava.... you trip and fall in...")
  print("YOU LOSE TRY AGAIN!")


if option == "2":
  print('YOU CHOSE: door two !')
  print("You open the door and the light was so intense that you turned into toast")
  print("YOU LOSE TRY AGAIN!")


if option == "3":
  print('door three!')
  print('you walk into a pool filled with parannas')
  print("BUT THE POOL IS FILLED WITH SALT!!!!! parannas cant swim in salt water.")
  
  option = input("There are now 3 keys on the table... please choose a key: ")

  if option == '1' :
    print("this was a lava key, your hand burned and you drop the key")
    print('you LOSE TRY agaen')

  if option == '2' :
    print('you made the right decision!')
    print("gooooooooood joooooooooob")

  if option == '3':
    print('you pick up the ice key and you turn into an ice cube...')
    print('you LOSE TRY again')