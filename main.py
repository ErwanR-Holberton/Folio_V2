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

    """Event handling loop"""
    for event in pygame.event.get():
        start = pygame.time.get_ticks()
        if event.type == QUIT: # Check for quit event (click on red cross or press Esc key)
            running = 0

        elif event.type == KEYUP:
            print (event.type, "KEYUP")
            if event.key == pygame.K_ESCAPE:
                running = 0
            tab.handle_key_input(event.key)
            tab.calculate(screen)

        elif event.type == MOUSEBUTTONDOWN:
            print (event.type, "BUTTONDOWN")
            mouse_x, mouse_y = event.pos
            if mouse_x < grid.width and not top.hover(mouse_x, mouse_y):
                dragging = 1

        elif event.type == MOUSEBUTTONUP: # Check for mouse button click event
            print (event.type, "BUTTONUP")
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
                        grid.calculate(screen)
            dragging = 0


        elif event.type == MOUSEMOTION: # Check for mouse motion event
            print (event.type, "MOTION")
            mouse_x, mouse_y = event.pos
            if dragging == 1:
                if event.buttons[0] and mouse_x < grid.width:
                    if not(top.hover(mouse_x, mouse_y)):
                        """if not click on top menu"""
                        key_index = grid.click(mouse_x, mouse_y, offset)
                        if key_index is not None and key_index != old_key:
                            grid.calculate(screen, offset)
                            old_key = key_index

                elif event.buttons[2]:
                    offset = (offset[0] + event.rel[0], offset[1] + event.rel[1])
                    grid.calculate(screen, offset)
            top.hover(mouse_x, mouse_y)
            tab.menu.hover(mouse_x - grid.width, mouse_y)

        elif event.type == VIDEORESIZE: # Check for window resize event
            print (event.type, "RESIZE")
            tab.calculate(screen)
            grid.calculate(screen)
        print (event.type, "time: ", pygame.time.get_ticks() - start)

    screen.fill((255, 255, 255))  #Fill the screen with a white background
    start = pygame.time.get_ticks()

    # Draw the menus tab and grid
    tab.draw(screen)
    grid.draw(screen)

    # Draw menus and submenus
    top.draw()

    pygame.display.flip() # Refresh the display
    print ("total time: ", pygame.time.get_ticks() - start)

pygame.quit() # Quit Pygame when the game loop exits
