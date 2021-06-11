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
        self.combat = Combat.Combat(Enemy_Data.enemy_possibilities['Dragon']())

    def on_enter(self):
        from W_Main_File.Views import Combat
        from W_Main_File.Views import Fading
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

    def fading_render(self, state_):
        if state_ == 'fading' or not state_:
            self.explore.on_draw()
        elif state_ == 'reversing':
            self.combat.on_draw()

    def on_update(self, delta_time):
        if State.state.is_moving:
            return
        if not self.called_on_enter:
            self.on_enter()
            self.called_on_enter = True
