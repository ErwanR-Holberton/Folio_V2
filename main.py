#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True  #prevent __pycache__ creation
from models import *

top = menu_class("top_menu")
top.create_top_menu()
top.buttons[-1].radius_br = 10

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
            tab.handle_key_input(event.key)
            tab.calculate(screen)

        elif event.type == MOUSEBUTTONUP: # Check for mouse button click event
            mouse_x, mouse_y = event.pos
            click, name = 0, None
            click, name = top.click(mouse_x, mouse_y)
            tab.menu.click(mouse_x - grid.width, mouse_y)
            if not click:
                if mouse_x > grid.width:
                    grid.selected_tile = tab.click(mouse_x - grid.width, mouse_y)
                else:
                    if tab.selected_tab == 1:
                        grid.click(mouse_x, mouse_y)
                    grid.calculate(screen)

        elif event.type == MOUSEMOTION: # Check for mouse motion event
            mouse_x, mouse_y = event.pos
            top.hover(mouse_x, mouse_y)
            tab.menu.hover(mouse_x - grid.width, mouse_y)

        elif event.type == VIDEORESIZE: # Check for window resize event
            tab.calculate(screen)
            grid.calculate(screen)

    screen.fill((255, 255, 255))  #Fill the screen with a white background

    # Draw the menus tab and grid
    tab.draw(screen)
    grid.draw(screen)

    # Draw menus and submenus
    for button in top.buttons:
        button.draw(screen)

    pygame.display.flip() # Refresh the display

pygame.quit() # Quit Pygame when the game loop exits
