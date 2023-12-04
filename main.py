#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True  #prevent __pycache__ creation
from models import *


running = 1

while running:

    for event in pygame.event.get():    #main event loop
        if event.type == QUIT:          #if click on red cross
            running = 0

        elif event.type == KEYDOWN:             #if key is pressed
            if event.key == pygame.K_ESCAPE:
                running = 0

        elif event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            for menu in list:
                menu.state = 0
                menu.test_click(mouse_x, mouse_y)

        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            for menu in list:
                if menu.state != 1:
                    if menu.test_hover(mouse_x, mouse_y):
                        menu.color = (160, 160, 160)
                    else:
                        menu.color = (150, 150, 150)

        elif event.type == VIDEORESIZE:
            tab.calculate(screen)

    screen.fill((255, 255, 255))  #fill the screen, everything after is drawing

    for menu in list:
        menu.draw(screen)
        if menu.state == 1:
            menu.draw_submenus(screen)

    tab.draw(screen)


    pygame.display.flip()                               #refresh screen

pygame.quit() # Quit Pygame
