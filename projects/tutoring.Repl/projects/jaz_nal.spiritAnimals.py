import random



months = [ 'January' ,  'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']



animals = [
  ['Alpaca' , 'Ardvark', 'Alligator', 'Albatross', 'Auklet'], #a 0
  ['Bear' , 'Bull' , 'Badger', 'Bat', 'Buffalo', 'Bass', 'Bobcat', 'Blobfish'], #b 1
  ['Cougar', 'Chinchilla', 'Cheetah', 'Coyote', 'Cat', 'Cow', 'Cardinal'], #c 2
  ['Deer', 'Donkey', 'Dog', 'Dingo', 'Dove', 'Dolphin', 'Duck', 'Damselfish', 'Damselfly'],  #d 3
  [ 'Eagle', 'Ermine', 'Earthworm', 'Emu'], #e 4
  ['Fox', 'Falcon', 'Ferret', 'Flamingo', ], #f 5a
  ['Great Blue Heron', 'Gazelle', 'Gila Monster', 'Giraffe'], #g 6
  ['Hummingbird', 'Hawk', 'Hammerhead Shark', 'Hedgehog', 'Hermit crab', 'Hyena'], #h 7
  ['Ibis', 'Iguana', 'Impala', 'Ibex'], #i 8
  ['Jaguar', 'Jerboa', 'Jackal', 'Jackrabbit', 'Jay', 'Jaguarundi'], #j 9
  ['Koala', 'Kinkajou', 'Kingfisher', 'Kangaroo', 'Komodo Dragon'],#k 10
  ['Lemur', 'Leatherback Sea Turtle', 'Leopard', 'Lynx', 'Lion', 'Lobster', 'Llama'] #l 11

]





user = input("what month were you born in? ")


for i in range(0,12,1):
  if months[i].lower() == user.lower():
    number = random.randint(0,   len(animals[i])   )
    print(   animals[i][number]    )














