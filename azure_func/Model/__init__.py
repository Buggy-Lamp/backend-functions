from dataclasses import dataclass


@dataclass
class Project:
    name: str
    tools: list
    color: str = 'gray'
    color_weight: int = -1

    def process_project_color(self):
        self.color = 'gray'
        self.color_weight = -1

        for tool in self.tools:
            tool.process_tool_color()

            if tool.color is None or tool.color_weight is None:
                continue

            if tool.color_weight > self.color_weight:
                self.color = tool.color
                self.color_weight = tool.color_weight

    def serialize(self) -> dict:
        return {
            'id': self.name,
            'project': self.name,
            'color': self.color,
            'color_weight': self.color_weight,
            'tools': dict((tool.name, tool.serialize()) for tool in self.tools)
        }


@dataclass
class Tool:
    name: str
    instances: list
    color: str = 'gray'
    color_weight: int = -1

    def process_tool_color(self):
        self.color = 'gray'
        self.color_weight = -1

        for instance in self.instances:
            instance.process_instance_color()

            if instance.color is None or instance.color_weight is None:
                continue

            if instance.color_weight > self.color_weight:
                self.color = instance.color
                self.color_weight = instance.color_weight

    def serialize(self) -> dict:
        dct = {
            'name': self.name,
            'color': self.color,
            'color_weight': self.color_weight,
        }

        for instance in self.instances:
            dct[instance.name] = instance.serialize()

        return dct


@dataclass
class Instance:
    name: str
    properties: list
    color: str = 'gray'
    color_weight: int = -1

    def process_instance_color(self):
        self.color = 'gray'
        self.color_weight = -1

        for prop in self.properties:
            if prop.color is None or prop.color_weight is None:
                continue

            if prop.color_weight > self.color_weight:
                self.color = prop.color
                self.color_weight = prop.color_weight

    def append_prop(self, prop):
        if self.properties is None:
            self.properties = []

        self.properties.append(prop)

    def serialize(self) -> dict:
        return {
            'name': self.name,
            'color': self.color,
            'color_weight': self.color_weight,
            'properties': dict((prop.name, prop.serialize()) for prop in self.properties)
        }


@dataclass
class Property:
    name: str
    color: str = 'gray'
    color_weight: int = -1
    min_threshold: int = None
    found_value: int = None
    error: str = None

    def serialize(self) -> dict:
        dct = DictNoNone()
        dct['name'] = self.name
        dct['color'] = self.color
        dct['color_weight'] = self.color_weight
        dct['min_threshold'] = self.min_threshold
        dct['found_value'] = self.found_value
        dct['error'] = self.error
        return dct


class DictNoNone(dict):
    def __setitem__(self, key, value):
        if key in self or value is not None:
            dict.__setitem__(self, key, value)
