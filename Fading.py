from arcade import View
import Exploration
import Vector
from arcade import load_texture
from pathlib import Path
import State

CIRCLE_FADE_FRAMES = [
    # <-- is apparently called an "Octothorp", but anyways    \/ this can be typed {i:0>2}, bruh
    load_texture(Path('Circle_Fade_Frames') / f'circle_fade_{f"0{i}" if i < 10 else f"{i}"}.png')
    for i in range(1, 33)
]


class Fading(Exploration.Explore):
    def __init__(self, reset_pos: Vector.Vector = None):
        super().__init__()
        self.reset_pos = reset_pos
        self.current_frame = 0
        self.frame_count = 1

    def on_draw(self):
        super().on_draw()
        CIRCLE_FADE_FRAMES[self.current_frame].draw_scaled(*State.state.screen_center)

    def on_update(self, delta_time: float):
        self.frame_count += 1
        if not self.frame_count % 4:
            self.current_frame += 1
            self.current_frame %= 32
