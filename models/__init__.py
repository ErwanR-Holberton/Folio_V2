from models.tab import * #import models
from models.main_screen import *
from functions import get_tile, load_tiles
from models.menu_class import menu_class

import pygame                   #import pygame and variables
from pygame.locals import *

pygame.init()                   #initialise pygame library

screen = pygame.display.set_mode((1200,800), pygame.RESIZABLE) #create the screen

from os import system           #clear terminal (linux)
system("clear")




tab = tab_class(screen)
"""create an instance of tab_class with screen argument"""
grid = main_screen(screen)
"""create an instance of main_screen with screen argument"""
tab.grid = grid
"""give access point to grid in tab class"""
button_class.grid = grid
"""give access point to grid in button_class"""
