import pygame
from utils import make_grid, Node, get_clicked_pos, draw
from algorithm import aStar_algorithm, Dijkstra_algorithm, generate_walls, bfs
from pygame_widgets import Button, Slider, TextBox, ButtonArray
import time

# INIT THE PYGAME WINDOW
pygame.init()
WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Visualiser")
chosenAlgo = "A*"

# FUNCTION CHECK THE BUTTON PRESSED FOR CHOSING THE ALGORITHM
def choseAlgo(x, y):
	global chosenAlgo
	if 53<x<192:
		if 157<y<197:
			chosenAlgo = "A*"
		if 204<y<247:
			chosenAlgo = "BFS"
		if 253<y<290:
			chosenAlgo = "Dijkstra"
			print(chosenAlgo)
		if 300<y<338:
			chosenAlgo = "DijkstraM"
	return chosenAlgo


# THIS FUNCTION IS THE ACTUAL ALGORITHM VISUALISATION TOOL
# IT TAKES IN THE WINDOW WIDTH AND THE AMMOUNT OF ROWS ENTERED IN THE MAIN MENU
# LISTENS FOR ALL THE EVENTS AND CALLS THE ALGORITHM FUNCTION WHEN CONDITIONS ARE MET
def main(win, width, ROWS=30):
	# initial values are created
	ROWS = slider.getValue()
	if ROWS >25 and ROWS % 2 == 0 and ROWS != 40:
		ROWS += 1
	grid = make_grid(ROWS, width)
	start = None
	end = None
	run = True
	if chosenAlgo == "A*M" or chosenAlgo == "DijkstraM":
		generate_walls(lambda:draw(win, grid, ROWS, width), grid, len(grid), start, end)
	# this while run is here to make the pygame window run untill you close it
	while run:
		events = pygame.event.get()
		draw(win, grid, ROWS, width)
		pygame.display.update()
		# the event listening is all made here
		for event in pygame.event.get():
			# the quit event that reroutes you back to the main_menu function 
			# NOTE THIS FUNCTION IS CALLED FROM WITHIN THE MAIN_MENU FUNCTION THAT IS WHY THIS WORKS
			if event.type == pygame.QUIT:
				run = False
			# event call for LMB, it draws either a start or an end or a block
			if pygame.mouse.get_pressed()[0]: 
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
			# event call for MMB, it clears the path found in the prev run
			elif pygame.mouse.get_pressed()[1]:
				for row in grid:
					for node in row:
						if node.is_path():
							node.reset()

			# event call RMB, deleting any block clicked on 
			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None

			# event listener for KEYBOARD press
			if event.type == pygame.KEYDOWN:
				# if SPACE is pressed than run the A* algorithm 
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							if node.is_closed() or node.is_open() or node.is_path(): 
								node.reset()
					for row in grid:
						for node in row:
							node.update_neighbors(grid)

					if chosenAlgo == "A*":
						aStar_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
					if chosenAlgo == "BFS":
						bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
					elif chosenAlgo == "Dijkstra" or chosenAlgo == "DijkstraM":
						Dijkstra_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)


				# if c in pressed than clear the current grid
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

# THESE ARE THE PYGAME_WIDGETS MODULE ELEMENTS
# THE BUTTON SLIDER AND TEXTBOX ARE ALL FROM THAT LIBRARY
# I JUST INITIALIZED THEM WITH MY OWN VALLUEs
button = Button(
            WIN, 260, 250, 270, 80, text='Generate',
            fontSize=50, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=main,
			onClickParams=(WIN, WIDTH)
        )
slider = Slider(WIN, 250, 180, 180, 40, 
				min=5, max=40, step=1, 
				handleColour=(255, 0, 0), handleRadius=22
			)
output = TextBox(WIN, 460, 180, 110, 40, fontSize=20)
buttonArray = ButtonArray(WIN, 50, 150, 150, 200, (1, 4),
                          border=5, texts=('A*', 'BFS', 'Dijkstra', 'Dijkstra & Maze'), 
                         )

