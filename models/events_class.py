import json
import pygame
from utils.functions import create_text_surface

class event_class():

    all = []
    win = 0
    loose = 0

    def __init__(self, event_dict):

        for key, value in event_dict.items():
            setattr(self, key, value)
        __class__.all.append(self)

    @staticmethod
    def load_events():
        """loads all events from a json file"""
        with open ("./saves/autosave_events.json", "r") as file:
            events = json.load(file)
        for dict in events:
            __class__(dict)

    def trigger(self, obj):
        """trigger the effect of the event"""
        if self.target == "one":  # target the entity that triggered this event
            selected_entities = [obj]
        elif self.target == "all":  # target all entities
            selected_entities = self.entities
        else:  # target by a specific id
            selected_entities = []
            for entity in self.entities:
                if entity.id == self.target:
                    selected_entities = [entity]
        if self.action == "move":
            for entity in selected_entities:
                entity.position = [self.dest[0] * 32, self.dest[1] * 32]
        if self.action == "win":
            __class__.win = 1
        if self.action == "loose":
            __class__.loose = 1

