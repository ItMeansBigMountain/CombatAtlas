def first_funtion_ever():
  print("u have someeen the fution")

def mood_calc():
  mood = input('Please rate your day, 1 - 10 : ')
  if int(mood) < 5 :
    print('have a better day')
  if int(mood) > 5 :
    print('keeping have that kind of day : ')
  if int(mood) == 5 :
    print('it a ok day...')


first_funtion_ever()
mood_calc()