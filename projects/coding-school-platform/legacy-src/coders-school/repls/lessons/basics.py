#integer (number)
affan_age = 25
jackson_age = 10
grayson_age = 10

#string (word)
affan_name = 'Affan'
jackson_name = 'jackson'
grayson_name = 'grayson'

#STRINGS ARE THE RED WORDS

#INTEGERS ARE THE GREEN NUMBERS

#you cant add WORDS with NUMBERS

#words can only be added to words

#numbers can only be added to numbers

#dictionary!
users = {
  'key' : 'value',
  'Affan' : 25,
  'jackson' :10,
  "grayson" :10,
}
print(users['key'])


#LIST (array, box)
import random

box = [
  random.randint(0,100),
  random.randint(0,100),
  random.randint(0,100),
  random.randint(0,100),
  users['grayson'],
]

print(box)
#this is the first item in the list
print(box[4])


#Forloop (how to count in python)
#range will stop at one number before the range(value)
for counter in range(10):
  print(counter)


#INFINITE LOOP
#while True:
  #print(random.randint(0,100))