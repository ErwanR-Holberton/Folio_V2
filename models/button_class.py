import pygame
import json
from pygame.locals import *

class button_class():
    def __init__(self, label):
        """Initialize class button with name"""

        self.label = label
        self.color = (150, 150, 150)
        self.state = 0
        self.text_surface = self.create_text_surface(label)
        self.sub_buttons = []
        self.radius_bottom_right = -1
        self.name = label
        self.function = None
        self.function = self.function_1

    def hover(self, x, y):
        """Check if the given coordinates are within the menu area for hover effect"""

        if x < self.rect_value[0] or x > self.rect_value[0] + self.rect_value[2]:
            return False
        if y < self.rect_value[1] or y > self.rect_value[1] + self.rect_value[3]:
            return False
        if self.state != 1:
            self.color = (160, 160, 160)
        return True

    def hover_subbuttons(self, x, y):

        button_hovered = 0
        if self.state != 1:
            self.color = (150, 150, 150)
        else:
            if self.sub_buttons is not None:
                for button in self.sub_buttons:
                    if button.hover(x, y):
                        button_hovered = 1
        if button_hovered:
            return True

    def set_position(self, x, y, width, height):
        """set the position and size of the button and text"""

        self.rect_value = (x, y, width, height)
        text_x = x + int(width/2) - int(self.text_surface.get_width()/2)
        text_y = y + int((height - self.text_surface.get_height())/2)

        self.position_text = (text_x, text_y)

    def draw(self, screen):
        """Draw the menu on the screen"""

        pygame.draw.rect(screen, self.color, self.rect_value, border_bottom_right_radius= self.radius_bottom_right)
        screen.blit(self.text_surface, self.position_text)
        if self.state == 1:
            for button in self.sub_buttons:
                button.draw(screen)

    def click(self, x, y):
        """ Toggle the menu state and update color accordingly"""

        clicked_sub_button = 0
        if self.state == 1 and self.sub_buttons is not None:
            for button in self.sub_buttons:
                if button.click(x, y):
                    clicked_sub_button = 1
                button.state = 0
        hover = self.hover(x, y)
        if hover:
            if self.state == 0:
                self.state = 1
                self.color = (120, 120, 120)
                if self.name == "R" or self.name == "G" or self.name == "B":
                    if self.label.isalpha():
                        self.label = ""
                        self.text_surface = self.create_text_surface("")
            else:
                self.state = 0
                self.color = (150, 150, 150)
            if self.function is not None:
                self.function()
        if clicked_sub_button:
            return True
        return hover

    def create_sub_buttons(self, sub_buttons):
        if sub_buttons is None:
            return
        count = 0
        x, y, w, h = self.rect_value
        for button_name in sub_buttons:
            count += 1
            new = button_class(button_name)
            new.set_position(x, (y + count * h), w, h)
            self.sub_buttons.append(new)

    def create_text_surface(self, text, size = 22):
        """Render text for the menu using a default font"""
        font = pygame.font.Font("./base_assets/CALIBRI.TTF", size)
        return font.render(text, True, (0, 0, 0))

    def edit_label(self, key):
        if key == -1:
            if len(self.label) > 0:
                self.label = self.label[:-1]
        else:
            if len(self.label) > 0:
                if int(self.label) == 0:
                    self.label = ""
            self.label += str(key)
            if int(self.label) > 255:
                self.label = "255"
        self.text_surface = self.create_text_surface(self.label)
        x, y, width, height = self.rect_value
        self.set_position(x, y, width, height)

    def function_1(self):
        print(self.label, "clicked")

    def save_tile(self):
        new_tile = pygame.Surface((len(self.grid.tile_grid), len(self.grid.tile_grid)), pygame.SRCALPHA)
        new_tile.fill((0, 0, 0, 25))
        for line in range (len(self.grid.tile_grid)):
            for column in range (len(self.grid.tile_grid[line])):
                new_tile.set_at((column, line), self.grid.tile_grid[column][line])
        name = self.popup("Please choose a name for the tile:", "Tile save")
        if name is not None:
            pygame.image.save(new_tile, "saves/tiles/" + name + ".png")
        self.grid.tab.reload_user_tiles()

    def load_tile(self):
        image = pygame.image.load("test.png")
        tile = self.grid.tile_grid = []
        for line in range (image.get_height()):
            new_line = []
            for column in range (image.get_width()):
                new_line.append(image.get_at((line, column)))
            tile.append(new_line)
        self.grid.calculate(self.grid.screen)

    def save_tile_json(self):
        with open ("dump.json", "w") as file:
            json.dump(self.grid.tile_grid, file)

    def load_tile_json(self):
        with open ("dump.json", "r") as file:
            self.grid.tile_grid = json.load(file)

    def new_tile(self):
        self.grid.tile_grid = [[(0, 0, 0, 0) for x in range(16)] for y in range(16)]
        self.grid.calculate(self.grid.screen)

    def popup(self, message, title):

        size = (400, 110)
        radius = 5
        loop = 1
        popup = pygame.Surface(size, pygame.SRCALPHA)
        popup_rect = popup.get_rect(center=self.grid.surf.get_rect().center)
        popup.fill((10, 8, 50, 0))
        self.draw_popup(popup, size, radius, title, message)
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
                    self.grid.calculate(self.grid.screen)
                    self.grid.draw(self.grid.screen)
                    self.tab.calculate(self.tab.screen)
                    self.tab.draw(self.tab.screen)
                    self.top.draw()
                    popup_rect = popup.get_rect(center=self.grid.surf.get_rect().center)
                if event.type == KEYUP:
                    if 'a' <= event.unicode <= 'z' or 'A' <= event.unicode <= 'Z':
                        answer += event.unicode
                        answer_surface = self.create_text_surface(answer)
                        pygame.draw.rect(popup, (240, 240, 240), (10, 70, size[0] -20, 20))
                        popup.blit(answer_surface, (15, 70))
                    elif event.unicode == '\x08':
                        if len(answer) > 0:
                            answer = answer[:-1]
                            answer_surface = self.create_text_surface(answer)
                            pygame.draw.rect(popup, (240, 240, 240), (10, 70, size[0] -20, 20))
                            popup.blit(answer_surface, (15, 70))
                    elif event.unicode == '\r':
                        if len(answer) > 0:
                            return answer
            self.grid.screen.blit(popup, (popup_rect.topleft))
            pygame.display.flip()

    def draw_popup(self, popup, size, radius, title, message):
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

        title_surface = self.create_text_surface(title)
        popup.blit(title_surface, (popup.get_width()//2-title_surface.get_width()//2, 0))

        question = self.create_text_surface(message, 20)
        popup.blit(question, (10, 40))

        pygame.draw.rect(popup, (240, 240, 240), (10, 69, size[0] -20, 25))

    def save_map(self):

        name = self.popup("Please choose a name for the map:", "Map save")
        if name is not None:
            pygame.image.save(self.grid.tile_surf, "saves/maps/" + name + ".png")

    def load_map(self):

        name = self.popup("Please enter the name of the desired map:", "Map load")
        if name is not None:
            self.grid.tile_surf = pygame.image.load("saves/maps/" + name + ".png")
            self.grid.calculate(self.grid.screen)
        print("function load")
