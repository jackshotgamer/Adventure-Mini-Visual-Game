import Exploration
import Vector
from arcade import load_texture, Sprite
from pathlib import Path
import State
from arcade import SpriteList
import random


forest_sprite = load_texture(Path('Sprites') / 'Forest_Tile_0.png')
plains_sprite = load_texture(Path('Sprites') / 'Plains_Tile_0.png')
village_sprite = load_texture(Path('Sprites') / 'Village_Tile_1.png')
home_sprite = load_texture(Path('Sprites') / 'Home_Tile.png')
chest_sprite = load_texture(Path('Sprites') / 'Chest_0.png')
black_sprite = load_texture(Path('Sprites') / 'Black_Square.png')
black_circle_sprite = load_texture(Path('Sprites') / 'Black_Circle.png')
black_circle_square_sprite = load_texture(Path('Sprites') / 'Black_Circle_Square.png')
black_square_circle_square_sprite = load_texture(Path('Sprites') / 'Black_Square_Square_Circle.png')

# 0 = Plains
# 1 = Forest
# 4 = Village
# 9 = House

# 2 = Mountain
# 3 = Desert
# 5 = Taiga
# 6 = Jungle
# 7 = Arctic
# 8 = Cave

sprite_alias = {
    '0': plains_sprite,
    '1': forest_sprite,
    '4': village_sprite
}

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
    if not backdrop_frame_count % 15:
        if current_backdrop_frame >= len(BACKGROUND_FRAMES) - 1:
            reversing = True
        elif current_backdrop_frame <= 0:
            reversing = False
        current_backdrop_frame += 1 if not reversing else -1
    if backdrop_frame_count > 20:
        backdrop_frame_count = 1


def draw_backdrop():
    import arcade
    arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y, 1000, 800, BACKGROUND_FRAMES[current_backdrop_frame])
