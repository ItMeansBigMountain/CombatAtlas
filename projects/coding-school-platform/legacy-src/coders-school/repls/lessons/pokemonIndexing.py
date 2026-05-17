pokemon_id = [1,2, 3, 4,5,6]
pokemon=['mew','mewtow', 'Blastois', 'Charzard', 'MEGA Charizard X','Charmeleon']
atk = [100,180,80, 130,300000,30]
defence = [180,200,20, 100,100000,30]

for x in range(len(pokemon)):
  print(x+1, str(pokemon[x]))


option = int(input('Please enter a pokemon ID: '))

for x in pokemon_id:
  if x == option:
    print(pokemon[option-1])
    print('ATTACK: ', atk[option-1])
    print('DEFENCE: ', defence[option-1])