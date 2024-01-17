import pygame

class button_class():
    def __init__(self, label):
        """Initialize class button with name"""

        self.label = label
        self.color = (150, 150, 150)
        self.state = 0
        self.text_surface = create_text_surface(label)
        self.sub_buttons = []

    def hover(self, x, y):
        """Check if the given coordinates are within the menu area for hover effect"""

        if self.state != 1:
            self.color = (150, 150, 150)
        else:
            if self.sub_buttons is not None:
                for button in self.sub_buttons:
                    button.hover(x, y)

        if x < self.rect_value[0] or x > self.rect_value[0] + self.rect_value[2]:
            return False
        if y < self.rect_value[1] or y > self.rect_value[1] + self.rect_value[3]:
            return False
        if self.state != 1:
            self.color = (160, 160, 160)
        return True

    def set_position(self, x, y, width, height):
        """set the position and size of the button and text"""

        self.rect_value = (x, y, width, height)
        text_x = x + int(width/2) - int(self.text_surface.get_width()/2)
        text_y = int((height - self.text_surface.get_height())/2)

        self.position_text = (text_x, text_y)

    def draw(self, screen):
        """Draw the menu on the screen"""

        pygame.draw.rect(screen, self.color, self.rect_value)
        screen.blit(self.text_surface, self.position_text)
        if self.state == 1:
            for button in self.sub_buttons:
                button.draw(screen)

    def click(self, x, y):
        """ Toggle the menu state and update color accordingly"""

        hover = self.hover(x, y)
        if hover:
            if self.state == 0:
                self.state = 1
                self.color = (120, 120, 120)
            else:
                self.state = 0
                self.color = (150, 150, 150)
            print (self.label, "clicked")
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


def create_text_surface(text):
    """Render text for the menu using a default font"""
    font = pygame.font.Font(None, 22)
    return font.render(text, True, (0, 0, 0))

