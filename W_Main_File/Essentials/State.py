import json
import pathlib
import random
from typing import List, Dict, Any, Union, Type

import arcade

from W_Main_File.Data import HpEntity, Grid, Sprites_, Meta_Data
from W_Main_File.Utilities import Vector, Seeding


class CacheState:
    def __init__(self):
        self._values = {}

    def __getattr__(self, item):
        return self._values.get(item)

    def __setattr__(self, key, value):
        if key == '_values':
            self.__dict__[key] = value
            return
        self._values[key] = value

    def __delattr__(self, item):
        if item in self._values:
            del self._values[item]

    def clear(self):
        self._values.clear()


class State:
    player_data_path = pathlib.Path('PLAYERDATA/')

    def __init__(self):
        self.player = HpEntity.HpEntity('', Vector.Vector(0, 0), 1000, 1000, 0, 0, 1, 1, Meta_Data.MetaData(is_player=True))
        self.camera_pos = Vector.Vector(0, 0)
        self.window = None
        self.grid = Grid.Grid()
        self.cell_size = Vector.Vector(100, 100)
        self.render_radius = 3
        self.default_window_size = Vector.Vector(1000, 800)
        self.texture_mapping = {}
        from W_Main_File.Items.Inventory import InventoryContainer
        self.inventory = InventoryContainer()
        self.current_page = 0
        self.is_new_tile = False
        self.is_moving = False
        self.moves_since_texture_save = 0
        self._preoccupied = False
        self.debug_mode = False
        # Meta_Data.is_me = True

    @property
    def grid_camera_pos(self):
        return (self.camera_pos / self.cell_render_size).rounded()

    @property
    def grid_camera_pos_raw(self):
        return self.camera_pos / self.cell_render_size

    @property
    def pos_of_player_on_screen(self):
        return ((self.player.pos * self.cell_render_size) - self.camera_pos) + self.screen_center

    @property
    def preoccupied(self):
        return self._preoccupied

    @preoccupied.setter
    def preoccupied(self, value):
        if self._preoccupied == value:
            return
        from W_Main_File.Views import Event_Base
        Event_Base.symbols.clear()
        Event_Base.held_modifiers = 0
        self._preoccupied = value

    def tile_type_pos(self, x, y):
        poss = Vector.Vector(x, y)
        xy = f'{int(x)} {int(y)}'
        if xy not in self.texture_mapping:
            rnjesus = Seeding.seed_for_vector(poss)
            sprite_textures = rnjesus.choices(tuple(Sprites_.sprite_alias), k=1, weights=Sprites_.weights)
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
        return self.cell_size * ((self.window.width / self.default_window_size.xf), (self.window.height / self.default_window_size.yf))

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
cache_state = CacheState()
