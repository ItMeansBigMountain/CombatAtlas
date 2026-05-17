import pygame

import random
import math


#Initialization
pygame.init()
# Create the screen
screen = pygame.display.set_mode((800,600))
# background
background = pygame.image.load('bape.jpg')
# TITLE AND ICON 
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('player.png')
pygame.display.set_icon(icon)


# Player
playerImg = pygame.image.load('purple_pixels.png')
playerX = 370
playerY = 480
playerX_change = 0
# Enemy
enemyImg = (pygame.image.load('notes.png'))
enemyX = (random.randint(0,735))
enemyY = (random.randint(50,150))
enemyX_change = (4)
enemyY_change = (40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480 #player is at this level at all times
bulletX_change = 4
bulletY_change = -10
bullet_state = "ready"

score = 0

def player(x,y):
	screen.blit(playerImg, (x,y))
def enemy(x,y):
	screen.blit(enemyImg, (x,y))
def fire_bullet(x,y):
	global bullet_state
	bullet_state = 'fire'
	screen.blit(bulletImg, (x+16,y+10))
def iscollision(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt(  (math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2))    )
	if distance < 27:
		return True
	else:
		return False














# GameLoop 30 frames per second
running = True
while running:
	# background image
	screen.fill((0,0,0))
	screen.blit(background,(0,0))

	#CHECKING FOR EVENTS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		# if keystroke pressed, check what direction
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -3
			if event.key == pygame.K_RIGHT:
				playerX_change = 3
			if event.key == pygame.K_SPACE:
				if bullet_state is "ready":
					bulletX = playerX
					fire_bullet(bulletX,bulletY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0
	
	
	# checking for MAP BOUNDRIES
	playerX += playerX_change
	if playerX<=0:
		playerX=0
	elif playerX >=736:
		playerX=736

	# EnemyBOUNDRIES
	enemyX += enemyX_change
	if enemyX<=0:
		enemyX_change = 4
		enemyY += enemyY_change
	elif enemyX >=736:
		enemyX_change = -4
		enemyY += enemyY_change

	# bullet movment
	if bulletY<=0:
		bulletY = 480
		bullet_state = 'ready'
	if bullet_state is 'fire':
		fire_bullet(bulletX,bulletY)
		bulletY += bulletY_change
	
	# collision
	collision = iscollision(enemyX, enemyY, bulletX, bulletY)
	if collision:
		bulletY = 480
		bullet_state = 'ready'
		score += 1
		print(score)
		enemyX = random.randint(0,735)
		enemyY = random.randint(50,150)

	player(playerX,playerY)
	enemy(enemyX,enemyY)
	pygame.display.update()

