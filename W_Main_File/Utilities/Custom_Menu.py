import typing

import arcade
from W_Main_File.Utilities import Vector
from dataclasses import dataclass


@dataclass()
class Menu:
    key: str
    pos: Vector.Vector
    offset: str
    values_and_callbacks: dict
    show: bool
    widest_text: int
    height_below_origin: int
    image: list


class MenuManager:
    def __init__(self):
        self.menus = {}

    def get_corners(self, mode: str, pos, size):
        pass

    def make_menu(self, key, pos, offset: str, values_and_callbacks: dict, show: bool):
        if values_and_callbacks is not None:
            from W_Main_File.Utilities.Inventory_GUI import sprite_from_text_image
            text_images = []
            widest_text = max(sprite_from_text_image(arcade.get_text_image(f'{key_}', arcade.color.GREEN, 24)).width for key_ in values_and_callbacks)
            height_below_origin = 0
            for index, key_ in enumerate(values_and_callbacks):
                text_image_sprite = sprite_from_text_image(arcade.get_text_image(f'{key_}', arcade.color.GREEN, 24, width=widest_text, align='center'))
                widest_text = max(widest_text, text_image_sprite.width)
                height_below_origin += text_image_sprite.height
                text_images.append((text_image_sprite, values_and_callbacks[key_], height_below_origin))
            menus_assign = Menu(key, pos, offset, values_and_callbacks, show, widest_text, height_below_origin, text_images)
            self.menus[key] = menus_assign

    def check_if_mouse_on_menu(self, key, mouse_pos: Vector.Vector):
        if key not in self.menus:
            return False
        menu = self.menus[key]
        if not menu.show:
            return False
        size = Vector.Vector(menu.widest_text, menu.height_below_origin)
        return menu.pos.x < mouse_pos.x < menu.pos.x + size.x and menu.pos.y - size.y < mouse_pos.y < menu.pos.y

    def check_which_hovered_option(self, key, relative_mouse_pos: Vector.Vector):
        if key not in self.menus:
            return False
        menu = self.menus[key]
        if not menu.show:
            return False
        # TODO returning wrong type of menu
        hovered_option_height_below_origin = abs(max(((relative_mouse_pos.y - images[2]) if (relative_mouse_pos.y - images[2]) <= 0 else -100000) for images in menu.image)) + relative_mouse_pos.y
        for item in menu.image:
            if item[2] == hovered_option_height_below_origin:
                return item
        return None, None

    def display_menu(self, key):
        if key in self.menus:
            menu = self.menus[key]
            images = menu.image
            if menu.show:
                tooltip_center = Vector.Vector(menu.pos.x + (menu.widest_text / 2), menu.pos.y - (menu.height_below_origin / 2))
                arcade.draw_rectangle_filled(tooltip_center.x, tooltip_center.y, menu.widest_text + 20, menu.height_below_origin + 20, (40, 40, 40))
                arcade.draw_rectangle_outline(tooltip_center.x, tooltip_center.y, menu.widest_text + 20, menu.height_below_origin + 20, (40, 150, 40), 2)
                image: tuple[arcade.Sprite, typing.Callable, float]
                for image in images:
                    arcade.draw_texture_rectangle(menu.pos.x + (menu.widest_text / 2), ((menu.pos.y - image[2]) + (image[0].height / 2)), menu.widest_text,
                                                  image[0].height, image[0].texture)
            return menu
        else:
            return None

    def remove_menu(self, key):
        if key in self.menus:
            del self.menus[key]
