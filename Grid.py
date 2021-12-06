import pygame
from Cube import Cube
import time
import copy
from sudoku_enzo import verif_grid, solve_sudoku, brute_force

class Grid:
	grid=[[0, 0, 0, 0, 5, 1, 7, 0, 3],
		[0, 0, 0, 0, 0, 0, 6, 4, 9],
		[0, 0, 4, 0, 6, 0, 0, 1, 2],
		[0, 0, 0, 9, 0, 4, 1, 7, 0],
		[0, 0, 1, 6, 0, 7, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 6],
		[0, 0, 2, 0, 9, 6, 0, 0, 0],
		[8, 0, 0, 1, 0, 2, 0, 0, 4],
		[9, 0, 7, 0, 0, 0, 3, 0, 0]]

	# grid=[[0, 0, 6, 0, 0, 0, 1, 0, 7],
	# 	[0, 0, 0, 0, 0, 1, 8, 5, 0],
	# 	[5, 7, 0, 0, 0, 9, 0, 0, 0],
	# 	[0, 4, 7, 0, 8, 3, 0, 0, 2],
	# 	[0, 2, 0, 6, 0, 0, 0, 7, 9],
	# 	[0, 0, 9, 2, 0, 7, 6, 3, 8],
	# 	[0, 0, 0, 0, 0, 0, 0, 2, 0],
	# 	[0, 1, 5, 0, 0, 0, 0, 0, 4],
	# 	[0, 8, 0, 1, 0, 4, 9, 0, 0]]

	# grid=[[4, 6, 0, 9, 0, 8, 0, 3, 0],
	# 		[3, 0, 7, 6, 4, 0, 0, 8, 5],
	# 		[9, 8, 2, 0, 5, 3, 0, 6, 7],
	# 		[2, 0, 0, 5, 1, 4, 8, 0, 0],
	# 		[8, 9, 0, 0, 3, 7, 0, 0, 6],
	# 		[5, 4, 0, 0, 9, 6, 0, 0, 0],
	# 		[0, 2, 8, 4, 0, 5, 3, 0, 0],
	# 		[6, 5, 9, 3, 0, 1, 2, 7, 0],
	# 		[0, 0, 0, 7, 2, 9, 6, 0, 0]]

	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.cubes = [[Cube(self.grid[i][j], i, j) for j in range(cols)] for i in range(rows)]
		self.model = None
		self.selected = None
		self.difficulty="N/A"
		self.nb_solution="N/A"
		self.time="N/A"
		self.evaluate()

	def update_model(self):
		self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

	def place(self, val):
		row, col = self.selected
		if self.cubes[row][col].value == 0:
			self.cubes[row][col].set(val)
			self.update_model()
			if self.valid(val, row, col):
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

		fnt = pygame.font.SysFont("default", 20)
		text = fnt.render("Difficulté : "+self.difficulty, 1, (0, 0, 0))
		win.blit(text, (25, 545))
		text = fnt.render("Temps de résolution : "+str(self.time), 1, (0, 0, 0))
		win.blit(text, (25, 560))
		text = fnt.render("Nombre solutions : "+str(self.nb_solution), 1, (0, 0, 0))
		win.blit(text, (25, 575))

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

	def valid(self,val, row, col):
		copy_grid=copy.deepcopy(self.model)
		copy_grid[row][col]=val
		return verif_grid(copy_grid) and solve_sudoku(copy_grid)

	def solve(self):
		self.update_model()
		copy_grid=copy.deepcopy(self.model)
		res=solve_sudoku(copy_grid)
		self.grid=copy_grid
		self.cubes = [[Cube(self.grid[i][j], i, j) for j in range(9)] for i in range(9)]
		return res

	def evaluate(self):
		self.update_model()
		copy_grid=copy.deepcopy(self.model)
		solutions=brute_force(copy_grid)
		print(copy_grid)
		print(solutions)
		start=time.time()
		copy_grid_force=copy.deepcopy(self.model)
		res=solve_sudoku(copy_grid_force)
		end=time.time()
		# print("La résolution de la grille a pris {:.3f}".format(end - start) + " secondes.")
		# print("Il y a : " + str(solutions) + " solutions.")
		if (solutions > 1):
			if ((end-start)>5):
				self.difficulty="difficile"
			else:
				self.difficulty="moyenne"
			self.nb_solution=solutions
			self.time="{:.3f}".format(end - start)
		elif (solutions==1):
			if ((end-start) > 5):
				self.difficulty="moyenne"
			else:
				self.difficulty="facile"
			self.difficulty="facile"
			self.nb_solution=solutions
			self.time="{:.3f}".format(end - start)
		if (str(self.time) == '0.000'):
			self.time = '0.001'