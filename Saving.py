from arcade import View
import Exploration
import Vector
import arcade
from pathlib import Path
import State
import requests
import Networking


class Saving(View):
    def __init__(self):
        super().__init__()
        self.frame_count = 1
        self.saved = False

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text('Saving...', State.state.screen_center.x, State.state.screen_center.y, arcade.color.WHITE,
                         font_size=30, font_name='arial', anchor_x='center', anchor_y='center')

    def on_update(self, delta_time: float):
        self.frame_count += 1
        if self.frame_count >= 10 and not self.saved:
            Networking.save()
            self.saved = True
        if self.frame_count >= 15 and self.saved:
            State.state.window.show_view(Exploration.Explore())
