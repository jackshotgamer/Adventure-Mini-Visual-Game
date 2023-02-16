from arcade import load_texture
from pathlib import Path
from collections import OrderedDict
from PIL import Image
import numpy as np
import arcade

from W_Main_File.Data.Item import ItemType
from W_Main_File.Utilities import Vector
from W_Main_File.Essentials import State
from W_Main_File.Data import Item
black_rapier = load_texture(Path('Sprites') / 'Black_Rapier_1.png')
dark_bident = load_texture(Path('Sprites') / 'dark_bident.png')
moon_axe = load_texture(Path('Sprites') / 'moon_axe.png')
steel_billhook = load_texture(Path('Sprites') / 'steel_Billhook.png')
steel_sword = load_texture(Path('Sprites') / 'steel_sword.png')
dane_axe = load_texture(Path('Sprites') / 'Dane_Axe.png')
billhook = load_texture(Path('Sprites') / 'Billhook.png')
iron_sword = load_texture(Path('Sprites') / 'iron_sword.png')
spear = load_texture(Path('Sprites') / 'spear.png')
saber = load_texture(Path('Sprites') / 'saber.png')
partisan = load_texture(Path('Sprites') / 'Partisan.png')
horseman_blade = load_texture(Path('Sprites') / 'Horsemans_Blade.png')
pole = load_texture(Path('Sprites') / 'pole.png')
metal_mace = load_texture(Path('Sprites') / 'metal_mace.png')
death_knight = load_texture(Path('Sprites') / 'Death_Knight.png')
desert_plains_01 = load_texture(Path('Sprites') / 'desert_plains_1.png')
devouring_horror = load_texture(Path('Sprites') / 'Devouering_Horror.png')
golden_serpent = load_texture(Path('Sprites') / 'Golden_Serpent.png')
offspring_of_shub_niggurath = load_texture(Path('Sprites') / 'offspring_of_shub_niggurath.png')
purgatory_dragon_skeleton = load_texture(Path('Sprites') / 'Purgatory_dragon_skelleton.png')
snow_plains = load_texture(Path('Sprites') / 'snow_plains.png')
troglodyte = load_texture(Path('Sprites') / 'Troglodyte.png')
troglodyte_hellebardier = load_texture(Path('Sprites') / 'Troglodyte_Hellebardier.png')

plains_sprite_01 = load_texture(Path('Sprites') / 'Plains_Tile_01.png')
plains_sprite_02 = load_texture(Path('Sprites') / 'Plains_Tile_02.png')
plains_sprite_03 = load_texture(Path('Sprites') / 'Plains_Tile_03.png')
plains_sprite_04 = load_texture(Path('Sprites') / 'Plains_Tile_04.png')
purgatory_plain_01 = load_texture(Path('Sprites') / 'Purgatory_plain2.png')
purgatory_plain_02 = load_texture(Path('Sprites') / 'Purgatory_plain_2.png')
purgatory_mountain_01 = load_texture(Path('Sprites') / 'Purgatory_mountain_1.png')
purgatory_mountain_02 = load_texture(Path('Sprites') / 'Purgatory_mountains2.png')
plains_trap_sprite = load_texture(Path('Sprites') / 'Plains_Tile_0_TRAP.png')
forest_sprite_1 = load_texture(Path('Sprites') / 'Forest_Tile_2.png')
forest_sprite_11 = load_texture(Path('Sprites') / 'Forest_Tile_2.1.png')
forest_sprite_12 = load_texture(Path('Sprites') / 'Forest_Tile_2.2.png')
forest_trap_sprite = load_texture(Path('Sprites') / 'Forest_Tile_2.0_TRAP.png')
mountain_sprite_1 = load_texture(Path('Sprites') / 'Mountain_Tile_1.png')
mountain_sprite_2 = load_texture(Path('Sprites') / 'Mountain_Tile_2.png')
mountain_sprite_3 = load_texture(Path('Sprites') / 'Mountain_Tile_3.png')
mountain_sprite_4 = load_texture(Path('Sprites') / 'Mountain_Tile_4.png')
village_sprite = load_texture(Path('Sprites') / 'Village_Tile_1.png')
village_sprite_02 = load_texture(Path('Sprites') / 'village_2_plains.png')
trapdoor_sprite = load_texture(Path('Sprites') / 'Trapdoor_Tile_0.png')
home_sprite = load_texture(Path('Sprites') / 'Home_Tile.png')
chest_sprite = load_texture(Path('Sprites') / 'Chest_0.png')
chest_body_sprite = load_texture(Path('Sprites') / 'Chest_Body_0.png')
trap_alert = load_texture(Path('Sprites') / 'Trap_Alert_0.png')
stick_sprite = load_texture(Path('Sprites') / 'Stick_Weapon_1.png')
rusty_knife_sprite = load_texture(Path('Sprites') / 'Rusty_Knife_1.png')
black_rapier_sprite = load_texture(Path('Sprites') / 'Black_Rapier_1.png')
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
barcode = load_texture(Path('Sprites') / 'Barcode_Sprite.png')
barcode2 = load_texture(Path('Sprites') / 'Barcode_Sprite_2.png')
# = load_texture(Path('Sprites') / '.png')
# = load_texture(Path('Sprites') / '.png')
# = load_texture(Path('Sprites') / '.png')
# = load_texture(Path('Sprites') / '.png')
combat_terrain = load_texture(Path('Sprites') / 'Combat_Terrain.png')
swamp_monster = load_texture(Path('Sprites') / 'Swamp_Monster_0.png')
black_sprite = load_texture(Path('Sprites') / 'Black_Square.png')
black_circle_sprite = load_texture(Path('Sprites') / 'Black_Circle.png')
black_circle_square_sprite = load_texture(Path('Sprites') / 'Black_Circle_Square.png')
black_square_circle_square_sprite = load_texture(Path('Sprites') / 'Black_Square_Square_Circle.png')

