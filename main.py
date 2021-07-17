import pygame
from board import Board
from tile import Tile
import time

def main():
	'''Runs the main Sudoku GUI/Game'''
	pygame.init()
	screen = pygame.display.set_mode((540, 590))
	screen.fill((255, 255, 255))
	pygame.display.set_caption("Sudoku")

	#loading screen when generating grid
	font = pygame.font.SysFont('Bahnschrift', 40)
	text = font.render("Generating", True, (0, 0, 0))
	screen.blit(text, (175, 245))

	font = pygame.font.SysFont('Bahnschrift', 40)
	text = font.render("Grid", True, (0, 0, 0))
	screen.blit(text, (230, 290))
	pygame.display.flip()

	#initiliaze values and variables
	wrong = 0
	board = Board(screen)
	selected = -1,-1 #NoneType error when selected = None, easier to just format as a tuple whose value will never be used
	keyDict = {}
	running = True
	startTime = time.time()
	while running:
		elapsed = time.time() - startTime
		passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))

		if board.board == board.solved: #user has solved the board
			for i in range(9):
				for j in range(9):
					board.tiles[i][j].selected = False
					running = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit() #so that it doesnt go to the outer run loop

			elif event.type == pygame.MOUSEBUTTONUP: #allow clicks only while the board hasn't been solved
				mousePos = pygame.mouse.get_pos()
				for i in range(9):
					for j in range (9):
						if board.tiles[i][j].clicked(mousePos):
							selected = i,j
							board.deselect(board.tiles[i][j]) #deselects every tile except the one currently clicked

			elif event.type == pygame.KEYDOWN:
				if board.board[selected[1]][selected[0]] == 0 and selected != (-1,-1):
					if event.key == pygame.K_1:
						keyDict[selected] = 1

					if event.key == pygame.K_2:
						keyDict[selected] = 2

					if event.key == pygame.K_3:
						keyDict[selected] = 3

					if event.key == pygame.K_4:
						keyDict[selected] = 4

					if event.key == pygame.K_5:
						keyDict[selected] = 5

					if event.key == pygame.K_6:
						keyDict[selected] = 6

					if event.key == pygame.K_7:
						keyDict[selected] = 7

					if event.key == pygame.K_8:
						keyDict[selected] = 8

					if event.key == pygame.K_9:
						keyDict[selected] = 9

					elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:  # clears tile out
						if selected in keyDict:
							board.tiles[selected[1]][selected[0]].value = 0
							del keyDict[selected]

					elif event.key == pygame.K_RETURN:
						if selected in keyDict:
							if keyDict[selected] != board.solved[selected[1]][selected[0]]: #clear tile when incorrect value is inputted
								wrong += 1
								board.tiles[selected[1]][selected[0]].value = 0
								del keyDict[selected]
								break
							#valid and correct entry into cell
							board.tiles[selected[1]][selected[0]].value = keyDict[selected] #assigns current grid value
							board.board[selected[1]][selected[0]] = keyDict[selected] #assigns to actual board so that the correct value can't be modified
							del keyDict[selected]

				if event.key == pygame.K_h:
					board.hint(keyDict)

				if event.key == pygame.K_SPACE:
					for i in range(9):
						for j in range(9):
							board.tiles[i][j].selected = False
					keyDict = {}  #clear keyDict out
					board.visualSolve(wrong, passedTime)
					for i in range(9):
						for j in range(9):
							board.tiles[i][j].correct = False
							board.tiles[i][j].incorrect = False #reset tiles
					running = False

		board.redraw(keyDict, wrong, passedTime)
	while True: #another running loop so that the program ONLY closes when user closes program
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
main()
pygame.quit()