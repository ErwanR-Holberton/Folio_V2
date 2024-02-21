#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True  #prevent __pycache__ creation
from models import *

old_key = None

"""Initialize the game state"""
running = 1
dragging = 0
offset = (0, 0)
clock = pygame.time.Clock()

"""Main game loop"""
while running:
    clock.tick(30)
    """print(grid.tile_grid[0][0])"""

    """Event handling loop"""
    for event in pygame.event.get():
        start = pygame.time.get_ticks()
        if event.type == QUIT: # Check for quit event (click on red cross or press Esc key)
            """response = popup("Are you sure you want to quit? (yes or no)", "Quitting the app :(", grid, tab, top)
            if response == "yes":"""
            running = 0

        elif event.type == KEYUP:
            tab.handle_key_input(event.key)
            tab.process_tab(screen)

        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if mouse_x < grid.width and not top.hover(mouse_x, mouse_y):
                dragging = 1

        elif event.type == MOUSEBUTTONUP: # Check for mouse button click event
            mouse_x, mouse_y = event.pos
            if event.button == 1:
                click = 0
                click = top.click(mouse_x, mouse_y)
                tab.menu.click(mouse_x - grid.width, mouse_y)
                if not click:
                    if mouse_x > grid.width:
                        grid.selected_tile = tab.click(mouse_x - grid.width, mouse_y)
                    else:
                        if tab.selected_tab == 1:
                            grid.click(mouse_x, mouse_y, offset)
                        elif tab.selected_tab == 2:
                            grid.set_color(mouse_x, mouse_y, tab.selected_color, screen)
                        grid.allow_process = 1
            dragging = 0


        elif event.type == MOUSEMOTION: # Check for mouse motion event
            mouse_x, mouse_y = event.pos
            if dragging == 1:
                if event.buttons[0] and mouse_x < grid.width:
                    if not(top.hover(mouse_x, mouse_y)):
                        """if not click on top menu"""
                        if tab.selected_tab == 1:
                            key_index = grid.click(mouse_x, mouse_y, offset)
                            if key_index is not None and key_index != old_key:
                                grid.allow_process = 1
                                old_key = key_index
                        elif tab.selected_tab == 2:
                            grid.set_color(mouse_x, mouse_y, tab.selected_color, screen)
                            grid.allow_process = 1

                elif event.buttons[2]:
                    offset = (offset[0] + event.rel[0], offset[1] + event.rel[1])
                    grid.allow_process = 1
            top.hover(mouse_x, mouse_y)
            tab.menu.hover(mouse_x - grid.width, mouse_y)

        elif event.type == VIDEORESIZE: # Check for window resize event
            tab.process_tab(screen)
            grid.allow_process = 1
        """print (event.type, "time: ", pygame.time.get_ticks() - start)"""

    if grid.allow_process:
        grid.process_surface(screen, offset)
        grid.allow_process = 0
    screen.fill((255, 255, 255))  #Fill the screen with a white background
    start = pygame.time.get_ticks()

    # Draw the menus tab and grid
    tab.draw(screen)
    grid.draw(screen)

    # Draw menus and submenus
    top.draw()

    pygame.display.flip() # Refresh the display
    """print ("total time: ", pygame.time.get_ticks() - start)"""

pygame.quit() # Quit Pygame when the game loop exits
