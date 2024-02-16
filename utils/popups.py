import pygame
from pygame.locals import *

def popup(message, title, grid, tab, top):
    """create a popup loop"""
    from utils.functions import create_text_surface
    size = (400, 110)
    radius = 5
    loop = 1
    popup = pygame.Surface(size, pygame.SRCALPHA)
    popup_rect = popup.get_rect(center=grid.surf.get_rect().center)
    popup.fill((10, 8, 50, 0))
    draw_popup(popup, size, radius, title, message)
    answer = ""
    while loop:
        for event in pygame.event.get():
            if event.type == QUIT: # Check for quit event (click on red cross or press Esc key)
                loop = 0
            if event.type == MOUSEBUTTONUP: # Check for mouse button click event
                mouse_x, mouse_y = event.pos
                mouse_x -= popup_rect.topleft[0]
                mouse_y -= popup_rect.topleft[1]
                if mouse_x >= size[0] - 28 and mouse_x <= size[0] -8:
                    if mouse_y >= 0 and mouse_y <= 15:
                        loop = 0
            if event.type == WINDOWRESIZED:
                grid.process_surface(grid.screen)
                grid.draw(grid.screen)
                tab.process_tab(tab.screen)
                tab.draw(tab.screen)
                top.draw()
                popup_rect = popup.get_rect(center=grid.surf.get_rect().center)
            if event.type == KEYUP:
                if 'a' <= event.unicode <= 'z' or 'A' <= event.unicode <= 'Z':
                    answer += event.unicode
                    answer_surface = create_text_surface(answer)
                    pygame.draw.rect(popup, (240, 240, 240), (10, 70, size[0] -20, 20))
                    popup.blit(answer_surface, (15, 70))
                elif event.unicode == '\x08':
                    if len(answer) > 0:
                        answer = answer[:-1]
                        answer_surface = create_text_surface(answer)
                        pygame.draw.rect(popup, (240, 240, 240), (10, 70, size[0] -20, 20))
                        popup.blit(answer_surface, (15, 70))
                elif event.unicode == '\r':
                    if len(answer) > 0:
                        return answer
        grid.screen.blit(popup, (popup_rect.topleft))
        pygame.display.flip()

def draw_popup(popup, size, radius, title, message):
    """draws a popup"""
    from utils.functions import create_text_surface
    pygame.draw.rect(popup, (240, 240, 240), (0, 0, size[0], 20),border_top_left_radius= radius, border_top_right_radius=radius)# top border
    pygame.draw.rect(popup, (0, 0, 0), (0, 0, size[0], 20), 1, border_top_left_radius= radius, border_top_right_radius=radius)# top border's border

    pygame.draw.rect(popup, (220, 220, 220), (0, 19, size[0], size[1]-19), 5, border_bottom_left_radius=radius, border_bottom_right_radius=radius)# all around border

    pygame.draw.rect(popup, (220, 0, 0), (size[0] -28, 0, 20, 15)) #red box
    pygame.draw.rect(popup, (150, 150, 150), (size[0] -28, -1, 20, 16), 1) #red box border

    pygame.draw.rect(popup, (190, 190, 190), (5, 20, size[0]-10, size[1]-25))# white background
    pygame.draw.rect(popup, (150, 150, 150), (5, 20, size[0]-10, size[1]-25), 1)# white background border
    pygame.draw.rect(popup, (0, 0, 0), (0, 0, size[0], size[1]), 1, radius)# all around border's border

    pygame.draw.line(popup, (255, 255, 255), (size[0]-23, 3), (size[0]-15, 11), 2) # white cross in red box
    pygame.draw.line(popup, (255, 255, 255), (size[0]-15, 3), (size[0]-23, 11), 2) # white cross in red box

    title_surface = create_text_surface(title)
    popup.blit(title_surface, (popup.get_width()//2-title_surface.get_width()//2, 0))

    question = create_text_surface(message, 20)
    popup.blit(question, (10, 40))

    pygame.draw.rect(popup, (240, 240, 240), (10, 69, size[0] -20, 25))
