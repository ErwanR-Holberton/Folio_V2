from utils.functions import load_json
from models.tile_class import tile_class

class map_class():
    "create a class for the maps"
    list_of_maps = []
    current_map = 0
    def __init__(self, path):
        map_dictionnary = load_json(path)
        self.events = map_dictionnary["events"]
        self.entities = map_dictionnary["entities"]
        self.offset = map_dictionnary["offset"]
        tiles_coordinates = map_dictionnary["tiles"]
        unique_tiles = set(tiles_coordinates.values())  # prepare to load tiles only once
        pairs = {name: tile_class(name) for name in unique_tiles}
        self.tiles = {}
        for key, value in tiles_coordinates.items():
            self.tiles[key] = pairs[value]
        __class__.list_of_maps.append(self)
