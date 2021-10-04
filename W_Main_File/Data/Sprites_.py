from arcade import load_texture
from pathlib import Path
from W_Main_File.Essentials import State

plains_sprite = load_texture(Path('Sprites') / 'Plains_Tile_0.png')
plains_trap_sprite = load_texture(Path('Sprites') / 'Plains_Tile_0_TRAP.png')
forest_sprite = load_texture(Path('Sprites') / 'Forest_Tile_2.0.png')
forest_trap_sprite = load_texture(Path('Sprites') / 'Forest_Tile_2.0_TRAP.png')
mountain_sprite = load_texture(Path('Sprites') / 'Mountain_Tile_1.png')
village_sprite = load_texture(Path('Sprites') / 'Village_Tile_1.png')
trapdoor_sprite = load_texture(Path('Sprites') / 'Trapdoor_Tile_0.png')
home_sprite = load_texture(Path('Sprites') / 'Home_Tile.png')
chest_sprite = load_texture(Path('Sprites') / 'Chest_0.png')
chest_body_sprite = load_texture(Path('Sprites') / 'Chest_Body_0.png')
trap_alert = load_texture(Path('Sprites') / 'Trap_Alert_0.png')
stick_sprite = load_texture(Path('Sprites') / 'Stick_Weapon_1.png')
rusty_knife_sprite = load_texture(Path('Sprites') / 'Rusty_Knife_1.png')
blank_button_dark = load_texture(Path('Sprites') / 'Button_Square_(No Decor)_0Dark.png')
blank_button_light = load_texture(Path('Sprites') / 'Button_Square_(No Decor)_1Light.png')
blank_button_light_middle = load_texture(Path('Sprites') / 'Button_Square_(No Decor)_2LightMiddle.png')
knight_start = load_texture(Path('Sprites') / 'Knight_Sprite_0_Start.png')
knight_start_2 = load_texture(Path('Sprites') / 'Knight_Sprite_0_Start_2_Foot.png')
knight_start_flipped = load_texture(Path('Sprites') / 'Knight_Sprite_0_Start_2_Foot_Flipped.png')
Null = load_texture(Path('Sprites') / 'X.png')
arrow_button_dark_left = load_texture(Path('Sprites') / 'ButtonArrow_DarkLeft.png')
arrow_button_dark_right = load_texture(Path('Sprites') / 'ButtonArrow_DarkRight.png')
arrow_button_light_left = load_texture(Path('Sprites') / 'ButtonArrow_LightLeft.png')
arrow_button_light_right = load_texture(Path('Sprites') / 'ButtonArrow_LightRight.png')
arrow_button_bright_left = load_texture(Path('Sprites') / 'ButtonArrow_BrightLeft.png')
arrow_button_bright_right = load_texture(Path('Sprites') / 'ButtonArrow_BrightRight.png')
# = load_texture(Path('Sprites') / '.png')
swamp_monster = load_texture(Path('Sprites') / 'Swamp_Monster_0.png')
black_sprite = load_texture(Path('Sprites') / 'Black_Square.png')
black_circle_sprite = load_texture(Path('Sprites') / 'Black_Circle.png')
black_circle_square_sprite = load_texture(Path('Sprites') / 'Black_Circle_Square.png')
black_square_circle_square_sprite = load_texture(Path('Sprites') / 'Black_Square_Square_Circle.png')

sprite_id_to_texture = {
    'rusty_knifeDefaultWeapon': rusty_knife_sprite,
    'Null': Null,
}


def get_sprite_from_id(id_):
    return sprite_id_to_texture.get(id_, Null)


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
    '4': village_sprite,
    '10': trapdoor_sprite
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
    load_texture(Path('Sprites') / 'Knight_Sprite_1_2.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_2_2.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_3_2.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_4.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_5.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_6.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_7.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_8.png'),
]

FLIPPED_CHARACTER_FRAMES = [
    load_texture(Path('Sprites') / 'Knight_Sprite_1_2_Flipped.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_2_2_Flipped.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_3_2_Flipped.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_4_Flipped.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_5_Flipped.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_6_Flipped.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_7_Flipped.png'),
    load_texture(Path('Sprites') / 'Knight_Sprite_8_Flipped.png'),
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


current_character_frame = 0
character_frame_count = 0


def update_character():
    global current_character_frame
    global character_frame_count
    character_frame_count += 1
    if character_frame_count > 18:
        character_frame_count = 1
    if not character_frame_count % 3:
        if current_character_frame >= len(CHARACTER_FRAMES) - 1:
            current_character_frame = -1
        current_character_frame += 1


def draw_backdrop():
    import arcade
    arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y, State.state.window.width, State.state.window.height, BACKGROUND_FRAMES[current_backdrop_frame])


def draw_character():
    import arcade
    from W_Main_File.Views.Exploration import Explore
    if Explore.symbol_ in (arcade.key.W, arcade.key.D):
        frames = CHARACTER_FRAMES[current_character_frame]
    else:
        frames = FLIPPED_CHARACTER_FRAMES[current_character_frame]
    arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y - 1,
                                  State.state.cell_render_size.y * 0.75, State.state.cell_render_size.y * 0.75,
                                  frames)
