import pygame

class drop_down_menu:
    """Class variables to maintain shared properties across instances"""

    buttons_number = 0
    menu_width = 100
    menu_height = 30
    state = 0

    def __init__(self, name, submenus):
        """Initialize drop-down menu instance with a name, color, position and submenus"""
        self.position = (self.buttons_number * self.menu_width, 0)
        self.name = name
        self.color = (150, 150, 150)

        """Create submenu instances based on the provided submenus"""
        self.submenus = []
        from models.submenus import submenus_class
        for element in submenus:
            self.submenus.append(submenus_class(element))

        """Define the rectangle that represents the menu for collision detection"""
        self.rect_value = (self.position[0], self.position[1], self.menu_width, self.menu_height)

        """Render text for the menu using a default font"""
        font = pygame.font.Font(None, 22)                           
        self.text = font.render(name, True, (0, 0, 0))
        self.position_text = (self.position[0] + int(self.menu_width/2) - int(self.text.get_width()/2), int((self.menu_height - self.text.get_height())/2))

        """Increment the buttons_number for the next instance"""
        self.__class__.buttons_number += 1

    def test_click(self, x, y):
        """Check if the given coordinates are within the menu area and handle click event"""

        if x < self.position[0] or x > self.position[0] + self.menu_width:
            return False
        if y < self.position[1] or y > self.position[1] + self.menu_height:
            return False

        """ Toggle the menu state and update color accordingly"""
        if self.state == 0:
            self.state = 1
            self.color = (120, 120, 120)
        else:
            self.state = 0
            self.color = (150, 150, 150)
        return True

    def test_hover(self, x, y):
        """Check if the given coordinates are within the menu area for hover effect"""

        if x < self.position[0] or x > self.position[0] + self.menu_width:
            return False
        if y < self.position[1] or y > self.position[1] + self.menu_height:
            return False
        return True

    def draw(self, screen):
        """Draw the menu on the screen"""

        pygame.draw.rect(screen, self.color, self.rect_value)
        screen.blit(self.text, self.position_text)

    def draw_submenus(self, screen):
        """Draw submenus below the main menu"""
        
        i = 1
        for menu in self.submenus:
            pygame.draw.rect(screen, menu.color, (self.position[0], self.position[1] + self.menu_height * i, self.menu_width, self.menu_height))
            screen.blit(menu.text, (self.position[0] + int(self.menu_width/2) - int(menu.text.get_width()/2), int((self.menu_height - menu.text.get_height())/2) + self.menu_height * i))
            i += 1
