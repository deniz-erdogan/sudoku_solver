

import pygame


class Tile:
	def __init__(self, value, window, x, y) -> None:
	    self.value = value
	    self.window = window
	    self.rect = pygame.Rect(x, y, 60, 60)
	    self.selected = False
	    self.correct = False
	    self.incorrect = False

	def draw(self, color, thickness):
		pygame.draw.rect(self.window, color, self.rect, thickness)

	
	def display(self, value, pos, color):
		font = pygame.font.SysFont(None, 45)
		text = font.render(str(value), True, color)
		self.window.blit(text, pos)

	
	def clicked(self, mousePos):
		if self.rect.collidepoint(mousePos):
			self.selected = True
		return self.selected

	