import arcade
from W_Main_File.Utilities import Vector
from dataclasses import dataclass


@dataclass()
class Menu:
    key: str
    pos: Vector.Vector
    offset: str
    title: str
    values_and_callbacks: dict
    show: bool
    image: arcade.sprite


class MenuManager:
    def __init__(self):
        self.menus = {}

    def get_corners(self, mode: str, pos, size):
        pass

    def make_menu(self, key, pos, offset: str, title: str, values_and_callbacks: dict, show: bool):
        text_image = arcade.get_text_image('\n'.join(values_and_callbacks.keys()).upper(), arcade.color.GREEN, 14)
        from W_Main_File.Utilities.Inventory_GUI import sprite_from_text_image
        image = sprite_from_text_image(text_image)
        self.menus[key] = (Menu(key, pos, offset, title, values_and_callbacks, show, image))

    def display_menu(self, key):
        if key in self.menus:
            menu = self.menus[key]
            image = menu.image
            if menu.show:
                tooltip_center = Vector.Vector(menu.pos.x + (image.width / 2), menu.pos.y - (image.height / 2))
                arcade.draw_rectangle_filled(tooltip_center.x, tooltip_center.y, image.width + 20, image.height + 20, (40, 40, 40))
                arcade.draw_rectangle_outline(tooltip_center.x, tooltip_center.y, image.width + 20, image.height + 20, (40, 150, 40), 2)
                arcade.draw_texture_rectangle(menu.pos.x + (image.width / 2), menu.pos.y - (image.height / 2), image.width, image.height, image.texture)

    def remove_menu(self, key):
        if key in self.menus:
            del self.menus[key]
