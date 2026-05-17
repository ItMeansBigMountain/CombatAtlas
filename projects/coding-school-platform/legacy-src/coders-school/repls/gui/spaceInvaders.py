
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
print ("sup, have fun!!!!!!!!!!!!!!!!!!!!!!!!")

# Player
playerImg = pygame.transform.scale(pygame.image.load('playerShip.png'), (140, 140))
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0
# Enemy
enemyImg = (pygame.image.load('notes.png'))
enemyX = (random.randint(0,735))
enemyY = (random.randint(50,150))
enemyX_change = (4)
enemyY_change = (10)

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
   pygame.draw.circle(screen,(0,0,255,25),(playerX+70,playerY+70), 25, 1)
def enemy(x,y):
    
    screen.blit(enemyImg, (x,y))
    pygame.draw.circle(screen,(255,0,0,25),(enemyX+30,enemyY+30), 25, 1)
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    
    screen.blit(bulletImg, (x-15,y))
    pygame.draw.circle(screen, (0,0,255,25), (x,y), 25, 1)
def iscollision(enemyX, enemyY, bulletX, bulletY, threshold):
	distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
	if distance < threshold:
		return True
	else:
		return False

display_width = 800
display_height = 600
black = (0,0,0)
white = (255,255,255)
gameDisplay = pygame.display.set_mode((display_width,display_height))
red = (255,0,0)

def message_display(text):
  largeText = pygame.font.Font('freesansbold.ttf',100)
  TextSurf, TextRect = text_objects(text, largeText)
  TextRect.center = ((750),(50))
  gameDisplay.blit(TextSurf, TextRect)

def text_objects(text, font):
  textSurface = font.render(text, True, white)
  return textSurface, textSurface.get_rect()


# GameLoop
running = True
while running:
	screen.fill((0,0,0))
	# background image
	screen.blit(background,(0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False    
# if keystroke pressed, check what direction
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				playerX_change = -3
			if event.key == pygame.K_d:
				playerX_change = 3
			if event.key == pygame.K_w:
				playerY_change = -3
			if event.key == pygame.K_s:
				playerY_change = 3
			if event.key == pygame.K_SPACE:
				if bullet_state == "ready":
					bulletX = playerX
					bulletY = playerY
					fire_bullet(bulletX,bulletY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a or event.key == pygame.K_d:
		    		playerX_change = 0
			if event.key == pygame.K_w or event.key == pygame.K_s:
		    		playerY_change = 0
# checking for MAP BOUNDRIES
	playerX += playerX_change
	playerY += playerY_change
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
	if bullet_state == 'fire':
		fire_bullet(bulletX+70,bulletY+10)
		bulletY += bulletY_change
	
	# collision
	collision = iscollision(enemyX+30, enemyY+30, bulletX+70, bulletY+10,50)
	if collision and bullet_state=="fire":
		bulletY = 480
		bullet_state = 'ready'
		score += 1
		print(score)
		enemyX = random.randint(0,735)
		enemyY = random.randint(50,150)

	collision = iscollision(playerX+70, playerY+70, enemyX+30, enemyY+30, 100)
	if collision:
		playerY = 480
		bullet_state = 'ready'
		score = 0
		print("You died!")
		enemyX = random.randint(0,735)
		enemyY = random.randint(50,150)
  
  

	player(playerX,playerY)  
	enemy(enemyX,enemyY)
	message_display(str(score))
	pygame.display.update()