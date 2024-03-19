from models.button_class import button_class

class menu_class():
    def __init__(self, name, screen):
        """Initialize class menu"""
        self.width = 0
        self.height = 30
        self.line_height = 30
        self.buttons = []
        self.screen = screen
        self.current_width = 0

    def create_top_menu(self):
        "create a list of drop_down menus"

        self.button_width = 100
        self.expand("Project", ["New", "Load", "Delete"])
        self.expand("Map", ["New", "Load", "Save", "Delete"])
        self.expand("Tile", ["New", "Load", "Save", "Delete"])
        self.expand("Blueprint", ["New", "Load", "Save", "Delete"])
        self.expand("Edit", ["Undo", "Redo"])
        self.expand("Play", [])
        self.expand("Help", [])
        self.buttons[0].sub_buttons[0].function = self.buttons[0].sub_buttons[0].new_project
        self.buttons[0].sub_buttons[1].function = self.buttons[0].sub_buttons[1].load_project
        self.buttons[0].sub_buttons[2].function = self.buttons[0].sub_buttons[2].delete_project
        self.buttons[1].sub_buttons[0].function = self.buttons[1].sub_buttons[0].new_map
        self.buttons[1].sub_buttons[1].function = self.buttons[1].sub_buttons[1].load_map
        self.buttons[1].sub_buttons[2].function = self.buttons[1].sub_buttons[2].save_map
        self.buttons[1].sub_buttons[3].function = self.buttons[1].sub_buttons[3].delete_map
        self.buttons[2].sub_buttons[0].function = self.buttons[2].sub_buttons[0].new_tile
        self.buttons[2].sub_buttons[1].function = self.buttons[2].sub_buttons[1].load_tile
        self.buttons[2].sub_buttons[2].function = self.buttons[2].sub_buttons[2].save_tile
        self.buttons[2].sub_buttons[3].function = self.buttons[2].sub_buttons[3].delete_tile
        self.buttons[3].sub_buttons[0].function = self.buttons[3].sub_buttons[0].new_blueprint
        self.buttons[3].sub_buttons[1].function = self.buttons[3].sub_buttons[1].load_blueprint
        self.buttons[3].sub_buttons[2].function = self.buttons[3].sub_buttons[2].save_blueprint
        self.buttons[3].sub_buttons[3].function = self.buttons[3].sub_buttons[3].delete_blueprint
        self.buttons[4].sub_buttons[0].function = self.buttons[4].sub_buttons[0].undo
        self.buttons[4].sub_buttons[1].function = self.buttons[4].sub_buttons[1].redo
        self.buttons[5].function = self.buttons[5].play
        self.buttons[6].function = self.buttons[6].help

    def create_tab_menu(self):
        "create a menu for the tab section"

        self.button_width = 107
        self.width = 320
        self.expand("Map mode")
        self.expand("Tile mode")
        self.expand("Settings")
        self.current_width = 0
        self.height = 60
        self.expand("Project", newline=1)
        self.expand("Entities", newline=1)
        self.expand("Events", newline=1)

    def expand(self, button_name, sub_buttons = None, newline = 0):
        """add a button to the object menu"""

        new_button = button_class(button_name)
        new_button.set_position(self.current_width, newline * self.line_height, self.button_width, self.line_height)
        new_button.create_sub_buttons(sub_buttons)
        new_button.function = new_button.change_tab
        self.buttons.append(new_button)
        self.current_width += self.button_width
        if self.current_width > self.width:
            self.width = self.current_width

    def hover(self, x, y):
        """test if the mouse is on the button"""
        button_hovered = False
        for button in self.buttons:
            if button.hover(x, y):
                button_hovered = True
            if button.hover_subbuttons(x, y):
                button_hovered = True
        return button_hovered

    def click(self, x, y):
        """test if the user clicked on the button"""
        clicked = 0
        for button in self.buttons:
            button.color = (150, 150, 150)
            if button.click(x, y) is False:
                button.state = 0
            else:
                clicked = 1
        return clicked

    def draw(self):
        """draw the buttons"""
        for button in self.buttons:
            button.draw(self.screen)
