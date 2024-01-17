import pygame

from models.button_class import button_class

class menu_class():
    def __init__(self, name):
        """Initialize class menu"""
        self.width = 0
        self.height = 30
        self.buttons = []

    def create_top_menu(self):
        "create a list of drop_down menus"

        self.button_width = 100
        self.expand("Project", ["New", "Load", "Save"])
        self.expand("Map", ["New", "Load", "Save"])
        self.expand("Tile", ["New", "Edit", "Delete"])
        self.expand("Edit", ["Undo", "Redo"])
        self.expand("Help", [])

    def expand(self, button_name, sub_buttons = None):
        """add a button to the object menu"""

        new_button = button_class(button_name)
        new_button.set_position(self.width, 0, self.button_width, self.height)
        new_button.create_sub_buttons(sub_buttons)
        self.buttons.append(new_button)
        self.width += self.button_width

    def hover(self, x, y):
        """"""
        for button in self.buttons:
            button.hover(x, y)

    def click(self, x, y):
        """"""
        for button in self.buttons:
            button.color = (150, 150, 150)
            if button.click(x, y) is False:
                button.state = 0
