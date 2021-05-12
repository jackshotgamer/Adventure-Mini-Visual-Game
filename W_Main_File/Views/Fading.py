from pathlib import Path

from arcade import load_texture, gui, View
import arcade
import random

from W_Main_File.Essentials import State
from W_Main_File.Utilities import Vector, Seeding

CIRCLE_FADE_FRAMES = [
    # <-- is apparently called an "Octothorp", but anyways    \/ this can be typed {i:0>2}, bruh
    load_texture(Path('Circle_Fade_Frames') / f'circle_fade_{f"0{i}" if i < 10 else f"{i}"}.png')
    for i in range(1, 33)
]


class Fading(View):
    def __init__(self, reset_screen_func, first_interval: int, second_interval: int = -1, should_reverse: bool = False, should_freeze: bool = False, only_reverse: bool = False,
                 should_reload_textures: bool = False,
                 reset_pos: Vector.Vector = None, reset_floor: int = None):
        from W_Main_File.Views import Exploration
        State.state.preoccupied = True
        super().__init__()
        self.explore = Exploration.Explore()
        self.moving = True
        self.reset_pos = reset_pos
        self.reset_floor = reset_floor
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
        self.should_reload_textures = should_reload_textures
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
                State.state.window.show_view(self.reset_screen_func())
            if self.reset_pos is not None:
                State.state.player.pos = Vector.Vector(*self.reset_pos)
            if self.reset_floor is not None:
                State.state.player.floor = self.reset_floor
            if self.should_reload_textures:
                State.state.texture_mapping.clear()
                Seeding.change_world_seed(random.randint(1, 75654655267269))
        if self.current_frame == -1:
            self.moving = False
            State.state.preoccupied = False
            State.state.window.show_view(self.reset_screen_func())

    def on_key_press(self, symbol: int, modifiers: int):
        return
