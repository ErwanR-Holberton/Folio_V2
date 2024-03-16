import pygame
import os
import json

tileset = pygame.image.load("tileset.png") #Load the tileset image

def get_tile(x, y, set = tileset):
    """Extract a specific tile from the tileset and scale it to the desired size."""

    """Extract the specified tile from the tileset"""
    tile = set.subsurface((y * 16, x * 16, 16, 16)).copy()

    """Scale the tile to the desired size (32x32)"""
    return pygame.transform.scale(tile, (32, 32))

def load_tiles(path = "./base_assets/tiles/"):
    """Load individual tiles from the desired directory and return a list of scaled tiles."""
    tile_list = list_png(path)  # lists the png files
    tile_list.sort()

    tiles = []  # Initialize an empty list to store loaded and scaled tiles
    for file in tile_list:  # Load each image from the desired directory
        loaded_image = pygame.image.load(path + file)

        if path == "./base_assets/tiles/":
            scaled_image = pygame.transform.scale(loaded_image, (32, 32))
            tiles.append([scaled_image, "b" + file[:-4]])
        elif path == "./saves/tiles/":
            tiles.append([loaded_image, "u" + file[:-4]])
        else:
            tiles.append([loaded_image])

    return tiles

def create_text_surface(text, size = 20, color=(0,0,0), font="CALIBRI.TTF"):
    """Render text for the menu using calibri font"""
    font = pygame.font.Font("./base_assets/" + font, size)
    return font.render(text, True, color)

def draw_screen(screen, tab, grid, top):
    """fills the screen and redraw it"""

    screen.fill((255, 255, 255))  #Fill the screen with a white background

    grid.draw(screen)
    top.draw()  # Draw menus and submenus

    # Draw a square with the selected tile
    pygame.draw.rect(screen, (100, 100, 100), (grid.width - 32, 0, 32, 32))  # background
    pygame.draw.rect(screen, (0, 0, 0), (grid.width - 32, 0, 32, 32), 1)  # border
    if grid.selected_tile is not None:
        scaled = pygame.transform.scale(grid.selected_tile[0], (32, 32))  # scale selected tile
        screen.blit(scaled, (grid.width - 32, 0))  # draw it

        if grid.selected_tile[0].get_width() > 32 and grid.mode == 0:  # draw the selected blueprint where it will be
            index_x, index_y = grid.calculate_coordinates(*pygame.mouse.get_pos())
            pos_x = index_x * 32 + grid.offset[0]
            pos_y = index_y * 32 + grid.offset[1]
            screen.blit(grid.selected_tile[0], (pos_x , pos_y))
    tab.draw(screen)  # Draw the menus tab and grid

    pygame.display.flip() # Refresh the display


def count_lines(array,items_by_lines=8):
    """counts number of lines of tiles in an given array"""
    lines = len(array) // items_by_lines    # count lines of tiles
    if len(array) % items_by_lines != 0:
        lines += 1  # if there is a rest add a line
    return lines

def load_json(path):
    """loads a json file"""
    with open(path, "r") as file:
        object = json.load(file)
    return object

def list_png(path):
    """list all pngs in the folder"""
    png_list = [f for f in os.listdir(path) if os.path.isfile(path + '/' + f)]

    return [f for f in png_list if not f.endswith(".json")]  #filter json files from the list
