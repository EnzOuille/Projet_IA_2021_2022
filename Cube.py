import pygame
pygame.font.init()

class Cube:
	rows=9
	cols=9

	def __init__(self,value,row,col):
		self.value=value
		self.row=row
		self.col=col
		self.selected=False
		self.temp=0

	def draw(self, win):
		fnt = pygame.font.SysFont("comicsans", 36)

		gap = 540 / 9
		x = self.col * gap
		y = self.row * gap

		if self.value == 0:
			text = fnt.render(str(self.temp), 1, (128,128,128))
			win.blit(text, (x+5, y+5))
		if not(self.value == 0):
			text = fnt.render(str(self.value), 1, (0, 0, 0))
			win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

		if self.selected:
			pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

	def set(self, val):
		self.value = val

	def set_temp(self, val):
		self.temp = val