item_dict = OrderedDict(
    rusty_knife=lambda: Item.Weapon('Rusty Knife', 'rusty_knifeDefaultWeapon',
                                    6, 10, 9, 1, Item.DamageType.Cutting, False, rusty_knife_sprite),
    nullifier=lambda: Item.Weapon('Nullifier', 'null_weapon_1SpecialWeapon',
                                  0, 200, 10, 10, Item.DamageType.Null | Item.DamageType.Void_Elemental, True, Null),
    disannull=lambda: Item.Weapon('Disannull', 'null_weapon_2SpecialWeapon',
                                  100, 100, 10, 10, Item.DamageType.Null | Item.DamageType.Void_Elemental, True, Null),
    black_rapier=lambda: Item.Weapon('Black Rapier', 'black_rapierSpecialWeapon',
                                     30, 90, 8, 3, Item.DamageType.Cutting, True, black_rapier),
    billhook=lambda: Item.Weapon('Billhook', 'billhookDefaultWeapon',
                                 10, 40, 4, 6, Item.DamageType.Piercing, False, billhook),
    iron_sword=lambda: Item.Weapon('Iron Sword', 'iron_swordDefaultWeapon',
                                   25, 35, 7, 3, Item.DamageType.Cutting, False, iron_sword),
    spear=lambda: Item.Weapon('Spear', 'spearDefaultWeapon',
                              35, 40, 5, 6, Item.DamageType.Piercing, False, spear),
    saber=lambda: Item.Weapon('Saber', 'saberDefaultWeapon',
                              30, 40, 6, 3, Item.DamageType.Cutting, False, saber),
    partisan=lambda: Item.Weapon('Partisan', 'partisanDefaultWeapon',
                                 30, 45, 4, 6, Item.DamageType.Piercing, False, partisan),
    horseman_blade=lambda: Item.Weapon('Horseman\'s Blade', 'horseman_bladeBossWeapon',
                                       50, 70, 5, 4, Item.DamageType.Cutting | Item.DamageType.Spectral, False, horseman_blade),
    dane_axe=lambda: Item.Weapon('Dane Axe', 'dane_axeDefaultWeapon',
                                 65, 70, 2, 5, Item.DamageType.Cutting, False, dane_axe),
    pole=lambda: Item.Weapon('Pole', 'poleDefaultWeapon',
                             5, 25, 8, 5, Item.DamageType.Blunt, False, pole),
    metal_mace=lambda: Item.Weapon('Solid Metal Mace', 'metal_maceDefaultWeapon',
                                   15, 50, 2, 2, Item.DamageType.Blunt, False, metal_mace),
    dark_bident=lambda: Item.Weapon('Dark Bident', 'dark_bidentDefaultWeapon',
                                    10, 40, 7, 7, Item.DamageType.Piercing, False, dark_bident),
    moon_axe=lambda: Item.Weapon('Moon Axe', 'moon_axeDefaultWeapon',
                                 50, 80, 4, 5, Item.DamageType.Cutting, False, moon_axe),
    steel_billhook=lambda: Item.Weapon('Steel Billhook', 'steel_billhookDefaultWeapon',
                                       20, 50, 4, 6, Item.DamageType.Piercing, False, steel_billhook),
    steel_sword=lambda: Item.Weapon('Steel Sword', 'steel_swordDefaultWeapon',
                                    35, 45, 7, 3, Item.DamageType.Cutting, False, steel_sword),
)

