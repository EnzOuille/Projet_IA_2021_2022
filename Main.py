import pygame
from Grid import Grid


def redraw_window(win, board, strikes):
    win.fill((255,255,255))
    board.draw(win)

win=pygame.display.set_mode((540,600))
pygame.display.set_caption("Sudoku")
board = Grid(9, 9)
# board.evaluate()
key = None
run = True
strikes = 0
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				board=Grid(9,9)
				# board.evaluate()
			if event.key == pygame.K_s:
				board.solve()
			if event.key == pygame.K_1:
				key = 1
			if event.key == pygame.K_2:
				key = 2
			if event.key == pygame.K_3:
				key = 3
			if event.key == pygame.K_4:
				key = 4
			if event.key == pygame.K_5:
				key = 5
			if event.key == pygame.K_6:
				key = 6
			if event.key == pygame.K_7:
				key = 7
			if event.key == pygame.K_8:
				key = 8
			if event.key == pygame.K_9:
				key = 9
			if event.key == pygame.K_DELETE:
				board.clear()
				key = None
			if event.key == pygame.K_RETURN:
				i, j = board.selected
				if board.cubes[i][j].temp != 0:
					if board.place(board.cubes[i][j].temp):
						print("Success")
						board.evaluate()
					else:
						print("Wrong")
						strikes += 1
					key = None
					if board.is_finished():
						print("Game over")
						run = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			clicked = board.click(pos)
			if clicked:
				board.select(clicked[0], clicked[1])
				key = None

	if board.selected and key != None:
		board.sketch(key)
	redraw_window(win, board, strikes)
	pygame.display.update()
