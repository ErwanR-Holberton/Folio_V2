#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True  #prevent __pycache__ creation
from models import *

top = menu_class("top_menu")
top.create_top_menu()

"""Initialize the game state"""
running = 1

"""Main game loop"""
while running:

    """Event handling loop"""
    for event in pygame.event.get():
        if event.type == QUIT: # Check for quit event (click on red cross or press Esc key)
            running = 0

        elif event.type == KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = 0

        elif event.type == MOUSEBUTTONUP: # Check for mouse button click event
            mouse_x, mouse_y = event.pos
            top.click(mouse_x, mouse_y)
            """for menu in list:
                menu.state = 0
                menu.test_click(mouse_x, mouse_y)"""
            if mouse_x > grid.width:
                grid.selected_tile = tab.click(mouse_x - grid.width, mouse_y)
            else:
                grid.click(mouse_x, mouse_y)
                grid.calculate(screen)

        elif event.type == MOUSEMOTION: # Check for mouse motion event
            mouse_x, mouse_y = event.pos
            top.hover(mouse_x, mouse_y)
            """for menu in list:
                if menu.state != 1: # Change menu color if hovered
                    if menu.test_hover(mouse_x, mouse_y):
                        menu.color = (160, 160, 160)
                    else:
                        menu.color = (150, 150, 150)
            for button in tab.menu:
                if button.state != 1: # Change tab button color if hovered
                    if button.test_hover(mouse_x - grid.width, mouse_y):
                        button.color = (160, 160, 160)
                        tab.calculate(screen)
                    else:
                        button.color = (150, 150, 150)
                        tab.calculate(screen)"""


        elif event.type == VIDEORESIZE: # Check for window resize event
            tab.calculate(screen)
            grid.calculate(screen)

    screen.fill((255, 255, 255))  #Fill the screen with a white background

    # Draw the tab and grid
    tab.draw(screen)
    grid.draw(screen)

    # Draw menus and submenus
    for button in top.buttons:
        button.draw(screen)
        """if menu.state == 1:
            menu.draw_submenus(screen)"""

    pygame.display.flip() # Refresh the display

pygame.quit() # Quit Pygame when the game loop exits
