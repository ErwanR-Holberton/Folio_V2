import pygame
import os

tileset = pygame.image.load("tileset.png") #Load the tileset image

def get_tile(x, y, set = tileset):
    """Extract a specific tile from the tileset and scale it to the desired size."""

    """Extract the specified tile from the tileset"""
    tile = set.subsurface((y * 16, x * 16, 16, 16)).copy()

    """Scale the tile to the desired size (32x32)"""
    return pygame.transform.scale(tile, (32, 32))

def load_tiles():
    """Load individual tiles from the "./tiles" directory and return a list of scaled tiles."""

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
