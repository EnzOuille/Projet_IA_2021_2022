import pygame
from Cube import Cube

class Grid:
	grid=[[0, 1, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 3, 0, 1, 0, 0, 8, 0],
		[9, 0, 0, 8, 6, 3, 0, 0, 5],
		[0, 5, 0, 0, 9, 0, 6, 0, 0],
		[1, 3, 0, 0, 0, 0, 2, 5, 0],
		[0, 0, 0, 0, 0, 0, 0, 7, 4],
		[0, 0, 5, 2, 0, 6, 3, 0, 0]]

	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.cubes = [[Cube(self.grid[i][j], i, j) for j in range(cols)] for i in range(rows)]
		self.model = None
		self.selected = None

	def update_model(self):
		self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

	def place(self, val):
		row, col = self.selected
		if self.cubes[row][col].value == 0:
			self.cubes[row][col].set(val)
			self.update_model()
			"""
			|||
			vvv INSERT HERE THE ALGO (replace valid) <--
			"""
			if valid(self.model, val, (row,col)) and solve(self.model):
				return True
			else:
				self.cubes[row][col].set(0)
				self.cubes[row][col].set_temp(0)
				self.update_model()
				return False

	def sketch(self, val):
		row, col = self.selected
		self.cubes[row][col].set_temp(val)

	def draw(self, win):
		gap = 540 / 9
		for i in range(self.rows+1):
			if i % 3 == 0 and i != 0:
				thick = 4
			else:
				thick = 1
			pygame.draw.line(win, (0,0,0), (0, i*gap), (540, i*gap), thick)
			pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, 540), thick)

		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j].draw(win)

	def select(self, row, col):
		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j].selected = False

		self.cubes[row][col].selected = True
		self.selected = (row, col)

	def clear(self):
		row, col = self.selected
		if self.cubes[row][col].value == 0:
			self.cubes[row][col].set_temp(0)

	def click(self, pos):
		if pos[0] < 540 and pos[1] < 540:
			gap = 540 / 9
			x = pos[0] // gap
			y = pos[1] // gap
			return (int(y),int(x))
		else:
			return None

	def is_finished(self):
		for i in range(self.rows):
			for j in range(self.cols):
				if self.cubes[i][j].value == 0:
					return False
		return True