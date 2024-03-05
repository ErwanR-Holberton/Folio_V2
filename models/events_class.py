import json

class event_class():

    all = []

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

    def trigger(self):
        selected_entities = self.entities
        if self.action == "move":
            for entity in selected_entities:
                entity.position = [self.dest[0] * 32, self.dest[1] * 32]

