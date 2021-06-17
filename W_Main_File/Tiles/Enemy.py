from abc import ABC
from typing import Tuple
import collections
from W_Main_File.Utilities import Vector, Action_Queue
from W_Main_File.Essentials import State
from W_Main_File.Data import Tile, Sprites_, Enemy_Data
import arcade
import random



class EnemyTile(Tile.Tile):

    def __init__(self, pos):
        from W_Main_File.Views import Exploration
        from W_Main_File.Views import Combat
        super().__init__(pos)
        self.fought = False
        self.called_on_enter = False
        self.explore = Exploration.Explore()
        self.current_opacity = 0
        self.combat = Combat.Combat(Enemy_Data.enemy_possibilities['Dragon']())

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
                    5, 5, should_reverse=True, should_freeze=True,
                    render=self.fading_render
                )
                ))

    def on_render_foreground(self, center, top_left, cell_size):
        if State.state.player.pos == self.pos:
            if State.state.is_moving:
                return
            if self.fought:
                if len(self.combat.combatant.name) < 7:
                    arcade.draw_rectangle_filled(center.x, center.y * 1.018, cell_size.x * 2.1, cell_size.y * 0.2, (0, 0, 0, self.current_opacity))
                    arcade.draw_rectangle_filled(center.x, center.y * 0.9786, cell_size.x * 1.45, cell_size.y * 0.118, (0, 0, 0, self.current_opacity))
                else:
                    arcade.draw_rectangle_filled(center.x, center.y * 1.018, cell_size.x * 2.3, cell_size.y * 0.2, (0, 0, 0, self.current_opacity))
                    arcade.draw_rectangle_filled(center.x, center.y * 0.9786, cell_size.x * 1.45, cell_size.y * 0.118, (0, 0, 0, self.current_opacity))

                arcade.draw_text(f'You have already fought this {self.combat.combatant.name}.\nKeep searching for more!', center.x, center.y,
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
        self.current_opacity = min(200, self.current_opacity + 4)
        if not self.called_on_enter:
            self.on_enter()
            self.called_on_enter = True
