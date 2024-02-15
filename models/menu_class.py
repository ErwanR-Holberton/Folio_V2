import pygame

from models.button_class import button_class

class menu_class():
    def __init__(self, name, screen):
        """Initialize class menu"""
        self.width = 0
        self.height = 30
        self.buttons = []
        self.screen = screen

    def create_top_menu(self):
        "create a list of drop_down menus"

        self.button_width = 100
        self.expand("Project", ["New", "Load", "Save", "Delete"])
        self.expand("Map", ["New", "Load", "Save", "Delete"])
        self.expand("Tile", ["New", "Load", "Save", "Delete"])
        self.expand("Edit", ["Undo", "Redo"])
        self.expand("Help", [])
        self.buttons[2].sub_buttons[1].function = self.buttons[2].sub_buttons[1].load_tile
        self.buttons[2].sub_buttons[2].function = self.buttons[2].sub_buttons[2].save_tile
        self.buttons[2].sub_buttons[0].function = self.buttons[2].sub_buttons[0].new_tile

    def create_tab_menu(self):
        "create a menu for the tab section"

        self.button_width = 107
        self.expand("Tiles")
        self.expand("Tools")
        self.expand("Settings")

    def expand(self, button_name, sub_buttons = None):
        """add a button to the object menu"""

        new_button = button_class(button_name)
        new_button.set_position(self.width, 0, self.button_width, self.height)
        new_button.create_sub_buttons(sub_buttons)
        self.buttons.append(new_button)
        self.width += self.button_width

    def hover(self, x, y):
        """"""
        button_hovered = False
        for button in self.buttons:
            if button.hover(x, y):
                button_hovered = True
            if button.hover_subbuttons(x, y):
                button_hovered = True
        return button_hovered

    def click(self, x, y):
        """"""
        clicked = 0
        for button in self.buttons:
            button.color = (150, 150, 150)
            if button.click(x, y) is False:
                button.state = 0
            else:
                clicked = 1
        return clicked

    def draw(self):
        for button in self.buttons:
            button.draw(self.screen)
