import pygame
import os

tileset = pygame.image.load("tileset.png") #Load the tileset image

def get_tile(x, y, set = tileset):
    """Extract a specific tile from the tileset and scale it to the desired size."""

    """Extract the specified tile from the tileset"""
    tile = set.subsurface((y * 16, x * 16, 16, 16)).copy()

    """Scale the tile to the desired size (32x32)"""
    return pygame.transform.scale(tile, (32, 32))

def load_tiles(path = "./base_assets/tiles/"):
    """Load individual tiles from the desired directory and return a list of scaled tiles."""

    """Get a list of file names in the desired directory"""
    tile_list = [f for f in os.listdir(path) if os.path.isfile(path + '/' + f)]

    tile_list.sort()

    """Initialize an empty list to store loaded and scaled tiles"""
    tiles = []

    """Load each image from the desired directory"""
    for file in tile_list:
        loaded_image = pygame.image.load(path + file)

        """Use the get_tile function to scale the loaded tile and append it to the list"""
        if path == "./base_assets/tiles/":
            center = get_tile(1, 1, loaded_image)
            tiles.append(center)
        else:
            tiles.append(loaded_image)

    return tiles

def create_text_surface(text, size = 20):
    """Render text for the menu using calibri font"""
    font = pygame.font.Font("./base_assets/CALIBRI.TTF", size)
    return font.render(text, True, (0, 0, 0))


def draw_screen(screen, tab, grid, top):
    screen.fill((255, 255, 255))  #Fill the screen with a white background

    # Draw the menus tab and grid
    tab.draw(screen)
    grid.draw(screen)

    # Draw menus and submenus
    top.draw()

    # Draw a square with the selected tile
    pygame.draw.rect(screen, (100, 100, 100), (grid.width - 32, 0, 32, 32))
    pygame.draw.rect(screen, (0, 0, 0), (grid.width - 32, 0, 32, 32), 1)
    if grid.selected_tile is not None:
        screen.blit(grid.selected_tile, (grid.width - 32, 0))

    pygame.display.flip() # Refresh the display


def count_lines(array,items_by_lines=8):
    lines = len(array) // items_by_lines    # count lines of tiles
    if len(array) % items_by_lines != 0:
        lines += 1
    return lines
