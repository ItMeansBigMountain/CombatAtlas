print("WELCOME TO THE EVERYTHING MANSION! WE HAVE EVERYTHING YOU COULD\n POSSIBLY WANT!")
Name=input("What's your name? ")
while Name=="" or Name.isdigit():
  print("HEY! You can't have an empty name.")
  Name=input("What's your name? ")

print("Hello",Name)
print("1 : Something calm")
print("2 : Something exciting")
print("3 : Something in the future")

choice = ""
while choice=="" or not choice.isdigit(): # while invalid input ask the question again
  choice=(input( "Which one would you like to do? "))

activity=choice

if choice=="1":
  print("You chose something calm.")
elif choice=="2":
  print("You chose something exiting.")
elif choice=="3":
  print("You chose something in the future.")
  
print("That is a great idea! We have two of those rooms. Which room \nwould you like to pick? The one on the left, or the one on the \nright.")
print("1 : Right")
print("2 : Left")
choice = ""
while choice=="" or not choice.isdigit(): # while invalid input ask the question again
  choice=(input( "Which one would you like to do? "))

if choice=="1":
  print("You turned right.")
  if activity=="1":
    print("You open the door to a relaxing lake at morning.Then, a sea monster apears and eats you up. YOU LOSE!")
  
  elif activity=="2":
    print("You open the door and find yourself in a plane about to skydive without a parachute! YOU LOSE!")
    
  elif activity=="3":
    print("You open the door and see a big time machine.You go forward in time and see human killing robots.YOU LOSE!")

elif choice=="2":
  print("You turned left.")
  if activity=="1":
    print("You open the door and find yourself in a very relaxing spa.Then you see that there is a zombie apocolypse.YOU LOSE!")

  elif activity=="2":
    print("You open the door and see that you are on the Takabisha.(Which is the scariest rollercoaster ever! If you didn't know.)You will also ride it without a seat belt.YOU LOSE!")
    
  elif activity=="3":
    print("You open the door and find yourself in a cheese planet eating \ncheese while holding a iphone 5000. You also have no space \nhelmet.YOU LOSE!")

print(Name + ": This is not everything I could have wanted...")
print("Oh yeah? What else could you possibly want, a chicken?")
a = input(Name + ": How about a ")
print("Ok. The " + a + " blew up." )
print("YOU LOSE! Unless you know the cheat code")
Happy=input("")
if Happy == "YOU LOSE!":
  print ("You won, I can't believe it!")
else:
  print ("YOU LOSE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")  