from pathlib import Path

from arcade import load_texture, gui, View
import arcade
import random

from W_Main_File.Essentials import State
from W_Main_File.Utilities import Vector, Seeding, Floor_Data_Saving

CIRCLE_FADE_FRAMES = [
    # <-- is apparently called an "Octothorp", but anyways    \/ this can be typed {i:0>2}, bruh
    load_texture(Path('Circle_Fade_Frames') / f'circle_fade_{f"0{i}" if i < 10 else f"{i}"}.png')
    for i in range(1, 33)
]


class Fading(View):
    def __init__(self, reset_screen_func, first_interval: int, second_interval: int = -1, should_reverse: bool = False, should_freeze: bool = False, only_reverse: bool = False,
                 reset_pos: Vector.Vector = None, reset_floor: int = None, finishing_func=lambda: None):
        from W_Main_File.Views import Exploration
        State.state.preoccupied = True
        super().__init__()
        self.explore = Exploration.Explore()
        self.moving = True
        self.reset_pos = reset_pos
        self.reset_floor_number = reset_floor
        self.current_frame = 0
        self.frame_count = 1
        self.reversing = False
        self.ui_manager = gui.UIManager()
        self.ui_manager.purge_ui_elements()
        self.reset_screen_func = reset_screen_func
        self.first_interval = first_interval
        self.second_interval = second_interval
        self.should_reverse = should_reverse
        self.should_freeze = should_freeze
        self.finishing_func = finishing_func
        if only_reverse:
            self.should_reverse = True
            self.reversing = True
            self.current_frame = len(CIRCLE_FADE_FRAMES) - 1

    def on_draw(self):
        arcade.start_render()
        self.explore.on_draw()
        CIRCLE_FADE_FRAMES[self.current_frame].draw_scaled(*State.state.screen_center)

    def update(self, delta_time: float):
        self.frame_count += 1
        if not self.frame_count % self.first_interval and not self.reversing:
            self.current_frame += 1
        if not self.frame_count % (self.second_interval if self.second_interval != -1 else self.first_interval) and self.reversing and self.should_reverse:
            self.current_frame -= 1
        if self.current_frame == len(CIRCLE_FADE_FRAMES) - 1:
            if self.should_reverse:
                self.reversing = True
            else:
                self.moving = False
                State.state.preoccupied = False
                self.go_to_next_view()
            if self.reset_pos is not None:
                State.state.player.pos = Vector.Vector(*self.reset_pos)
            if self.reset_floor_number is not None:
                Floor_Data_Saving.FloorSaveManager.load_floor(self.reset_floor_number)
                State.state.player.floor = self.reset_floor_number
        if self.current_frame == -1:
            self.moving = False
            State.state.preoccupied = False
            self.go_to_next_view()

    def go_to_next_view(self):
        self.finishing_func()
        State.state.window.show_view(self.reset_screen_func())

    def on_key_press(self, symbol: int, modifiers: int):
        return
