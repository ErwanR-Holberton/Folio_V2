#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True  #prevent __pycache__ creation
from models import *

top = menu_class("top_menu")
top.create_top_menu()
top.buttons[-1].radius_bottom_right = 10
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
        if event.type == QUIT: # Check for quit event (click on red cross or press Esc key)
            running = 0

        elif event.type == KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = 0
            tab.handle_key_input(event.key)
            tab.calculate(screen)

        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            dragging = 1

        elif event.type == MOUSEBUTTONUP: # Check for mouse button click event
            mouse_x, mouse_y = event.pos
            if event.button == 1:
                click, name = 0, None
                click, name = top.click(mouse_x, mouse_y)
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
            mouse_x, mouse_y = event.pos
            if dragging == 1:
                if event.buttons[0]:
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
