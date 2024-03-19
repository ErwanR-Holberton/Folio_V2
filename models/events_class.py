import json
import pygame
from utils.functions import create_text_surface

class event_class():
    """define event class"""

    all = []
    win = 0
    loose = 0

    def __init__(self, event_dict):

        for key, value in event_dict.items():
            if key == "optional_keys":
                for key2, value2 in event_dict["optional_keys"].items():
                    setattr(self, key2, value2)
            else:
                setattr(self, key, value)
        __class__.all.append(self)

    @staticmethod
    def load_events(events_list):
        """loads all events from the list of events in the map"""
        for dict in events_list:
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
            if not hasattr(self, "dest"):
                return
            for entity in selected_entities:
                entity.position = [self.dest[0] * 32, self.dest[1] * 32]
        elif self.action == "win":
            __class__.win = 1
        elif self.action == "loose":
            __class__.loose = 1
        elif self.action == "change_stat":
            for key in ["sign", "stat", "value"]:
                if not hasattr(self, key):
                    return
            for entity in selected_entities:
                if self.stat in entity.stats:
                    if self.sign == "-":
                        entity.stats[self.stat] -= self.value
                    elif self.sign == "+":
                        entity.stats[self.stat] += self.value
                    print(entity.stats)

