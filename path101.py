import pygame
import math
import time
from queue import PriorityQueue
from pygame_widgets import Button, Slider, TextBox

def write():
    x = slider.getValue()
    print(x)

# pygame init
pygame.init()
WIDTH = 600
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path 101")

slider = Slider(WIN, 50, 630, 300, 30, min=1, max=50, step=1)
output = TextBox(WIN, 380, 630, 30, 30, fontSize=18)

class Node:
	def __init__(self, row, column, width, all_rows):
		self.row = row
		self.column = column
		self.x = row * width
		self.y = column * width
		self.color = (64, 224, 208)
		self.neighbors = []
		self.width = width
		self.all_rows = all_rows

	# IT TOOK ME LIKE A WEEK TO SEARCH FOR THIS STUFF
	def __lt__(self, other):
		return False

	def is_open(self):
		return self.color == (0, 255, 0)

	def is_closed(self):
		return self.color == (255, 0, 0)

	def is_blocked(self):
		return self.color == (0, 0, 0)

	def is_path(self):
		return self.color == (255, 255, 255)

	def start(self):
		return self.color == (255, 165 ,0)

	def end(self):
		return self.color == (255, 255, 0)

	def reset(self):
		self.color = (64, 224, 208)

	def make_open(self):
		self.color = (0, 255, 0)

	def make_closed(self):
		self.color = (255, 0, 0)

	def make_blocked(self):
		self.color = (0, 0, 0)

	def make_start(self):
		self.color = (255, 165 ,0)

	def make_end(self):
		self.color = (255, 255, 0)

	def make_path(self):
		self.color = (255, 255, 255)

	def get_pos(self):
		return self.row, self.column

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.all_rows - 1 and not grid[self.row + 1][self.column].is_blocked(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.column])

		if self.row > 0 and not grid[self.row - 1][self.column].is_blocked(): # UP
			self.neighbors.append(grid[self.row - 1][self.column])

		if self.column < self.all_rows - 1 and not grid[self.row][self.column + 1].is_blocked(): # RIGHT
			self.neighbors.append(grid[self.row][self.column + 1])

		if self.column > 0 and not grid[self.row][self.column - 1].is_blocked(): # LEFT
			self.neighbors.append(grid[self.row][self.column - 1])

# THIS IS FOR A* MATH PART
def manhattan_distance(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

# THIS IS GOING BACK AND MAKING THE PATH
def reconstruct_path(came_from, current, draw, size):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		if size<11:
			time.sleep(0.2)
		elif size<20:
			time.sleep(0.1)
		else:
			time.sleep(0.02)
		draw()
		pygame.display.update()

# JUST MAKING THAT GRID
def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i,j,gap,rows)
			grid[i].append(node)
	return grid

# SHOW THE GRID
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, (0,100,128), (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, (0, 100, 128), (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
	for row in grid:
		for node in row:
			node.draw(win)
	draw_grid(win, rows, width)

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos
	row = y // gap 
	col = x // gap
	return row, col

def aStar_algorithm(draw, grid, start, end):
	# INIT OF A* ALGO
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	a_score = {node: float("inf") for row in grid for node in row}
	a_score[start] = 0
	b_score = {node: float("inf") for row in grid for node in row}
	b_score[start] = manhattan_distance(start.get_pos(), end.get_pos())
	open_set_hash = {start}

	# ACTUALLY APPLY ALGO

	while not open_set.empty():
		# PYGAME CHECK FOR QUIT
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		# SET NODE 
		current = open_set.get()[2]
		open_set_hash.remove(current)

		# IF I FOUND THE END STOP
		if current == end:
			reconstruct_path(came_from, end, draw,	len(grid))
			end.make_end()
			start.make_start()
			return True

		# A STAR MAKING THE DECISION 
		for neighbor in current.neighbors:
			temp_a_score = a_score[current] + 1

			if temp_a_score < a_score[neighbor]:
				came_from[neighbor] = current
				a_score[neighbor] = temp_a_score
				b_score[neighbor] = temp_a_score + manhattan_distance(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((b_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()
		pygame.display.update()
		if len(grid)<11:
			time.sleep(0.2)
		elif len(grid)<20:
			time.sleep(0.1)
		else:
			time.sleep(0.02)
		draw()

		if current != start:
			current.make_closed()

	return False


def main(win, width, ROWS=30):
	ROWS = slider.getValue()
	grid = make_grid(ROWS, width)
	start = None
	end = None
	print (ROWS)
	run = True
	while run:
		events = pygame.event.get()

		#slider.listen(events)
		#slider.draw()
		#output.setText(slider.getValue())
		#output.draw()

		draw(win, grid, ROWS, width)
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if pygame.mouse.get_pressed()[0]: # LEFT
				try:
					pos = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos, ROWS, width)
					node = grid[row][col]
					if not start and node != end:
						start = node
						start.make_start()

					elif not end and node != start:
						end = node
						end.make_end()

					elif node != end and node != start:
						node.make_blocked()
				except:
					continue

			elif pygame.mouse.get_pressed()[1]:# MIDDLE
				for row in grid:
					for node in row:
						if node.is_closed() or node.is_open() or node.is_path():
							node.reset()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							if node.is_closed() or node.is_open() or node.is_path(): 
								node.reset()
					for row in grid:
						for node in row:
							node.update_neighbors(grid)

					aStar_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

				if event.key == pygame.K_UP:
					for row in grid:
						for node in row:
							node.reset()
							start = None
							end = None

button = Button(
            WIN, 100, 350, 200, 100, text='Submit',
            fontSize=50, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=main,
			onClickParams=(WIN, WIDTH)
         )
slider = Slider(WIN, 100, 200, 300, 40, min=2, max=50, step=1)
output = TextBox(WIN, 475, 200, 50, 50, fontSize=30)
font = pygame.font.Font('freesansbold.ttf', 64) 
text = font.render('PATH 101', True, (255, 0, 0)) 
small_text= font.render("Best pathfinding algortihm \n visualisation tool ever used!", True, (255, 0, 0))
textRect = text.get_rect()  
textRect.center = (300, 50)

def main_menu(win, width):
	x = 50
	while True:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				run = False
				quit()

		win.fill((0, 0, 0))

		win.blit(text, textRect)
		button.listen(events)
		button.draw()
		slider.listen(events)
		slider.draw()
		output.setText(slider.getValue())
		output.draw()
		X = slider.getValue()

		pygame.display.update()


main_menu(WIN, WIDTH)