import HpEntity
import Vector
import Meta_Data
import Grid
import json
import random
import Sprites_
import pathlib


class State:
    Textures_folder = pathlib.Path('Textures')

    def __init__(self):
        self.player = HpEntity.HpEntity('', Vector.Vector(0, 0), 120, 100, 0, 0, 1, 1, Meta_Data.MetaData(is_player=True))
        self.window = None
        self.grid = Grid.Grid()
        self.cell_size = Vector.Vector(100, 100)
        self.render_radius = 2
        self.pw = ''
        self.texture_mapping = {}
        self.load_textures()
        self.is_new_tile = False
        self.is_moving = False
        self.moves_since_texture_save = 0
        # Meta_Data.isme = True

    def tile_type_pos(self, x, y):
        xy = f'{int(x)} {int(y)}'
        if xy not in self.texture_mapping:
            sprite_textures = random.choices(tuple(Sprites_.sprite_alias), k=1, weights=(45, 35, 1))
            # 25, 20, 15, 10, 5, 3,
            self.texture_mapping[xy] = random.choice(sprite_textures)
            self.is_new_tile = True
        return Sprites_.sprite_alias[self.texture_mapping[xy]]

    def ensure_textures_folder(self):
        if not self.Textures_folder.exists():
            self.Textures_folder.mkdir()

    def load_textures(self):
        import os
        self.ensure_textures_folder()
        if not os.path.exists(self.Textures_folder/f'{self.player.name}_texture_list.json'):
            self.save_textures()
        with open(self.Textures_folder/f'{self.player.name}_texture_list.json') as input_file:
            self.texture_mapping = json.load(input_file)

    def save_textures(self):
        self.ensure_textures_folder()
        with open(self.Textures_folder/f'{self.player.name}_texture_list.json', 'w') as output:
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
