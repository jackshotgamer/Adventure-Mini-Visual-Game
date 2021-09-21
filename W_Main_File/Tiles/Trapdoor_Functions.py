from typing import Tuple
import collections
from W_Main_File.Utilities import Vector, Action_Queue
from W_Main_File.Essentials import State
from W_Main_File.Data import Tile, Sprites_
from W_Main_File.Views import Fading, Exploration
import arcade
import random


## Play Animation for black screen + closed trapdoor load in
## Play Animation for trapdoor opening
## Play Animation for player going into trapdoor
## Reset Tile locations

## Make it so that if they are a multiple of 5 floors down, have a boss battle


class TrapdoorTile(Tile.Tile):
    current_opacity = 0

    def key_up(self, keycode, mods):

        if keycode == arcade.key.E and not State.state.preoccupied:
            from W_Main_File.Utilities import Inventory_GUI
            if Inventory_GUI.is_inv():
                return
            State.state.preoccupied = True
            explore = Exploration.Explore()
            Action_Queue.action_queue.append(
                lambda: State.state.window.show_view(
                    Fading.Fading(self.after_fadein, 7, 2,
                                  should_reverse=False,
                                  should_freeze=True,
                                  reset_pos=Vector.Vector(0, 0),
                                  render=lambda _: explore.on_draw()
                                  )))

    @staticmethod
    def invalidate_floor_data():
        State.state.clear_current_floor_data()

    def after_fadein(self):
        from W_Main_File.Utilities import Floor_Data_Saving, Seeding
        Floor_Data_Saving.FloorSaveManager.floor_save()
        print(State.state.player.floor)
        explore = Exploration.Explore()
        fade_to_explore = Fading.Fading(Exploration.Explore, 7, 2,
                                        should_reverse=False,
                                        should_freeze=True,
                                        only_reverse=True,
                                        halfway_func=lambda: self.invalidate_floor_data(),
                                        reset_floor=State.state.player.floor + 1,
                                        reset_pos=Vector.Vector(0, 0),
                                        render=lambda _: explore.on_draw())
        return fade_to_explore

    def on_render_foreground(self, center, top_left, cell_size):
        from W_Main_File.Utilities import Inventory_GUI
        if Inventory_GUI.is_inv():
            return
        if State.state.player.pos == self.pos:
            if State.state.is_moving:
                return
            arcade.draw_rectangle_filled(center.x, center.y, cell_size.x * 1.65, cell_size.y * 0.2, (0, 0, 0, self.current_opacity))
            arcade.draw_text(f'Press E to Enter Trapdoor!', State.state.screen_center.x, State.state.screen_center.y, (255, 69, 0, 220),
                             12, anchor_x='center', anchor_y='center')

    def on_update(self, delta_time):
        from W_Main_File.Utilities import Inventory_GUI
        if Inventory_GUI.is_inv():
            return
        self.current_opacity = min(200, self.current_opacity + 4)

    def on_enter(self):
        self.current_opacity = 0

    def persistent_data(self):
        return {
            'pos': self.pos
        }

    @classmethod
    def load_from_data(cls, persistent_data):
        return TrapdoorTile(persistent_data['pos'])
