from models.drop_down_menu import * #import models
from models.submenus import *
from models.tab_menus import *
from models.main_screen import *

import pygame                   #import pygame and variables
from pygame.locals import *

pygame.init()                   #initialise pygame library

screen = pygame.display.set_mode((800,600), pygame.RESIZABLE) #create the screen

from os import system           #clear terminal (linux)
system("clear")


list = []               #create a list of drop_down menus
list.append(drop_down_menu("Project", ["New", "Load", "Save"]))
list.append(drop_down_menu("Map", ["New", "Load", "Save"]))
list.append(drop_down_menu("Play", ["This map", "That map"]))
list.append(drop_down_menu("Help", []))

tab = tab_menu_class(screen)
grid= main_screen(screen)
