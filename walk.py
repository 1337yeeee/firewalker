import pygame
from pygame.locals import *
from levels import levels
import sys
import os
import time


pygame.init()
pygame.font.init()


font = pygame.font.Font(pygame.font.match_font('arial'), 16)
font.set_bold(True)

font1 = pygame.font.Font(pygame.font.match_font('arial'), 32)
font1.set_bold(True)


turn = None


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400


HERO_IMG = pygame.image.load(os.path.join('img', 'hero.png'))
COIN_IMG = pygame.image.load(os.path.join('img', 'coin.png'))
LAKE_IMG = pygame.image.load(os.path.join('img', 'lake.png'))
FINISH_IMG = pygame.image.load(os.path.join('img', 'finish.png'))

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
screen.fill((0,0,0))

COINS = []
LAKES = []

COUNT = 0

level_num = 1




class Level():

	def __init__(self, num, COINS = [], LAKES = [], COUNT = 0):
		self.num = num
		self.legend = levels[num]
		self.COINS = COINS
		self.LAKES = LAKES
		self.COUNT = COUNT
		self.level_img = pygame.image.load(os.path.join('img', 'LEVEL_%s.png' %num))
		self.XCOR = None
		self.YCOR = None
		self.FINX = None
		self.FINY = None


	def cors(self):
		legend = self.legend

		for i in range(15):
			for j in range(10):
				if legend[i][j] == 5:
					self.XCOR = i * 40
					self.YCOR = j *40
				if legend[i][j] == 3:
					self.FINX = i * 40
					self.FINY = j * 40


	def fill_lists(self):
		legend = self.legend

		for i in range(15):
			if 2 in legend[i] or 4 in legend[i]:
				for j in range(10):
					if legend[i][j] == 2:
						self.LAKES.append([i*40, j*40])

					if legend[i][j] == 4:
						self.COINS.append([i*40, j*40])
						self.COUNT += 1


	def stack(self):
		global LAKE_IMG, COIN_IMG

		for lake in self.LAKES:
			screen.blit(LAKE_IMG, lake)

		for coin in self.COINS:
			screen.blit(COIN_IMG, coin)

		screen.blit(FINISH_IMG, [self.FINX, self.FINY])


	def clean_lists(self):
		XCOR, YCOR = self.XCOR, self.YCOR

		if [XCOR, YCOR] in self.LAKES:
			self.LAKES.remove([XCOR, YCOR])

		if [XCOR, YCOR] in self.COINS:
			self.COINS.remove([XCOR, YCOR])

	def score(self):
		screen.blit(font.render(str(self.COUNT-len(self.COINS)) + '/' + str(self.COUNT), False, (0,0,0)), (528,15))


	def do_move(self):
		global turn

		legend = self.legend

		col, row = int(self.XCOR/40), int(self.YCOR/40)
		can = False
		ok = [0, 2, 3, 4]
		dx, dy = 0, 0

		if turn == 'u' and legend[col][row-1] in ok:
			can = True
			dy -= 1

		elif turn == 'r' and legend[col+1][row] in ok:
			can = True
			dx += 1

		elif turn == 'd' and legend[col][row+1] in ok:
			can = True
			dy += 1

		elif turn == 'l' and legend[col-1][row] in ok:
			can = True
			dx -= 1

		if can == True:

			legend[col][row] = 0

			self.XCOR += dx*40
			self.YCOR += dy*40

		legend[int(self.XCOR/40)][int(self.YCOR/40)] = 5

		time.sleep(0.1)




### menu ###


def menu():

	while True:
		screen.blit(pygame.image.load(os.path.join('img', 'menu.png')), [0,0])

		for event in pygame.event.get():

			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == 6:
				if 225 <= event.pos[0] <= 375 and 280 <= event.pos[1] <= 318:
					pygame.quit()
					sys.exit()

				elif 225 <= event.pos[0] <= 375 and 135 <= event.pos[1] <= 173:
					return 'play'

				elif 225 <= event.pos[0] <= 375 and 207 <= event.pos[1] <= 245:
					return 'levels'


		pygame.display.update()


### pick level ###


def what_level():

	while True:
		screen.blit(pygame.image.load(os.path.join('img', 'what_level.png')), [0,0])

		for event in pygame.event.get():

			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == 6:
				if 0 <= event.pos[0] <= 50 and 0 <= event.pos[1] <= 30:
					main()

				if 193 <= event.pos[0] <= 253 and 161 <= event.pos[1] <= 222:
					return 1

				if 376 <= event.pos[0] <= 436 and 161 <= event.pos[1] <= 222:
					return 2					

		pygame.display.update()


### game ###


def game(level_num):

	global screen, turn

	while True:

		level = Level(level_num)

		level.cors()

		level.fill_lists()

		KDOWN = False

		while True:
			if level.XCOR == level.FINX and level.YCOR == level.FINY:
				level.COINS.clear()
				level.LAKES.clear()
				break


			screen.blit(level.level_img, [0,0])

			level.stack()

			level.clean_lists()

			screen.blit(HERO_IMG, [level.XCOR, level.YCOR])

			level.score()


			for event in pygame.event.get():
		
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

				if event.type == 6:
					if 0 <= event.pos[0] <= 50 and 0 <= event.pos[1] <= 30:

						level.COINS.clear()
						level.LAKES.clear()

						main()

				if event.type == KEYDOWN:
					KDOWN = True
					k = event.key

					if k == 273:
						turn = 'u'

					elif k == 274:
						turn = 'd'

					elif k == 275:
						turn = 'r'

					elif k == 276:
						turn = 'l'

				if event.type == KEYUP:
					KDOWN = False


			if KDOWN == True:
				level.do_move()
			elif KDOWN == False:
				turn = None


			pygame.display.update()


		level_num += 1


### main ###


def main():
	what = menu()

	if what == 'play':
		try: 
			game(level_num)
		except:
			game(1)

	elif what == 'levels':
		game(what_level())

	



if __name__ == '__main__':

	main()
	
