from typing import Tuple
import collections
from W_Main_File.Utilities import Vector
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
            State.state.preoccupied = True
            State.state.window.show_view(Fading.Fading(Exploration.Explore, 7, 2, should_reverse=True, should_freeze=True, should_reload_textures=True,
                                                       reset_pos=Vector.Vector(0, 0), reset_floor=State.state.player.floor + 1))

    def on_render_foreground(self, center, top_left, cell_size):
        if State.state.player.pos == self.pos:
            if State.state.is_moving:
                return
            arcade.draw_rectangle_filled(center.x, center.y, cell_size.x * 1.65, cell_size.y * 0.2, (0, 0, 0, self.current_opacity))
            arcade.draw_text(f'Press E to Enter Trapdoor!', State.state.screen_center.x, State.state.screen_center.y, (255, 69, 0, 220),
                             12, anchor_x='center', anchor_y='center')

    def on_update(self, delta_time):
        self.current_opacity = min(200, self.current_opacity + 4)

    def on_enter(self):
        self.current_opacity = 0

    #     self.current_opacity = 0
    #     self.opening = False
    #     self.frame_step = 0
    #     self.elapsed_frames = 0
    #     self.true = True
    #     self.alpha = 0
    #     self.opened = False
    #     self.weapon_sprite_pos = Vector.Vector(0, -15)
    #     self.waiting = 0
    #
    # def on_render_foreground(self, center, top_left, cell_size):
    #     if State.state.player.pos == self.pos and not self.opening:
    #         if State.state.is_moving:
    #             return
    #         arcade.draw_rectangle_filled(center.x, center.y, cell_size.x * 1, cell_size.y * 0.2, (0, 0, 0, self.current_opacity))
    #         if not self.entered:
    #             arcade.draw_text(f'Press E to Enter Trapdoor!', State.state.screen_center.x, State.state.screen_center.y, (255, 69, 0, 220),
    #                              12, anchor_x='center', anchor_y='center')
    #         else:
    #             arcade.draw_text(f'Entered.', State.state.screen_center.x, State.state.screen_center.y, (255, 0, 0, 220),
    #                              12, anchor_x='center', anchor_y='center')
    #     elif State.state.player.pos == self.pos and self.opening:
    #         arcade.draw_rectangle_filled(State.state.screen_center.x, State.state.screen_center.y - (State.state.cell_size.y * 1.5), 300, 200, (0, 0, 0, self.alpha))
    #         if self.alpha < 255:
    #             arcade.draw_texture_rectangle(State.state.screen_center.x, (State.state.screen_center.y - (State.state.cell_size.y * 2)),
    #             100, 100, Sprites_.CHEST_OPENING_FRAMES[0], alpha=self.alpha)
    #         if self.alpha == 255:
    #             arcade.draw_texture_rectangle(State.state.screen_center.x, (State.state.screen_center.y - (State.state.cell_size.y * 2)), 100, 100, Sprites_.CHEST_OPENING_FRAMES[self.frame_step])
    #             if self.opened:
    #                 chest_body = Vector.Vector(State.state.screen_center.x, (State.state.screen_center.y - (State.state.cell_size.y * 2)))
    #                 arcade.draw_texture_rectangle(chest_body.x, chest_body.y + self.weapon_sprite_pos.y, 50, 50, Sprites_.blank_button_dark)
    #                 arcade.draw_texture_rectangle(chest_body.x, chest_body.y, 100, 100, Sprites_.chest_body_sprite)
    #
    # def on_update(self, delta_time):
    #     self.current_opacity = min(200, self.current_opacity + 4)
    #     if self.opening:
    #         self.alpha = min(255, self.alpha + 2)
    #     if self.alpha == 255:
    #         self.elapsed_frames += 1
    #         if not self.elapsed_frames % 10:
    #             self.frame_step += 1
    #         if self.frame_step > 8:
    #             self.frame_step = 8
    #             self.opened = True
    #         if self.opened and self.weapon_sprite_pos.y < 100:
    #             self.weapon_sprite_pos += 0, 1
    #         elif self.opened and self.weapon_sprite_pos.y >= 100:
    #             self.waiting += 1
    #             if self.waiting >= 60:
    #                 self.opening = False
    #                 State.state.preoccupied = False
    #
    # def on_enter(self):
    #     self.current_opacity = 0
    #     self.alpha = 0
    #     self.elapsed_frames = 0
    #     self.frame_step = 0
    #     self.weapon_sprite_pos = Vector.Vector(0, -15)
    #     self.opened = False
    #     self.waiting = 0
    #
    # def key_down(self, keycode, mods):
    #     if self.opening:
    #         return
    #     if keycode == arcade.key.E and not self.entered:
    #         self.opening = True
    #         self.entered = True
    #         State.state.preoccupied = True
    #     elif keycode == arcade.key.H and State.state.player.meta_data.is_me and self.entered:
    #         self.entered = False
    #         self.on_enter()
    #     elif keycode == arcade.key.E and self.entered:
    #         self.entered = True
