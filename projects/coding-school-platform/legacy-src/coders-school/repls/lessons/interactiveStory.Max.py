age = int(input("what is your age?: "))

adult = False

if age > 18:
  print('you are an adult')
  adult = True
else:
  print("youre just a kid. ")
  adult = False


print(  "you are " + str(age)    )
print(adult)

