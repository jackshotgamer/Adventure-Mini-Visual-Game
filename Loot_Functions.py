from typing import Tuple
import collections
import Exploration
import Vector
import State
import Tile
import arcade
import Sprites_
import random


class LootTable:
    def __init__(self, *items: Tuple[str, int]):
        self.items = collections.OrderedDict(items)

    def get_item(self):
        return random.choices(tuple(self.items), k=1, weights=tuple(self.items.values()))[0]


class LootTile(Tile.Tile):
    def __init__(self, pos):
        super().__init__(pos)
        self.current_opacity = 0
        self.looted = False

    def on_render_foreground(self, center, top_left, cell_size):
        if State.state.player.pos == self.pos:
            if State.state.is_moving:
                return
            arcade.draw_rectangle_filled(center.x, center.y, cell_size.x * 1, cell_size.y * 0.2, (0, 0, 0, self.current_opacity))
            if not self.looted:
                arcade.draw_text(f'Press E to Loot!', State.state.screen_center.x, State.state.screen_center.y, (255, 69, 0, 220),
                                 12, anchor_x='center', anchor_y='center')
            else:
                arcade.draw_text(f'Looted.', State.state.screen_center.x, State.state.screen_center.y, (255, 0, 0, 220),
                                 12, anchor_x='center', anchor_y='center')

    def on_update(self, delta_time):
        self.current_opacity = min(200, self.current_opacity + 4)

    def on_enter(self):
        self.current_opacity = 0

    def key_down(self, keycode, mods):
        if keycode == arcade.key.E and not self.looted:
            table = LootTable(('rusty knife', 8), ('iron knife', 5), ('iron short-sword', 4), ('iron broad-sword', 1))
            print(str(table.get_item()))
            self.looted = True
        elif keycode == arcade.key.H and State.state.player.meta_data.is_me and self.looted:
            self.looted = False
        elif keycode == arcade.key.E and self.looted:
            table = LootTable(('banana peel', 8), ('ball of seaweed', 6), ('rusty can', 4), ('broken stick', 2))
            print(str(table.get_item()))
            self.looted = True
