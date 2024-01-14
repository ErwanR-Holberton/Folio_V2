from models.drop_down_menu import * #import models
from models.submenus import *
from models.tab import *
from models.main_screen import *
from models.tab_menus import *
from functions import get_tile, load_tiles

import pygame                   #import pygame and variables
from pygame.locals import *

pygame.init()                   #initialise pygame library

screen = pygame.display.set_mode((1200,800), pygame.RESIZABLE) #create the screen

from os import system           #clear terminal (linux)
system("clear")


list = []               #create a list of drop_down menus
list.append(drop_down_menu("Project", ["New", "Load", "Save"]))
list.append(drop_down_menu("Map", ["New", "Load", "Save"]))
list.append(drop_down_menu("Tile", ["New", "Edit", "Delete"]))
list.append(drop_down_menu("Edit", ["Undo", "Redo"]))
list.append(drop_down_menu("Help", []))

tab = tab_class(screen) 
"""create an instance of tab_class with screen argument"""
grid = main_screen(screen)
"""create an instance of main_screen with screen argument"""
tab.grid = grid
"""assign the value of grid to the grid attribute of tab instance"""