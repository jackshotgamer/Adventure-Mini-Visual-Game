from arcade import load_texture
from pathlib import Path
from W_Main_File.Essentials import State

plains_sprite = load_texture(Path('Sprites') / 'Plains_Tile_0.png')
plains_trap_sprite = load_texture(Path('Sprites') / 'Plains_Tile_0_TRAP.png')
forest_sprite = load_texture(Path('Sprites') / 'Forest_Tile_2.0.png')
forest_trap_sprite = load_texture(Path('Sprites') / 'Forest_Tile_2.0_TRAP.png')
mountain_sprite = load_texture(Path('Sprites') / 'Mountain_Tile_1.png')
village_sprite = load_texture(Path('Sprites') / 'Village_Tile_1.png')
home_sprite = load_texture(Path('Sprites') / 'Home_Tile.png')
chest_sprite = load_texture(Path('Sprites') / 'Chest_0.png')
chest_body_sprite = load_texture(Path('Sprites') / 'Chest_Body_0.png')
trap_alert = load_texture(Path('Sprites') / 'Trap_Alert_0.png')
stick_sprite = load_texture(Path('Sprites') / 'Stick_Weapon_1.png')
rusty_knife_sprite = load_texture(Path('Sprites') / 'Rusty_Knife_1.png')
blank_button_dark = load_texture(Path('Sprites') / 'Button_Square_(No Decor)_0Dark.png')
blank_button_light = load_texture(Path('Sprites') / 'Button_Square_(No Decor)_1Light.png')
blank_button_light_middle = load_texture(Path('Sprites') / 'Button_Square_(No Decor)_2LightMiddle.png')
# temp_2 = load_texture(Path('Sprites') / '.png')
# temp_3 = load_texture(Path('Sprites') / '.png')
# temp_4 = load_texture(Path('Sprites') / '.png')
# temp_5 = load_texture(Path('Sprites') / '.png')
black_sprite = load_texture(Path('Sprites') / 'Black_Square.png')
black_circle_sprite = load_texture(Path('Sprites') / 'Black_Circle.png')
black_circle_square_sprite = load_texture(Path('Sprites') / 'Black_Circle_Square.png')
black_square_circle_square_sprite = load_texture(Path('Sprites') / 'Black_Square_Square_Circle.png')

# 0 = Plains
# 0.5 = Plains TRAP
# 1 = Forest
# 1.5 = Forest TRAP
# 2 = Mountain
# 4 = Village
# 9 = House

# 3 = Desert
# 5 = Taiga
# 6 = Jungle
# 7 = Arctic
# 8 = Cave

sprite_alias = {
    '0': plains_sprite,
    '0.5': plains_trap_sprite,
    '1': forest_sprite,
    '1.5': forest_trap_sprite,
    '2': mountain_sprite,
    '4': village_sprite
}

CHEST_OPENING_FRAMES = [
    load_texture(Path('Chest_Opening_Frames') / 'chest_sprite_0.png'),
    load_texture(Path('Chest_Opening_Frames') / 'chest_sprite_1.png'),
    load_texture(Path('Chest_Opening_Frames') / 'chest_sprite_2.png'),
    load_texture(Path('Chest_Opening_Frames') / 'chest_sprite_3.png'),
    load_texture(Path('Chest_Opening_Frames') / 'chest_sprite_4.png'),
    load_texture(Path('Chest_Opening_Frames') / 'chest_sprite_5.png'),
    load_texture(Path('Chest_Opening_Frames') / 'chest_sprite_6.png'),
    load_texture(Path('Chest_Opening_Frames') / 'chest_sprite_7.png'),
    load_texture(Path('Chest_Opening_Frames') / 'chest_sprite_8.png')
]

BACKGROUND_FRAMES = [
    load_texture(Path('Background_Frames') / 'backdrop_1.png'),
    load_texture(Path('Background_Frames') / 'backdrop_2.png'),
    load_texture(Path('Background_Frames') / 'backdrop_3.png'),
    load_texture(Path('Background_Frames') / 'backdrop_4.png'),
    load_texture(Path('Background_Frames') / 'backdrop_5.png'),
    load_texture(Path('Background_Frames') / 'backdrop_6.png'),
    load_texture(Path('Background_Frames') / 'backdrop_7.png')
]

CHARACTER_FRAMES = [
    load_texture(Path('Sprites') / 'Knight_Sprite_1.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_2.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_3.png')
    # load_texture(Path('Sprites') / 'Knight_Sprite_0_Start.png')
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
