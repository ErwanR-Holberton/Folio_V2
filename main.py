#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True  #prevent __pycache__ creation
from models import *


running = 1

while running:

    for event in pygame.event.get():    #main event loop
        if event.type == QUIT:          #if click on red cross
            running = 0

        elif event.type == KEYUP:             #if key is pressed
            if event.key == pygame.K_ESCAPE:
                running = 0

        elif event.type == MOUSEBUTTONUP: #if clicked
            mouse_x, mouse_y = event.pos
            for menu in list:
                menu.state = 0
                menu.test_click(mouse_x, mouse_y)
            for button in tab.menu:
                button.state = 0
                if button.test_click(mouse_x - grid.width, mouse_y):
                    if button.name == "Tiles":
                        tab.selected_tab = 1
                    if button.name == "Tools":
                        tab.selected_tab = 2
                    if button.name == "Settings":
                        tab.selected_tab = 3

            grid.click(mouse_x, mouse_y)
            grid.calculate(screen)

        elif event.type == MOUSEMOTION: #if moves
            mouse_x, mouse_y = event.pos
            for menu in list:
                if menu.state != 1:
                    if menu.test_hover(mouse_x, mouse_y):
                        menu.color = (160, 160, 160)
                    else:
                        menu.color = (150, 150, 150)
            for button in tab.menu:
                if button.state != 1:
                    if button.test_hover(mouse_x - grid.width, mouse_y):
                        button.color = (160, 160, 160)
                        tab.calculate(screen)
                    else:
                        button.color = (150, 150, 150)
                        tab.calculate(screen)


        elif event.type == VIDEORESIZE:
            tab.calculate(screen)
            grid.calculate(screen)

    screen.fill((255, 255, 255))  #fill the screen, everything after is drawing
    tab.draw(screen)
    grid.draw(screen)

    for menu in list:
        menu.draw(screen)
        if menu.state == 1:
            menu.draw_submenus(screen)

    pygame.display.flip()                               #refresh screen

pygame.quit() # Quit Pygame