# THIS PART TAKES CARE OF THE TITLE THAN SHIFTS THE FONT TO NORMAL TEXT
font = pygame.font.Font('freesansbold.ttf', 56) 
text = font.render('PATH VISUALISER', True, (255, 0, 0)) 
textRect = text.get_rect()  
textRect.center = (300, 50)
font = pygame.font.Font('freesansbold.ttf', 16) 

# THIS WHOLE BLOCK OF CODE IS JUST THE CONTROLS TEXT IN THE MAIN MENU
small_text1 = font.render("EXIT visualiser --> back to home screen | SPACE --> run algorithm", True, (255, 0, 0))
small_textRect1 = small_text1.get_rect()
small_textRect1.center = (300,450) 
small_text2 = font.render("LMB --> draw blocks and points | RMB --> delete blocks and points ", True, (255, 0, 0))
small_textRect2 = small_text2.get_rect()
small_textRect2.center = (300, 475) 
small_text3 = font.render("MMB --> clear algorithm | c --> hard reset", True, (255, 0, 0))
small_textRect3 = small_text3.get_rect()
small_textRect3.center = (300, 500) 

# THIS BLOCK OF CODE IS JUST THE INFORMATIVE COLORED TEXT AT THE BOTTOM OF THE MAIN MENU PAGE
font = pygame.font.Font('freesansbold.ttf', 12)  
algo_text1 = font.render("START", True, (255, 165 ,0))
algo_textRect1 = algo_text1.get_rect()
algo_textRect1.center = (120, 575) 
algo_text2 = font.render("END", True, (255, 255, 0))
algo_textRect2 = algo_text2.get_rect()
algo_textRect2.center = (480, 575) 
algo_text3 = font.render("BLOCKED", True, (0, 0, 0))
algo_textRect3 = algo_text3.get_rect()
algo_textRect3.center = (300, 575) 
algo_text4 = font.render("VISITED", True, (255, 0, 0))
algo_textRect4 = algo_text4.get_rect()
algo_textRect4.center = (200, 575) 
algo_text5 = font.render("IN QUEUE", True, (0, 255, 0))
algo_textRect5 = algo_text5.get_rect()
algo_textRect5.center = (400, 575) 

# THIS IS THE MAIN FUNCTION THAT GETS CALLED IN ORDER TO PUT THE APP IN FUNCTION
# IT'S A GUI INTERFACE THAT TAKES IN INPUT FROM THE USER AND SENDS IT TO THE MAIN FUNCTION
# AFTER THAT THE MAIN FUNCTION TAKES CONTROL OF EVRYTHING SO THIS MENU IS JUST FOR SELECTION
# THE SIZE OF THE GRID
def main_menu(win, width):
	# unlike the other function here i don't need a variables 
	# as this will be run until the screen is closed
	while True:
		events = pygame.event.get()
		# this string will be the output text of my TextBox widget
		output_text = str(slider.getValue()) + 'x' + str(slider.getValue()) + ' GRID'
		for event in events:
			# the only event possible here is a quit one
			if event.type == pygame.QUIT:
				pygame.quit()
				run = False
				quit()
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				choseAlgo(pos[0], pos[1])

		# put all the text and color on the screen
		win.fill((50, 50, 50))
		win.blit(text, textRect)
		win.blit(algo_text1, algo_textRect1)
		win.blit(algo_text2, algo_textRect2)
		win.blit(algo_text3, algo_textRect3)
		win.blit(algo_text4, algo_textRect4)
		win.blit(algo_text5, algo_textRect5)
		win.blit(small_text1, small_textRect1)
		win.blit(small_text2, small_textRect2)
		win.blit(small_text3, small_textRect3)

		# draw all the widgets
		button.listen(events)
		button.draw()
		slider.listen(events)
		slider.draw()
		output.setText(output_text)
		output.draw()
		buttonArray.listen(events)
		buttonArray.draw()
		pygame.display.update()


