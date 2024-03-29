#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True  # prevent __pycache__ creation
from models import *

old_key = None

"""Initialize the game state"""
running = 1
dragging = 0
offset = (0, 0)
clock = pygame.time.Clock()

"""Main game loop"""
while running:
    clock.tick(30)  # Refresh rate control

    """Event handling loop"""
    for event in pygame.event.get():
        if event.type == QUIT:  # Check for quit event (click on red cross or press Esc key)
            top.buttons[5].autosave()  # call autosave function
            running = 0  # quit the program

        elif event.type == KEYUP:  # when a key is released
            tab.handle_key_input(event.key)  # handle user input to change RGB values
            tab.process_tab(screen)  # change appearance of the tab

        elif event.type == KEYDOWN:  # when a key is pressed down
            keys = pygame.key.get_pressed()  # get the keys
            if (keys[K_LCTRL] or keys[K_RCTRL]) and keys[K_z]:
                top.buttons[4].sub_buttons[0].function()  # call undo
            elif (keys[K_LCTRL] or keys[K_RCTRL]) and keys[K_y]:
                top.buttons[4].sub_buttons[1].function()  # call redo

        elif event.type == MOUSEBUTTONDOWN:  # when user presses mouse button
            mouse_x, mouse_y = event.pos
            if mouse_x < grid.width and not top.hover(mouse_x, mouse_y):
                """not on tab or top menu then start dragging"""
                dragging = 1
                grid.dragging = 1

        elif event.type == MOUSEBUTTONUP:  # Check for mouse button click event
            mouse_x, mouse_y = event.pos
            if event.button == 1:
                click = 0
                click = top.click(mouse_x, mouse_y)
                tab.menu.click(mouse_x - grid.width, mouse_y)
                if not click:
                    if mouse_x > grid.width:
                        grid.selected_tile = tab.click(mouse_x - grid.width, mouse_y)
                    else:
                        if tab.selected_tab == 1:  # map
                            grid.old_index = None
                            grid.click(mouse_x, mouse_y, offset)
                        elif tab.selected_tab == 2:  # tiles
                            grid.set_color(mouse_x, mouse_y, tab.selected_color, screen)
                        elif tab.selected_tab == 5:  # entities
                            grid.new_entity(mouse_x, mouse_y)
                        elif tab.selected_tab == 6:  # events
                            grid.new_event(mouse_x, mouse_y)
                        grid.allow_process = 1
            elif event.button == 3:  # right click
                grid.delete_entity_or_event(*event.pos)

            elif event.button == 4:  # scroll down
                tab.update_scroll(32)
            elif event.button == 5:  # scroll up
                tab.update_scroll(-32)
            dragging = 0
            grid.dragging = 0

        elif event.type == MOUSEMOTION:  # Check for mouse motion event
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
                    grid.offset = offset
                    grid.allow_process = 1
            top.hover(mouse_x, mouse_y)
            tab.menu.hover(mouse_x - grid.width, mouse_y)

        elif event.type == VIDEORESIZE:  # Check for window resize event
            tab.process_tab(screen)
            grid.allow_process = 1

    if grid.allow_process:
        grid.process_surface(screen, offset)
        grid.allow_process = 0

    draw_screen(screen, tab, grid, top)

pygame.quit()  # Quit Pygame when the game loop exits
