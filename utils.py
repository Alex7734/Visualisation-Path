import pygame
import math
import time
from queue import PriorityQueue
from pygame_widgets import Button, Slider, TextBox

# THIS IS WHAT EVERY SQUARE OF THE GRID WILL BE
# BEEING ABLE TO USE AN OBJECT FOR THIS MATTER IS GOOD DUE TO MORE REASONS
# 1. I CAN INITIALIZE EACH SQUARE WITH ATRIBUTES THAT I WILL ALWAYS NEED
# 2. I CAN WRITE METHODS THAT CHANGE OR CHECK FOR THE SQUARE'S STATE
# 3. THE CODE IS MORE ORGANISED

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
		if self.row < self.all_rows - 1 and not grid[self.row + 1][self.column].is_blocked(): 
			self.neighbors.append(grid[self.row + 1][self.column])

		if self.row > 0 and not grid[self.row - 1][self.column].is_blocked():
			self.neighbors.append(grid[self.row - 1][self.column])

		if self.column < self.all_rows - 1 and not grid[self.row][self.column + 1].is_blocked():
			self.neighbors.append(grid[self.row][self.column + 1])

		if self.column > 0 and not grid[self.row][self.column - 1].is_blocked():
			self.neighbors.append(grid[self.row][self.column - 1])

# THE FOLLOWING FUNCTIONS ARE NOTHING MORE THAN HELPER FUNCTIONS 
# THEIR USE RANGES FROM DRAWING AND MAKING THE GRID TO ALGORITHMS RELATED NEEDS

# THIS FUNCTION WILL HELP MY gui.py APP KNOW WHAT ELEMENT ON THE SCREEN I CLICKED
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos
	row = y // gap 
	col = x // gap
	return row, col

# THIS FUNCTION IS JUST CALCULATING THE MANHATTAN DISTANCE BETWEEN TWO POINTS
def manhattan_distance(a, b):
	x1, y1 = a
	x2, y2 = b
	return abs(x1 - x2) + abs(y1 - y2)

# THIS FUNCTION IS USED TO RECONSTRUCT THE PATH FROM THE END NODE TO THE START NODE
# I USED A SIMPLE BACKTRACKING LIKE ALGORITHM AND I UPDATE THE SCREEN DEPENDING ON 
# HOW BIG THE GRID IS, SO THAT THE USER DOESN'T HAVE TO WAIT A LOT IN SOME CASES BUT
# HE CAN STILL SEE HOW THE PATH IS RECONSTRUCTED
def reconstruct_path(came_from, current, draw, size, grid, start):
	# NOTE THAT THERE IS ONE BUG IN HERE WHEN REDOING THE PATH THE START SQUARE IS REWRITTEN
	while current in came_from:
		current = came_from[current]
		current.make_path()
		start.make_start()
		if size<11:
			time.sleep(0.1)
		elif size<20:
			time.sleep(0.05)
		else:
			time.sleep(0.01)
		draw()
		pygame.display.update()
	# After waiting some time I will clear the open and closed squares 
	# that the app uses to show how the path is found. I had a big thought
	# before doing this as I was not totally sure wheather this is going to be
	# a good feature or not but knowing the user has a great control of the visualiser
	# I decided that just showing the path is a good thing! 
	time.sleep(0.5)
	for row in grid:
		for node in row:
			if node.is_closed() or node.is_open():
				node.reset()

# THIS FUNCTION GENERATES THE GRID DEPENDING ON THE NUMBER OF ROWS
def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i,j,gap,rows)
			grid[i].append(node)
	return grid

# THIS FUNCTION DRAWS THE GRID TO THE SCREEN
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, (0,100,128), (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, (0, 100, 128), (j * gap, 0), (j * gap, width))

# THIS FUNCTION REDRAWS EVRY ELEMENT WHEN CALLED
def draw(win, grid, rows, width):
	for row in grid:
		for node in row:
			node.draw(win)
	draw_grid(win, rows, width)

# FUNCTION CHECK THE BUTTON PRESSED FOR CHOSING THE ALGORITHM
def choseAlgo(x, y):
	global chosenAlgo
	if 53<x<192:
		if 157<y<197:
			chosenAlgo = "A*"
		if 204<y<247:
			chosenAlgo = "A*M"
		if 253<y<290:
			chosenAlgo = "Dijkstra"
			print(chosenAlgo)
		if 300<y<338:
			chosenAlgo = "DijkstraM"
	return chosenAlgo
