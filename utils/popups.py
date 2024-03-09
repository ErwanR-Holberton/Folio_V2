import pygame
from pygame.locals import *

def popup(message, title, grid, tab, top, size=(400, 110), get_key=0):
    """create a popup loop"""
    from utils.functions import create_text_surface

    loop = 1

    popup = pygame.Surface(size, pygame.SRCALPHA)  # prepare popup suraface
    popup_rect = popup.get_rect(center=grid.surf.get_rect().center)
    popup.fill((10, 8, 50, 0))
    draw_popup(popup, size, title, message, get_key)

    answer = ""
    while loop:

        for event in pygame.event.get(): # handle events
            if event.type == QUIT: # Check for quit event
                loop = 0

            elif event.type == MOUSEBUTTONUP: # Check for mouse button click event
                mouse_x, mouse_y = event.pos

                mouse_x -= popup_rect.topleft[0]  # adjust coordinates
                mouse_y -= popup_rect.topleft[1]  # relative to the popup

                if mouse_x >= size[0] - 28 and mouse_x <= size[0] -8:
                    if mouse_y >= 0 and mouse_y <= 15:  # if click on red cross
                        loop = 0                        # quit

            elif event.type == WINDOWRESIZED:
                """process and draw when size changes"""
                grid.process_surface(grid.screen)
                grid.draw(grid.screen)
                tab.process_tab(tab.screen)
                tab.draw(tab.screen)
                top.draw()
                popup_rect = popup.get_rect(center=grid.surf.get_rect().center)

            elif event.type == KEYUP: # if a key was pressed
                if get_key:  # if we just want a key return the key
                    return event.key

                if 'a' <= event.unicode <= 'z' or 'A' <= event.unicode <= 'Z' or '0' <= event.unicode <= '9': # from a to z or 0 to 9
                    answer += event.unicode  # append the response and draw it
                    answer_surface = create_text_surface(answer)
                    pygame.draw.rect(popup, (240, 240, 240), (10, 70, size[0] -20, 20))
                    popup.blit(answer_surface, (15, 70))

                elif event.unicode == '\x08': #delete
                    if len(answer) > 0:
                        answer = answer[:-1]
                        answer_surface = create_text_surface(answer)
                        pygame.draw.rect(popup, (240, 240, 240), (10, 70, size[0] -20, 20))
                        popup.blit(answer_surface, (15, 70))

                elif event.unicode == '\r': #enter validates
                    if len(answer) > 0:
                        return answer

        grid.screen.blit(popup, (popup_rect.topleft))
        pygame.display.flip()

    #leave the popup after this line/loop

def draw_popup(popup, size, title, message, get_key=0):
    """draws a popup"""
    from utils.functions import create_text_surface
    radius = 5
    rect = pygame.draw.rect
    black = (0, 0, 0)
    white = (255, 255, 255)

    rect(popup, (240, 240, 240), (0, 0, size[0], 20),border_top_left_radius= radius, border_top_right_radius=radius)# top border
    rect(popup, black, (0, 0, size[0], 20), 1, border_top_left_radius= radius, border_top_right_radius=radius)# top border's border

    rect(popup, (220, 220, 220), (0, 19, size[0], size[1]-19), 5, border_bottom_left_radius=radius, border_bottom_right_radius=radius)# all around border

    rect(popup, (220, 0, 0), (size[0] -28, 0, 20, 15)) #red box
    rect(popup, (150, 150, 150), (size[0] -28, -1, 20, 16), 1) #red box border

    rect(popup, (190, 190, 190), (5, 20, size[0]-10, size[1]-25))# white background
    rect(popup, (150, 150, 150), (5, 20, size[0]-10, size[1]-25), 1)# grey inner border
    rect(popup, black, (0, 0, size[0], size[1]), 1, radius)# all around border's border

    # draws the white cross in the red box
    pygame.draw.line(popup, white, (size[0]-23, 3), (size[0]-15, 11), 2)
    pygame.draw.line(popup, white, (size[0]-15, 3), (size[0]-23, 11), 2)

    title_surface = create_text_surface(title)  # draws title
    popup.blit(title_surface, (popup.get_width()//2-title_surface.get_width()//2, 0))

    question = create_text_surface(message, 20)
    popup.blit(question, (10, 40))  # draws question

    if get_key == 0:  # draws the answer box only if needed
        pygame.draw.rect(popup, (240, 240, 240), (10, 69, size[0] -20, 25))
