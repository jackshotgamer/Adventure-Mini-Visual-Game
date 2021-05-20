import json
import pathlib
import random
from typing import List, Dict, Any, Union, Type

from W_Main_File.Data import HpEntity, Grid, Sprites_, Meta_Data
from W_Main_File.Utilities import Vector, Seeding


class State:
    Textures_folder = pathlib.Path('Interactable_Tiles')

    def __init__(self):
        self.player = HpEntity.HpEntity('', Vector.Vector(0, 0), 220, 200, 0, 0, 1, 1, Meta_Data.MetaData(is_player=True))
        self.window = None
        self.grid = Grid.Grid()
        self.cell_size = Vector.Vector(100, 100)
        self.render_radius = 2
        self.pw = ''
        self.texture_mapping = {}
        self.is_new_tile = False
        self.is_moving = False
        self.moves_since_texture_save = 0
        self.preoccupied = False
        # Meta_Data.is_me = True

    def tile_type_pos(self, x, y):
        poss = Vector.Vector(x, y)
        xy = f'{int(x)} {int(y)}'
        if xy not in self.texture_mapping:
            rnjesus = Seeding.seed_for_vector(poss)
            sprite_textures = rnjesus.choices(tuple(Sprites_.sprite_alias), k=1, weights=(45, 1.5, 35, 1.5, 15, 1))
            # 20, 15, 10, 5, 3,
            self.texture_mapping[xy] = rnjesus.choice(sprite_textures)
            self.is_new_tile = True
        return Sprites_.sprite_alias[self.texture_mapping[xy]]

    def get_tile_id(self, vector):
        self.tile_type_pos(vector.x, vector.y)
        return self.texture_mapping[f'{vector.x} {vector.y}']

    @property
    def screen_center(self):
        return Vector.Vector(self.window.width / 2, self.window.height / 2)

    @staticmethod
    def generate_radius(radius):
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                yield x, y

    def give_gold(self, amount):
        self.player.gold += round((((self.player.floor - 1) / 100) + 1) * amount)

    def clear_current_floor_data(self):
        self.texture_mapping.clear()
        self.grid.interactable_tiles.clear()


state = State()
