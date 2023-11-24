import pygame

class drop_down_menu:

    buttons_number = 0
    menu_width = 100
    menu_height = 30
    state = 0

    def __init__(self, name, submenus):
        
        self.position = (self.buttons_number*self.menu_width, 0)
        self.name = name
        self.submenus = []
        from submenus import submenus_class
        for element in submenus:
            self.submenus.append(submenus_class(element))
        self.__class__.buttons_number += 1
        self.rect_value = (self.position[0], self.position[1], self.menu_width, self.menu_height)
        font = pygame.font.Font(None, 22)                           #create default font size 20
        self.text = font.render(name, True, (0, 0, 0))
        self.position_text = (self.position[0] + int(self.menu_width/2) - int(self.text.get_width()/2), int((self.menu_height - self.text.get_height())/2))
        self.color = (150, 150, 150)

    def test_click(self, x, y):
    
        if x < self.position[0] or x > self.position[0] + self.menu_width:
            return False
        if y < self.position[1] or y > self.position[1] + self.menu_height:
            return False

        if self.state == 0:
            self.state = 1
            self.color = (120, 120, 120)
        else:
            self.state = 0
            self.color = (150, 150, 150)
        return True
    
    def test_hover(self, x, y):
    
        if x < self.position[0] or x > self.position[0] + self.menu_width:
            return False
        if y < self.position[1] or y > self.position[1] + self.menu_height:
            return False
        return True
    
    def draw(self, screen):

        pygame.draw.rect(screen, self.color, self.rect_value)
        screen.blit(self.text, self.position_text)

    def draw_submenus(self, screen):
        i = 1
        for menu in self.submenus:
            pygame.draw.rect(screen, menu.color, (self.position[0], self.position[1] + self.menu_height * i, self.menu_width, self.menu_height))
            screen.blit(menu.text, (self.position[0] + int(self.menu_width/2) - int(menu.text.get_width()/2), int((self.menu_height - menu.text.get_height())/2) + self.menu_height * i))
            i += 1