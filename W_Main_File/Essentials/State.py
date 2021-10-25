import json
import pathlib
import random
from typing import List, Dict, Any, Union, Type

import arcade

from W_Main_File.Data import HpEntity, Grid, Sprites_, Meta_Data
from W_Main_File.Items import Inventory
from W_Main_File.Utilities import Vector, Seeding


class State:
    Textures_folder = pathlib.Path('Interactable_Tiles')

    def __init__(self):
        self.player = HpEntity.HpEntity('', Vector.Vector(0, 0), 1000, 1000, 0, 0, 1, 1, Meta_Data.MetaData(is_player=True))
        self.window = None
        self.grid = Grid.Grid()
        self.cell_size = Vector.Vector(100, 100)
        self.render_radius = 2
        self.default_window_size = Vector.Vector(1000, 800)
        self.pw = ''
        self.texture_mapping = {}
        self.inventory = Inventory.InventoryContainer()
        self.current_page = 0
        self.is_new_tile = False
        self.is_moving = False
        self.moves_since_texture_save = 0
        self._preoccupied = False
        # Meta_Data.is_me = True

    @property
    def preoccupied(self):
        return self._preoccupied

    @preoccupied.setter
    def preoccupied(self, value):
        self._preoccupied = value

    def tile_type_pos(self, x, y):
        poss = Vector.Vector(x, y)
        xy = f'{int(x)} {int(y)}'
        if xy not in self.texture_mapping:
            rnjesus = Seeding.seed_for_vector(poss)
            sprite_textures = rnjesus.choices(tuple(Sprites_.sprite_alias), k=1, weights=(45, 1.1, 35, 1.1, 15, 1.5, 1))
            # 20, 15, 10, 5, 3,
            self.texture_mapping[xy] = rnjesus.choice(sprite_textures)
            self.is_new_tile = True
        return Sprites_.sprite_alias[self.texture_mapping[xy]]

    def get_tile_id(self, vector):
        """
        return the numeric id of the texture at the given vector position
        """
        self.tile_type_pos(vector.x, vector.y)
        return self.texture_mapping[f'{vector.x} {vector.y}']

    @property
    def screen_center(self):
        return Vector.Vector(self.window.width / 2, self.window.height / 2)

    @property
    def cell_render_size(self):
        return self.cell_size * ((self.window.width / self.default_window_size.x), (self.window.height / self.default_window_size.y))

    @staticmethod
    def generate_radius(radius):
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                yield x, y

    def give_gold(self, amount):
        self.player.gold += round((((self.player.floor - 1) / 100) + 1) * amount)

    def clear_current_floor_data(self, should_clear_grid=True):
        self.texture_mapping.clear()
        if should_clear_grid:
            home_tile = self.grid.get(0, 0)
            self.grid.interactable_tiles.clear()
            from W_Main_File.Tiles import Home_Tile
            if isinstance(home_tile, Home_Tile.HomeTile):
                self.grid.add(home_tile)

    # noinspection PyProtectedMember
    def render_mouse(self):
        # arcade.draw_texture_rectangle(self.window._mouse_x + 15, self.window._mouse_y - 15, 30, 30, Sprites_.knight_start_flipped)
        arcade.draw_circle_outline(self.window._mouse_x, self.window._mouse_y, 10, (0, 255, 0, 175), 2)
        arcade.draw_line(self.window._mouse_x - 10, self.window._mouse_y, self.window._mouse_x + 10, self.window._mouse_y, (0, 255, 0, 175))
        arcade.draw_line(self.window._mouse_x, self.window._mouse_y - 10, self.window._mouse_x, self.window._mouse_y + 10, (0, 255, 0, 175))


state = State()
