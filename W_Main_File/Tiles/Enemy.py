from abc import ABC
from typing import Tuple
import collections
from W_Main_File.Utilities import Vector, Action_Queue
from W_Main_File.Essentials import State
from W_Main_File.Data import Tile, Sprites_, Enemy_Data
import arcade
import random
import time

"""
self.combat.on_draw()
self.combat = Combat.Combat(Enemy_Data.enemy_possibilities['Dragon']())
"""


class EnemyTile(Tile.Tile):
    def __init__(self, pos):
        from W_Main_File.Views import Exploration
        from W_Main_File.Views import Combat
        super().__init__(pos)
        self.fought = False
        self.called_on_enter = False
        self.explore = Exploration.Explore()
        self.current_opacity = 0
        self.combat = Combat.Combat()
        self.alpha = 0
        self.dont_render_it = True
        self.tomes = 0

    def on_enter(self):
        from W_Main_File.Views import Combat
        from W_Main_File.Views import Fading
        self.current_opacity = 0
        if State.state.is_moving:
            return
        if not self.fought:
            Action_Queue.action_queue.append(
                lambda: State.state.window.show_view(Fading.Fading(
                    lambda: self.combat,
                    1, 1, should_reverse=True, should_freeze=True,
                    render=self.fading_render
                )
                ))

    def on_render(self, center, top_left, cell_size):
        from W_Main_File.Views.Exploration import Explore
        if (self.pos.x, self.pos.y) != (State.state.player.pos.x, State.state.player.pos.y):
            self.dont_render_it = False
        if self.fought and not self.dont_render_it:
            if self.alpha < 210:
                self.alpha = min(210, self.alpha + 1)
            arcade.draw_texture_rectangle(center.x, center.y, State.state.cell_render_size.x * 0.73, State.state.cell_render_size.yf * 0.88, Sprites_.black_square_circle_square_sprite,
                                          alpha=int(self.alpha / 1.68))
            arcade.draw_texture_rectangle(center.x, center.y, State.state.cell_render_size.x * 0.75, State.state.cell_render_size.y * 0.75, Sprites_.knight_start_2,
                                          alpha=self.alpha)
            arcade.draw_texture_rectangle(center.x, center.y, State.state.cell_render_size.x * 0.50, State.state.cell_render_size.y * 0.50, Sprites_.Null,
                                          alpha=int(self.alpha / 1.5))

    def on_render_foreground(self, center, top_left, cell_size):
        if State.state.player.pos.rounded() == self.pos:
            if State.state.is_moving:
                return
            from W_Main_File.Utilities import Inventory_GUI
            if Inventory_GUI.is_inv():
                return
            if self.fought:
                arcade.draw_rectangle_filled(center.x, center.y * 1.018, cell_size.x * 2.3, cell_size.y * 0.2, (0, 0, 0, self.current_opacity))
                arcade.draw_rectangle_filled(center.x, center.y * 0.9786, cell_size.x * 1.45, cell_size.y * 0.118, (0, 0, 0, self.current_opacity))

                arcade.draw_text(f'You have already fought this enemy!.\nKeep searching for more!', center.x, center.y,
                                 (255, 200, 0), align='center', anchor_x='center', anchor_y='center', font_size=11)

    def fading_render(self, state_):
        if state_ == 'fading' or not state_:
            self.explore.on_draw()
        elif state_ == 'reversing':
            self.fought = True
            self.combat.on_draw()

    def on_update(self, delta_time):
        if State.state.is_moving:
            return
        from W_Main_File.Utilities import Inventory_GUI
        if Inventory_GUI.is_inv():
            return
        self.current_opacity = min(200, self.current_opacity + 4)
        if not self.called_on_enter:
            self.on_enter()
            self.called_on_enter = True

    def persistent_data(self):
        return {
            'pos': self.pos,
            'fought': self.fought,
        }

    @classmethod
    def load_from_data(cls, persistent_data):
        tile = EnemyTile(persistent_data['pos'])
        tile.fought = persistent_data['fought']
        if not tile.fought:
            tile.dont_render_it = True
        else:
            tile.dont_render_it = False
        return tile

    def on_exit(self):
        super().on_exit()
        State.state.preoccupied = False
