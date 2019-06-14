import pygame
from pygame.locals import *
import sys


pygame.init()
pygame.font.init()


font = pygame.font.Font(pygame.font.match_font('arial'), 16)
font.set_bold(True)

font1 = pygame.font.Font(pygame.font.match_font('arial'), 32)
font1.set_bold(True)


turn = None


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400


LEVEL_1 = pygame.image.load("LEVEL_1.png")
HERO_IMG = pygame.image.load('hero.png')
COIN_IMG = pygame.image.load('coin.png')
LAKE_IMG = pygame.image.load('lake.png')


COINS = []
LAKES = []

COUNT = 0

LEGEND_1 = [
		[1]*10,#1
		[1,4]*2 + [0]*4 + [5,1],#2
		[1,0]*2 + [1]*4 + [0,1],#3
		[1,0]*2 + [1,4] + [0,1]*2,#4
		[1,0]*2 + [1,1] + [0,1]*2,#5
		[1,0]*2 + [0,1] + [0]*3 + [1],#6
		[1,0,1,1,0] + [1]*3 + [0,1],#7
		[1] + [0]*4 + [2] + [0]*3 + [1],#8
		[1,1,0] + [1]*7,#9
		[1,1,0,1] + [0]*5 + [1],#10
		[1,1,0,0,0,1,0,1,0,1],#11
		[1]*6 + [0,1]*2,#12
		[1] + [0]*3 + [1] + [0,0] + [1,0,1],#13
		[1,3,1,4,0,0,1,1,4,1],#14
		[1]*10#15
	]

### Set hero's coordinates ###
for i in range(15):
	if 5 in LEGEND_1[i]:
		XCOR = i * 40

		for j in range(10):
			if LEGEND_1[i][j] == 5:
				YCOR = j *40

### Fill in the lists of coordinates of coins and lakes ###
for i in range(15):
	if 2 in LEGEND_1[i] or 4 in LEGEND_1[i]:
		for j in range(10):
			if LEGEND_1[i][j] == 2:
				LAKES.append([i*40, j*40])

			if LEGEND_1[i][j] == 4:
				COINS.append([i*40, j*40])
				COUNT += 1

			if LEGEND_1[i][j] == 3:
				FINX = i * 40
				FINY = j * 40

### Creating the main screen ###

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

screen.blit(LEVEL_1, [0,0])

### Functions ###


def stack():
	for lake in LAKES:
		screen.blit(LAKE_IMG, lake)

	for coin in COINS:
		screen.blit(COIN_IMG, coin)


def do_move():
	global XCOR, YCOR, turn

	col, row = int(XCOR/40), int(YCOR/40)
	can = False
	ok = [0, 2, 3, 4]
	dx, dy = 0, 0

	if turn == 'u' and LEGEND_1[col][row-1] in ok:
		can = True
		dy -= 1

	elif turn == 'r' and LEGEND_1[col+1][row] in ok:
		can = True
		dx += 1

	elif turn == 'd' and LEGEND_1[col][row+1] in ok:
		can = True
		dy += 1

	elif turn == 'l' and LEGEND_1[col-1][row] in ok:
		can = True
		dx -= 1

	if can == True:

		LEGEND_1[col][row] = 0

		XCOR = XCOR + dx*40
		YCOR = YCOR + dy*40

	LEGEND_1[int(XCOR/40)][int(YCOR/40)] = 5

	turn = None


def clean_lists():
	global XCOR, YCOR

	if [XCOR, YCOR] in LAKES:
		LAKES.remove([XCOR, YCOR])

	if [XCOR, YCOR] in COINS:
		COINS.remove([XCOR, YCOR])


def score():
	screen.blit(font.render(str(COUNT-len(COINS)) + '/' + str(COUNT), False, (0,0,0)), (528,15)) 




while True:

	if XCOR == FINX and YCOR == FINY:
		break

	screen.blit(LEVEL_1, [0,0])

	stack()

	clean_lists()

	screen.blit(HERO_IMG, [XCOR, YCOR])

	score()
	
	for event in pygame.event.get():
		
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == KEYDOWN:
			k = event.key

			if k == 273:
				turn = 'u'

			elif k == 274:
				turn = 'd'

			elif k == 275:
				turn = 'r'

			elif k == 276:
				turn = 'l'


	do_move()


	pygame.display.update()


while True:
	
	pygame.draw.rect(screen, (255, 255, 255), (200, 120, 200, 160))

	screen.blit(font1.render('Level 1 have gone', False, (0,0,0)), (260, 180))

	for event in pygame.event.get():
		
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	pygame.display.update()