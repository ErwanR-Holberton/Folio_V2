import pygame
import os

tileset = pygame.image.load("tileset.png")

def get_tile(x, y, set = tileset):
    tile = set.subsurface((y * 16, x * 16, 16, 16)).copy()
    return pygame.transform.scale(tile, (32, 32))

def load_tiles():
    images = [f for f in os.listdir("./tiles")]
    tiles = []
    for file in images:
        loaded_image = pygame.image.load("./tiles/" + file)
        tiles.append(get_tile(1, 1, loaded_image))
    return tiles
