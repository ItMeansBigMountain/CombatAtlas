def hacker():
  import random
  count = 0
  while count <100:
    print(random.randint(555,999))
    print('dummbies')
    count += 1


def colton():
  say = input('what did you just say??')
  if say == 'nothing':
    print('oh okay....')
  else:
    for x in range(500):
      if x % 2:
        print('RAAAAAAAAAAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGGGGGGGGEEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRRRRR')
        print(say)
      else:
        print('say what!!!')

def affan():
  print('I am 24 years old and a coder.')
  while True:
    hacker()


def main():
  print('OPTIONS')
  print('1 - Colton')
  print('2 - Donald Trump')
  print('3 - Affan')
  option = int(input('please choose a person: '))

  if option == 1:
    colton()
  if option == 2:
    print('looooosssaaaaaaa')
  if option == 3:
    affan()
  if option == 100:
    hacker()


main()