import pygame

tileset = pygame.image.load("tileset.png")

def get_tile(x, y):
    tile = tileset.subsurface((y * 16, x * 16, 16, 16)).copy()
    return pygame.transform.scale(tile, (32, 32))