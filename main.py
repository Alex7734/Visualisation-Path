import pygame
from gui import main_menu

# THIS FILE IS USED TO RUN THE APPLICATION ONLY 
# I PASS IN THE WIDTH AND WINDOW AND THAN CALL THE MAIN_MENU FUNCTION
# THIS FUNCTION HANDLES EVRYTHING AFTER THAT

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))

main_menu(WIN,WIDTH)