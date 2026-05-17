def question1():
  print ("starting test")
  answers=[]
  
  right_answer=3
  print()
  print("Whats my favorite food?")
  print("1 : Lasanga ")
  print("2 : Mac N Cheese ")
  print("3 : Pizza ")
  print("4 : Chicken ")
  option = int(input("Please choose an answer: "))
  if option == right_answer:
    print('YAY GOOD JOB')
  else:
    print('wow i cant believe you got that wrong...')

def question2():

  answers=[]
  
  right_answer=4
  print()
  print("Whats my favorite sport?")
  print("1 : Football ")
  print("2 : Basketball ")
  print("3 : Baseball ")
  print("4 : Hockey ")
  option = int(input("Please choose an answer: "))
  if option == right_answer:
    print('YAY GOOD JOB')
  else:
    print('wow i cant believe you got that wrong...')
def question3():

  answers=[]
  
  right_answer=2
  print()
  print("Whats my favorite Game Console?")
  print("1 :PS5  ")
  print("2 : Vr ")
  print("3 : Xbox ")
  print("4 : Stadia(defently not) ")
  option = int(input("Please choose an answer: "))
  if option == right_answer:
    print('YAY GOOD JOB')
  else:
    print('wow i cant believe you got that wrong...')

#running when app starts
def main():

  print ("hello world")
  print ("Welcome to my test")
  name=input("What is your name?: ")
  print("Hello",name)
  print()
  question1()
  question2()
  question3()
  print ("function has ended")

main()