# 3 = Desert
# 5 = Taiga
# 6 = Jungle
# 7 = Arctic
# 8 = Cave

ranges = {
    1: (0, 0, 0),
    2: (0, 0, 0),
    3: (0, 0, 0),
    4: (0, 0, 0),
    5: (1, -1, 0),
    6: (0, 0, 0),
}

safe_sprite_alias = ['0.1', '0.2', '0.3', '0.4']

sprite_alias_o = {
    '0.1': (plains_sprite_01, 11),
    '0.2': (plains_sprite_02, 11),
    '0.3': (plains_sprite_03, 11),
    '0.4': (plains_sprite_04, 11),
    '0.5': (plains_trap_sprite, 1.1),
    '1': (forest_sprite_1, 7),
    '1.1': (forest_sprite_11, 7),
    '1.2': (forest_sprite_12, 7),
    '1.5': (forest_trap_sprite, 1.1),
    '2': (mountain_sprite_1, 2),
    '2.1': (mountain_sprite_2, 2),
    '2.2': (mountain_sprite_3, 3),
    '2.3': (mountain_sprite_4, 3),
    '4': (village_sprite, 0.8),
    '4.1': (village_sprite_02, 0.8),
    '10': (trapdoor_sprite, 1)
    # total = 79.8
}

sprite_alias_p = {
    '0.1': (purgatory_plain_01, 11),
    '0.2': (purgatory_plain_02, 11),
    '0.3': (purgatory_plain_01, 11),
    '0.4': (purgatory_plain_02, 11),
    '0.5': (plains_trap_sprite, 1.1),
    '1': (forest_sprite_1, 7),
    '1.1': (forest_sprite_11, 7),
    '1.2': (forest_sprite_12, 7),
    '1.5': (forest_trap_sprite, 1.1),
    '2': (purgatory_mountain_01, 2),
    '2.1': (purgatory_mountain_02, 2),
    '2.2': (purgatory_mountain_01, 3),
    '2.3': (purgatory_mountain_02, 3),
    '4': (village_sprite, 0.8),
    '4.1': (village_sprite_02, 0.8),
    '10': (trapdoor_sprite, 1)
}

sprite_alias_options = {
    'Overworld': sprite_alias_o,
    'Purgatory': sprite_alias_p,
}

loot_options = {'1', '1.1', '1.2', '2', '2.1', '2.2', '2.3'}
enemy_options = {'1', '1.1', '1.2'}
trapdoor_options = ('10',)
trap_options = ('0.5', '1.5')
excluded_tiles = ('0.1', '0.2', '0.3', '0.4', '0.5', '1.5', '10')

CHEST_OPENING_FRAMES = [
    load_texture(Path('Chest_Opening_Frames') / f'chest_sprite_{num}.png') for num in range(0, 9)
]

BACKGROUND_FRAMES = [
    load_texture(Path('Background_Frames') / f'backdrop_{num}.png') for num in range(1, 8)
]

CHARACTER_FRAMES = [
    load_texture(Path('Sprites') / f'Knight_Sprite_{num}.png') for num in range(1, 9)
]

FLIPPED_CHARACTER_FRAMES = [
    load_texture(Path('Sprites') / f'Knight_Sprite_{num}_Flipped.png') for num in range(1, 9)
]

current_backdrop_frame = 0
backdrop_frame_count = 0
reversing = False


