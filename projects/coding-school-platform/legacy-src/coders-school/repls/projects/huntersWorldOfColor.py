import random



def WorldOfCOLORandFOOD():
  cake = '🍰'  *  900
  panOfFood = '🥘' * 900
  ROOTBEER = '🍻'* 9000
  emojis = '''
  🥨🍳🥩🧀🥧🍦🍭🍤🍤🍤🐌🦞🐙🦀🥯🌽🥔🍻🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🧃🧃🧃🍯🍪🍫🧇🍕🍝🍣🍛🍤🧁🍻🍤🍤🍤🍤🍤🎄🐉🦚🐊🦑🦞🐙🐙🐡🐳☀️️🔥☀️️☁️️☁️️⛈⛅️️🌦🌩🌨❄️️💥✨💫⭐️️🌟🌙🍒🥝🥦🍍🍳🥒🥑🍅🍆🌽🥨🧀🥩🥞🥖🧀🥚🥓🥩🧇🥶🌭🍕🥘🥗🍝🍣🥘🥨🍳🥩🧀🥧🍦🍭🍤🍤🍤🐌🦞🐙🦀🥯🌊🌊🌊🌊🌊🌊🌊🌽🥔🍻🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍷🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🍻🧃🧃🧃🧃🧃🧃🧃🧃🧃🧃🍷🧃🧃🧃🍯🍪🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🇹🇷🧇🍕🍝🍣🍛🍤🧁🍻🍤🍤🍤🍤🍤🎄🐉🦚🐊🦑🦞🐙🐙🐡🐳☀️️️🔥☀☁️️☁⛈⛅️️🌦🌩🌨❄️️💥✨💫⭐️️🌟🌙🍒🥝🥦🍍🍳🥒🥑🍅🍆🌽🥨🧀🥩🥞🥖🧀🥚🥓🥩🧇🌭🍕🥘🥗🍝🍣🍭🍭🍭🍭🍭🍭🍭🍭🍭🍭🍭🍭🍭🍭🍭🍭🍭🍰🍭🍭🍭🍭🍭🍭🍭🍭🍰🍫🍫🍫🍫🍫🍫🍫🍫🍫🍫🍫🍫🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉 ``'
  '''
  print(cake) 
  print(panOfFood)
  print(ROOTBEER)
  for x in emojis:
    print( x * 100000  )





# calling functions down here
# WorldOfCOLORandFOOD()

answer = random.randint(1,9)
lives = 3476376836478317863781378
while lives > 0:
  print(lives)
  print("CHOICES")
  print('1 - 🥩')
  print('2 - 🍤')
  print('3 - 🐉')
  print('4 - 🌳')
  print('5 - 🌴')
  print('6 - ☀️')
  print('7 - 🔥')
  print('8 - 💥')
  print('9 - 🍣')
  print('10 - 🇹🇷')  

  guess = input("Please choose an option: ")

  if  int(guess) == answer:
    print("you win!!!!!")
    WorldOfCOLORandFOOD()
  else:
    print('YOU LOSE!!!!')
    lives = lives - 1

