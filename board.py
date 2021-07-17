from copy import deepcopy
from sudoku import generate_board, solve
from copy import deepcopy
from tile import *
from sudoku import *

class Board:
	def __init__(self, window) -> None:
		self.board = generate_board()
		self.solved = deepcopy(self.board)
		solve(self.solved)
		self.tiles = [[Tile(self.board[i][j], window, i*60, j*60) for j in range(9)] for i in range(9)]
		self.window = window


	def draw_board(self):
		for i in range(9):
			for j in range(9):
				if j%3 == 0 and j != 0:
					pygame.draw.line(self.window, (0, 0, 0), ((j//3)*180, 0), ((j//3)*180, 540), 4)

				if i%3 == 0 and i != 0:
					pygame.draw.line(self.window, (0, 0, 0), (0, (i//3)*180), (540, (i//3)*180), 4)

				self.tiles[i][j].draw((0,0,0), 1)

				if self.tiles[i][j].value != 0:
					self.tiles[i][j].display(self.tiles[i][j].value, (21+(j*60), (16+(i*60))), (0, 0, 0))
		pygame.draw.line(self.window, (0, 0, 0), (0, ((i+1) // 3) * 180), (540, ((i+1) // 3) * 180), 4)


	def deselect(self, tile):
		for i in range(9):
			for j in range(9):
				if self.tiles[i][j] != tile:
					self.tiles[i][j].selected = False


	def redraw(self, keys, wrong, time):
		self.window.fill((255,255,255))
		self.draw_board()
		for i in range(9):
			for j in range(9):
				if self.tiles[j][i].selected:  #draws the border on selected tiles
					self.tiles[j][i].draw((50, 205, 50), 4)
					
				elif self.tiles[i][j].correct:
					self.tiles[j][i].draw((34, 139, 34), 4)
					
				elif self.tiles[i][j].incorrect:
					self.tiles[j][i].draw((255, 0, 0), 4)
					
		if len(keys) != 0: #draws inputs that the user places on board but not their final value on that tile
			for value in keys:
				self.tiles[value[0]][value[1]].display(keys[value], (21+(value[0]*60), (16+(value[1]*60))), (128, 128, 128))
				
			
		if wrong > 0:
			font = pygame.font.SysFont('Bauhaus 93', 30) #Red X
			text = font.render('X', True, (255, 0, 0))
			self.window.blit(text, (10, 554))

			font = pygame.font.SysFont('Bahnschrift', 40) #Number of Incorrect Inputs
			text = font.render(str(wrong), True, (0, 0, 0))
			self.window.blit(text, (32, 542))

		else:
			font = pygame.font.SysFont('Bahnschrift', 40) #Time Display
			text = font.render(str(time), True, (0, 0, 0))
			self.window.blit(text, (388, 542))
		pygame.display.flip()

	def visualSolve(self, wrong, time):
		for event in pygame.event.get(): #so that touching anything doesn't freeze the screen
			if event.type == pygame.QUIT:
				exit()

		empty = find_empty(self.board)
		if not empty:
			return True

		for nums in range(9):
			if is_valid(self.board, (empty[0],empty[1]), nums+1):
				self.board[empty[0]][empty[1]] = nums+1
				self.tiles[empty[0]][empty[1]].value = nums+1
				self.tiles[empty[0]][empty[1]].correct = True
				pygame.time.delay(63) #show tiles at a slower rate
				self.redraw({}, wrong, time)

				if self.visualSolve(wrong, time):
					return True

				self.board[empty[0]][empty[1]] = 0
				self.tiles[empty[0]][empty[1]].value = 0
				self.tiles[empty[0]][empty[1]].incorrect = True
				self.tiles[empty[0]][empty[1]].correct = False
				pygame.time.delay(63)
				self.redraw({}, wrong, time)

	def hint(self, keys):
		while True: #keeps generating i,j coords until it finds a valid random spot
			i = random.randint(0, 8)
			j = random.randint(0, 8)
			if self.board[i][j] == 0: #hint spot has to be empty
				if (j,i) in keys:
					del keys[(j,i)]
				self.board[i][j] = self.solvedBoard[i][j]
				self.tiles[i][j].value = self.solvedBoard[i][j]
				return True

			elif self.board == self.solvedBoard:
				return False