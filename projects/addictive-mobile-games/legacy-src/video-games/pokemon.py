import time
import numpy as np
import sys

# delay printing

def delay_print(s):
	for c in s:
		sys.stdout.write(c)
		sys.stdout.flush()
		time.sleep(0.05)

# create class

class Pokemon:
	def __init__(self, name, types, moves, EVs, health= '===================='):
		# save varialbles as attributes
		self.name = name
		self.types = types
		self.moves = moves
		self.health = health
		self.attack = EVs['ATTACK']
		self.defense = EVs['DEFENSE']
		self.bars = 50 #amount of health bars

	def fight(self, Pokemon2):
		# allow two pokemon to fight eachother
		# print fight information
		print('---------POKEMON BATTLE---------')
		print(f"\n{self.name}")
		print('TYPE/', self.types)
		print('ATTACK/', self.attack)
		print('DEFENSE/', self.defense)
		print('LVL/', 3+(1+np.mean([self.attack, self.defense])))
		print('\nVS')
	
		# Pokemon2
		print(f"\n{Pokemon2.name}")
		print('TYPE/', Pokemon2.types)
		print('ATTACK/', Pokemon2.attack)
		print('DEFENSE/', Pokemon2.defense)
		print('LVL/', 3+(1+np.mean([Pokemon2.attack, Pokemon2.defense])))
		time.sleep(2)

		# consider types advantages
		version = ['fire', 'water', 'grass']
		for i,k in enumerate(version):
			if self.types == k:
				# Both are SAME type
				if Pokemon2.types == k :
					string_1_attack = 'Its not very effective...'
					string_2_attack = 'Its not very effective...'
				# Pokemon2 is STRONG
				if Pokemon2.types == version[(i+1)%3]:
					Pokemon2.attack *= 2
					Pokemon2.defense *= 2
					self.attack /= 2
					self.defense /= 2
					string_1_attack = 'Its not very effective...'
					string_2_attack = 'Its super effective!'
				# Pokemon2 is WEAK
				if Pokemon2.types == version[(i+2)%3]:
					self.attack *= 2
					self.defense *= 2
					Pokemon2.attack /= 2
					Pokemon2.defense /= 2
					string_1_attack = 'Its super effective!'
					string_2_attack = 'Its not very effective...'


		# now for the actual fight
		# contninue while pokemon still have health
		while (self.bars> 0) and (Pokemon2.bars > 0):
			# Print health of each pokemon
			print(f'\n{self.name}\t\HLTH\t{self.health}')
			print(f'{Pokemon2.name}\t\HLTH\t{Pokemon2.health}')

			print(f'\nGo {self.name}!')
			for i,x in enumerate(self.moves):
				print(f'\n{i+1}.', x)

			index = int(input('\nPick a move: '))
			delay_print(f'\n{self.name} used {self.moves[index-1]}!')
			print()
			time.sleep(1)

			delay_print(string_1_attack)

			# determimne damage
			Pokemon2.bars -= self.attack
			Pokemon2.health = ''

			# add back bars 
			for j in range(int(Pokemon2.bars+.1*Pokemon2.defense)):
				Pokemon2.health += '='
			time.sleep(1)
			# Print health of each pokemon
			print(f'\n{self.name}\t\HLTH\t{self.health}')
			print(f'{Pokemon2.name}\t\HLTH\t{Pokemon2.health}')
			time.sleep(.5)
			# check to see if pokemon has fainted
			if Pokemon2.bars <= 0:
				delay_print('\n...' + Pokemon2.name + ' fainted!!')
				print()
				break
			# pokemon2 turn to attack if not fainted 

			print(f'\nGo {Pokemon2.name}!')
			for i,x in enumerate(Pokemon2.moves):
				print(f'\n{i+1}.', x)
			index = int(input('Pick a move: '))
			delay_print(f'\n{Pokemon2.name} used {Pokemon2.moves[index-1]}!')
			time.sleep(1)
			print()

			delay_print(string_2_attack)

			# determimne damage
			self.bars -= Pokemon2.attack
			self.health = ''

			# add back bars 
			for j in range(int(self.bars+.1*self.defense)):
				self.health += '='

			time.sleep(1)

			# Print health of each pokemon
			print(f'\n{self.name}\t\HLTH\t{self.health}')
			print(f'{Pokemon2.name}\t\HLTH\t{Pokemon2.health}')
			time.sleep(.5)

			# check to see if pokemon has fainted
			if self.bars <= 0:
				delay_print('\n...' + self.name + ' fainted!!')
				print()
				break
			
		money = np.random.choice(5000)
		delay_print(f'\nOpponent paid you ${money}')

		


if __name__ == '__main__':
	pass
	
	# create pokemon
	Charizard = Pokemon('Charizard', 'fire', ['FlameThrower','Fly', 'Blast Burn', 'Fire Punch'] , {'ATTACK': 12, 'DEFENSE': 8})

	
	Blastoise = Pokemon('Blastoise', 'water', ['Water Gun', 'BubleBeam', 'Hydro Pump', 'Surf'] , {'ATTACK': 10, 'DEFENSE': 10})

	Bulbasuar = Pokemon('Bulbasuar', 'grass', ['Vine Whip', 'Razor Leaf', 'Earthquake', 'Cut'] , {'ATTACK': 8, 'DEFENSE': 12})







player1 = int(input('PLAYER =ONE!\n\n Choose a pokemon!\n\n 1.CHARZARD \n\n 2.BLASTOISE \n\n 3.BULBASUAR\n\t'))

print()

player2 = int(input('PLAYER TWO!\n\n Choose a pokemon!\n\n 1.CHARZARD \n\n 2.BLASTOISE \n\n 3.BULBASUAR\n\t'))


if player1 == 1 and player2 == 1:
	Charizard.fight(Charizard)
elif player1 == 1 and player2 == 2:
	Charizard.fight(Blastoise)
elif player1 == 1 and player2 == 3:
	Charizard.fight(Bulbasuar)

elif player1 == 2 and player2 == 1:
	Blastoise.fight(Charizard)
elif player1 == 2 and player2 == 2:
	Blastoise.fight(Blastoise)
elif player1 == 2 and player2 == 3:
	Blastoise.fight(Bulbasuar)

elif player1 == 3 and player2 == 1:
	Bulbasuar.fight(Charizard)
elif player1 == 3 and player2 == 2:
	Bulbasuar.fight(Blastoise)
elif player1 == 3 and player2 == 3:
	Bulbasuar.fight(Bulbasuar)