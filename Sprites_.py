import Exploration
import Vector
from arcade import load_texture, Sprite
from pathlib import Path
import State
from arcade import SpriteList


forest_sprite = load_texture(Path('Sprites') / 'Forest_Tile_0.png')
black_sprite = load_texture(Path('Sprites') / 'Black_Tile.png')

BACKGROUND_FRAMES = [
    load_texture(Path('Background_Frames') / 'backdrop_1.png'),
    load_texture(Path('Background_Frames') / 'backdrop_2.png'),
    load_texture(Path('Background_Frames') / 'backdrop_3.png'),
    load_texture(Path('Background_Frames') / 'backdrop_4.png'),
    load_texture(Path('Background_Frames') / 'backdrop_5.png'),
    load_texture(Path('Background_Frames') / 'backdrop_6.png'),
    load_texture(Path('Background_Frames') / 'backdrop_7.png')
]

current_backdrop_frame = 0
backdrop_frame_count = 0
reversing = False


def update_backdrop():
    global current_backdrop_frame
    global backdrop_frame_count
    global reversing
    backdrop_frame_count += 1
    if not backdrop_frame_count % 20:
        if current_backdrop_frame >= len(BACKGROUND_FRAMES) - 1:
            reversing = True
        elif current_backdrop_frame <= 0:
            reversing = False
        print(current_backdrop_frame)
        current_backdrop_frame += 1 if not reversing else -1
    if backdrop_frame_count > 20:
        backdrop_frame_count = 1


def draw_backdrop():
    import arcade
    arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y, 1000, 800, BACKGROUND_FRAMES[current_backdrop_frame])
