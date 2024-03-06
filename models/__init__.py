from os import system

from models.tab import *  # import models
from models.main_screen import *
from models.menu_class import menu_class

from utils.functions import get_tile, load_tiles, draw_screen
from utils.popups import popup

import pygame                   # import pygame and variables
from pygame.locals import *

pygame.init()                   # initialize pygame library

screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)  # create the screen
pygame.display.set_caption("RPG Map Builder")

system("clear")  # clear terminal (linux)

top = menu_class("top_menu", screen)  # create menu object
top.create_top_menu()  # initialize the top menu
top.buttons[-1].radius_bottom_right = 10  # round the bottom right corner

tab = tab_class(screen)  #initialize tab and grid
grid = main_screen(screen)

tab.grid = grid  # give access point to grid in tab class
grid.tab = tab  # and vice versa

button_class.grid = grid  # give access point to grid tab and top in button_class
button_class.tab = tab
button_class.top = top
