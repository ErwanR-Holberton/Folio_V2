#!/usr/bin/env python3
import json
from pygame.locals import *

def save_entities(entities):
    with open("./saves/autosave_entities.json", "w") as file:
        json.dump(entities, file)


entities = []
player = {"icon": "./saves/tiles/rabbit.png", "position": [5, 5], "keys": [K_UP, K_RIGHT, K_DOWN, K_LEFT]}
entities.append(player)
save_entities(entities)
