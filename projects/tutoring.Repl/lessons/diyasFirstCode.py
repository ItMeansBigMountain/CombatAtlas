# a function is doing something the same way every time

# DEFINE FUNCTIONS HERE
def adventure():
  print("welcome to Diya's mysterious adventure")

  # Data About Diya
  name = input("please enter your name: ")
  age = int(input("please enter your age: "))
  gender = input("are you a boy or girl?:  ")
  place = input("please enter your a place: ")
  things = input("please enter multiple things: ")
  animal = input("please enter an animal: ")

  print()
  print( name + " is " + str(age) + " years old")
  print(name + " is a " + gender)
  print( name  + " walks into the " + place)
  print(" there are a lot of " + things  )
  print(" on one of the "  +  things  +  " you see a " + animal)
  print("the "+ animal + " sees you and starts to fly towards you!")
  print("the " + animal + " eats you alive, the end")


  print("you woke up in a hospital after the " + animal  + " attack.")
  print("you see 3 doors...")

  print("1: door one is fire door")
  print("2: door two is ice door")
  print('3: door three is a something room')

  option = input("please choose a door: ")
  if option == '3':
    print("you entered the something room")
    print("Inside the something room, you see a " + gender)
    attack = input("do you want to fight it? ")
    if attack=='yes':
      print("the " + gender +  " dies")
  else:
    print("you die")





# CALLING FUNCTIONS HERE
adventure()