def texture_to_sprite(image, width=None, height=None):
    import arcade
    text_sprite = arcade.Sprite()
    text_sprite._texture = image
    text_sprite.width = image.width if width is None else width
    text_sprite.height = image.height if height is None else height
    return text_sprite


def nullify_image_area(image, size):
    image_array = np.array(image)
    image_array[int((image.height * .5) - (size.y * .5)): int((image.height * .5) + (size.y * .5)), int((image.width * .5) - (size.x * .5)): int((image.width * .5) + (size.x * .5))] = (0, 0, 0, 0)
    return Image.fromarray(image_array)


def nullify_image_area_with_other_image(image, image2, offset):
    image_array = np.array(image)
    image_array[int(0 + offset.y): int(image2.height + offset.y), int(0 + offset.x): int(image2.width + offset.x)] = (0, 0, 0, 0)
    return Image.fromarray(image_array)


def png_to_image(image_path):
    return Image.open(image_path)


_image_to_sprite_counter = 0


def image_to_texture(image: Image.Image):
    global _image_to_sprite_counter
    return arcade.Texture(f'Namernamer{(_image_to_sprite_counter := _image_to_sprite_counter + 1)}123Hi', image)


def update_backdrop():
    global current_backdrop_frame
    global backdrop_frame_count
    global reversing
    backdrop_frame_count += 1
    if not backdrop_frame_count % 13:
        if current_backdrop_frame >= len(BACKGROUND_FRAMES) - 1:
            reversing = True
        elif current_backdrop_frame <= 0:
            reversing = False
        current_backdrop_frame += 1 if not reversing else -1
    if backdrop_frame_count > 20:
        backdrop_frame_count = 1


crop_current_backdrop_frame = 0
crop_backdrop_frame_count = 0
crop_reversing = False
CROPPED_BACKGROUND_FRAMES = []


def renew_cropped_backdrop():
    global CROPPED_BACKGROUND_FRAMES
    CROPPED_BACKGROUND_FRAMES = [
        image_to_texture(nullify_image_area(
            png_to_image(Path('Background_Frames') / f'backdrop_{num}.png').resize((int(State.state.window.width), int(State.state.window.height))),
            Vector.Vector(700, 700))) for num in range(1, 8)
    ]


def update_cropped_backdrop():
    global crop_current_backdrop_frame
    global crop_backdrop_frame_count
    global crop_reversing
    crop_backdrop_frame_count += 1
    if not crop_backdrop_frame_count % 13:
        if crop_current_backdrop_frame >= 7 - 1:
            crop_reversing = True
        elif crop_current_backdrop_frame <= 0:
            crop_reversing = False
        crop_current_backdrop_frame += 1 if not crop_reversing else -1
    if crop_backdrop_frame_count > 20:
        crop_backdrop_frame_count = 1


current_character_frame = 0
character_frame_count = 0


def update_character():
    global current_character_frame
    global character_frame_count
    character_frame_count += 1
    if character_frame_count > 18:
        character_frame_count = 1
    if not character_frame_count % 4:
        if current_character_frame >= len(CHARACTER_FRAMES) - 1:
            current_character_frame = -1
        current_character_frame += 1


def draw_backdrop():
    import arcade
    arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y, State.state.window.width, State.state.window.height, BACKGROUND_FRAMES[current_backdrop_frame])


def draw_cropped_backdrop():
    import arcade
    arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y, State.state.window.width, State.state.window.height, CROPPED_BACKGROUND_FRAMES[crop_current_backdrop_frame])


def draw_character():
    import arcade
    from W_Main_File.Views.Exploration import Explore
    if Explore.symbol_ in (arcade.key.W, arcade.key.D):
        frames = CHARACTER_FRAMES[current_character_frame]
    else:
        frames = FLIPPED_CHARACTER_FRAMES[current_character_frame]
    arcade.draw_texture_rectangle(((State.state.player.pos.xf * State.state.cell_render_size.xf) - State.state.player.camera_pos.xf) + State.state.screen_center.xf,
                                  ((State.state.player.pos.yf * State.state.cell_render_size.yf) - State.state.player.camera_pos.yf) + State.state.screen_center.yf,
                                  State.state.cell_render_size.yf * 0.75, State.state.cell_render_size.yf * 0.75,
                                  frames)
