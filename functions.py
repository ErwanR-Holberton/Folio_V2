import pygame
import os

"""Load the tileset image"""
tileset = pygame.image.load("tileset.png")

def get_tile(x, y, set = tileset):
    """
    Extract a specific tile from the tileset and scale it to the desired size.

    Parameters:
    - x: Row index of the tile in the tileset.
    - y: Column index of the tile in the tileset.
    - set: The tileset image (default is the global tileset).

    Returns:
    - A scaled version of the specified tile.
    """

    """Extract the specified tile from the tileset"""
    tile = set.subsurface((y * 16, x * 16, 16, 16)).copy()

    """Scale the tile to the desired size (32x32)"""
    return pygame.transform.scale(tile, (32, 32))

def load_tiles():
    """
    Load individual tiles from the "./tiles" directory and return a list of scaled tiles.

    Returns:
    - A list of scaled tiles loaded from individual images in the "./tiles" directory.
    """

    """Get a list of file names in the "./tiles" directory"""
    images = [f for f in os.listdir("./tiles")]

    """Initialize an empty list to store loaded and scaled tiles"""
    tiles = []

    """Load each image from the "./tiles" directory"""
    for file in images:
        loaded_image = pygame.image.load("./tiles/" + file)

        """Use the get_tile function to scale the loaded tile and append it to the list"""
        tiles.append(get_tile(1, 1, loaded_image))

    return tiles
