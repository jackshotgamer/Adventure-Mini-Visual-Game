import HpEntity
import Vector
import Meta_Data
import Grid
import json


class State:
    def __init__(self):
        self.player = HpEntity.HpEntity('', Vector.Vector(0, 0), 120, 100, 0, 0, 1, 1, Meta_Data.MetaData(is_player=True))
        self.window = None
        self.grid = Grid.Grid()
        self.cell_size = Vector.Vector(100, 100)
        self.render_radius = 2
        self.pw = ''
        self.texture_mapping = {}
        self.load_textures()

    def load_textures(self):
        import os
        if not os.path.exists('texture_list.json'):
            self.save_textures()
        with open('texture_list.json') as input_file:
            self.texture_mapping = json.load(input_file)

    def save_textures(self):
        with open('texture_list.json', 'w') as output:
            json.dump(self.texture_mapping, output)

    @property
    def screen_center(self):
        return Vector.Vector(self.window.width / 2, self.window.height / 2)

    @staticmethod
    def generate_radius(radius):
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                yield x, y

    @staticmethod
    def generate_edges(inner_radius):
        for x in range(~inner_radius, inner_radius + 2):
            for y in range(~inner_radius, inner_radius + 2):
                if abs(x) > inner_radius or abs(y) > inner_radius:
                    yield x, y


state = State()
