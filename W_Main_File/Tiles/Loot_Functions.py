from typing import Tuple
import collections

from W_Main_File.Utilities import Vector
from W_Main_File.Essentials import State
from W_Main_File.Data import Tile, Sprites_, Item
import arcade
import random


def is_opening_chest():
    if tile := State.state.grid.get(*State.state.player.pos.rounded()):
        if isinstance(tile, LootTile):
            return tile.opening


class LootTable:
    def __init__(self, *items: Tuple[str, int]):
        self.items = collections.OrderedDict(items)

    def get_item(self):
        return random.choices(tuple(self.items), k=1, weights=tuple(self.items.values()))[0]


class LootTile(Tile.Tile):
    loot_result_dict = {
        'Broken_Stick': Sprites_.stick_sprite,
        'Rusty_Knife': Sprites_.rusty_knife_sprite,
    }
    
    def __init__(self, pos):
        super().__init__(pos)
        self.current_opacity = 0
        self.looted = False
        self.opening = False
        self.frame_step = 0
        self.elapsed_frames = 0
        self.true = True
        self.alpha = 0
        self.opened = False
        self.weapon_sprite_pos = Vector.Vector(0, -15)
        self.waiting = 0
        self.given_item = False
        self.table = LootTable(('Broken_Stick', 8), ('Rusty_Knife', 8))  # , ('Iron Knife', 5), ('Iron Short-sword', 4), ('Iron Broad-sword', 1))

        self.loot_result = ''

    def on_render_foreground(self, center, top_left, cell_size):
        from W_Main_File.Utilities import Inventory_GUI
        if Inventory_GUI.is_inv():
            return
        if State.state.player.pos.rounded() == self.pos and not self.opening:
            if State.state.is_moving:
                return
            arcade.draw_rectangle_filled(center.x, center.y, State.state.cell_render_size.x * 1,
                                         State.state.cell_render_size.y * 0.2, (0, 0, 0, self.current_opacity))
            if not self.looted:
                arcade.draw_text(f'Press E to Loot!', center.x, center.y, (255, 69, 0, 220),
                                 12, anchor_x='center', anchor_y='center')
            else:
                arcade.draw_text(f'Looted.', center.x, center.y, (255, 0, 0, 220),
                                 12, anchor_x='center', anchor_y='center')
        elif State.state.player.pos.rounded() == self.pos and self.opening:
            arcade.draw_rectangle_filled(State.state.screen_center.x, State.state.screen_center.y - (State.state.cell_render_size.y * 1.5),
                                         (State.state.window.width * 0.3), (State.state.window.height * 0.25), (0, 0, 0, self.alpha))
            if self.alpha < 255:
                arcade.draw_texture_rectangle(State.state.screen_center.x, (State.state.screen_center.y - (State.state.cell_render_size.y * 2)),
                                              (State.state.window.width * 0.1), (State.state.window.height * 0.125), Sprites_.CHEST_OPENING_FRAMES[0], alpha=self.alpha)
            if self.alpha == 255:
                arcade.draw_texture_rectangle(State.state.screen_center.x, (State.state.screen_center.y - (State.state.cell_render_size.y * 2)),
                                              (State.state.window.width * 0.1), (State.state.window.height * 0.125), Sprites_.CHEST_OPENING_FRAMES[self.frame_step])
                if self.opened:
                    chest_body = Vector.Vector(State.state.screen_center.x, (State.state.screen_center.y - (State.state.cell_render_size.y * 2)))
                    arcade.draw_texture_rectangle(chest_body.x, chest_body.y + self.weapon_sprite_pos.y, (State.state.window.width * 0.05), (State.state.window.height * 0.0625), self.loot_result_dict[self.loot_result])
                    arcade.draw_texture_rectangle(chest_body.x, chest_body.y, (State.state.window.width * 0.1), (State.state.window.height * 0.125), Sprites_.chest_body_sprite)

    def can_player_move(self):
        if self.true == self.true:
            return not self.opening
        else:
            print('WHAT\nWARNING: Computer have become sentient, this is not a drill, i repeat, this is not a drill!')

    def get_item_from_loot_result(self):
        dict_ = {
            'Rusty_Knife': Sprites_.item_dict['rusty_knife'],
            'Nullifier': Sprites_.item_dict['nullifier'],
            'Disannull': Sprites_.item_dict['disannull']
        }
        if not self.loot_result == 'Broken_Stick':
            return dict_[self.loot_result]

    def on_update(self, delta_time):
        from W_Main_File.Utilities import Inventory_GUI
        if Inventory_GUI.is_inv():
            return
        multipler_speed = 1
        self.current_opacity = min(200, self.current_opacity + 4)
        if self.opening:
            self.alpha = min(255, self.alpha + (2 * multipler_speed))
        if self.alpha == 255:
            self.elapsed_frames += (1 * multipler_speed)
            if not self.elapsed_frames % 10:
                self.frame_step += 1
            if self.frame_step > 8:
                self.frame_step = 8
                if not self.opened:
                    self.loot_result = self.table.get_item()
                self.opened = True
            if self.opened and self.weapon_sprite_pos.y < 100:
                self.weapon_sprite_pos += 0, (1 * multipler_speed)
            elif self.opened and self.weapon_sprite_pos.y >= 100:
                if not self.given_item:
                    if self.loot_result == 'Broken_Stick':
                        self.given_item = True
                        return
                    item_to_add = self.get_item_from_loot_result()
                    State.state.inventory.add_item(item_to_add)
                    self.given_item = True
                self.waiting += (1 * multipler_speed)
                if self.waiting >= 60:
                    self.opening = False
                    if State.state.preoccupied:
                        State.state.preoccupied = False

    def on_enter(self):
        self.current_opacity = 0
        self.alpha = 0
        self.elapsed_frames = 0
        self.frame_step = 0
        self.weapon_sprite_pos = Vector.Vector(0, -15)
        self.opened = False
        self.waiting = 0
        self.loot_result = ''

    def key_up(self, keycode, mods):
        if self.opening:
            return
        from W_Main_File.Utilities import Inventory_GUI
        if Inventory_GUI.is_inv():
            return
        if keycode == arcade.key.E and not self.looted:
            self.opening = True
            self.looted = True
            State.state.preoccupied = True
        elif keycode == arcade.key.H and State.state.player.meta_data.is_me and self.looted:
            self.looted = False
            self.given_item = False
            self.on_enter()
        elif keycode == arcade.key.E and self.looted:
            table = LootTable(('Banana Peel', 8), ('Ball of Seaweed', 6), ('Rusty Can', 4))
            self.looted = True

    def persistent_data(self):
        return {
            'pos': self.pos,
            'looted': self.looted
        }

    @classmethod
    def load_from_data(cls, persistent_data):
        tile = LootTile(persistent_data['pos'])
        tile.looted = persistent_data['looted']
        return tile
