import random
import test
import time

secret = random.randint(0,100)
options = int(     input("please choose a number: ")        )

while secret != options:
  print("you're wrong.")
  if options > secret:
    print("too much")
  if options < secret:
    print("not enough")
  options = int(input("please choose a number: "))

  if options == 9:
    while True:
      print("you're wrong a lot")