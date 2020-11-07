import pygame
import time
from queue import PriorityQueue
from utils import manhattan_distance, Node, reconstruct_path, draw

# THIS FUNCTION RUNS WHEN YOU PRESS SPACE IN THE VISUALISER 
# IT IS THE SOUL OF THIS APP AND IS THE ONE RESPONSIBLE FOR RUNNING
# THE WHOLE ALGORITHM
def aStar_algorithm(draw, grid, start, end):
	# pass the initial values
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	a_score = {node: float("inf") for row in grid for node in row}
	a_score[start] = 0
	b_score = {node: float("inf") for row in grid for node in row}
	b_score[start] = manhattan_distance(start.get_pos(), end.get_pos())
	open_set_hash = {start}

	# this while loop runs as long as we have squares to check
	while not open_set.empty():
		# check for quit event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		# if the current node is the end than reconstruct path and stop
		if current == end:
			end.make_end()
			reconstruct_path(came_from, end, draw,	len(grid), grid, start)
			end.make_end()
			start.make_start()
			return True

		# this is how we make the decision depending on the manhattan distace from start to end
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
		
		# refresh the screen after each iteration
		pygame.display.update()
		size = len(grid)
		if size<11:
			time.sleep(0.06)
		elif size<20:
			time.sleep(0.03)
		else:
			time.sleep(0.01)
		draw()

		if current != start:
			current.make_closed()

	return False
