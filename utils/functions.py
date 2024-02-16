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
    tile_list = [f for f in os.listdir(path)]

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
