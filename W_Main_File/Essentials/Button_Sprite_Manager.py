import arcade
import arcade.gui

from W_Main_File.Data import Sprites_
from W_Main_File.Utilities.Vector import Vector
from collections import namedtuple

Button = namedtuple('Button', 'id_, text, center, size, idle_texture, hover_texture, click_texture, alpha, on_click, text_colour, text_size')


class ButtonManager:
    def __init__(self):
        self.buttons = {}
        self.hover_buttons = set()
        self.clicked_buttons = set()

    def append(self,
               id_: str,
               text: str,
               center: Vector,
               size: Vector,
               idle_texture: arcade.Texture = None,
               hover_texture: arcade.Texture = None,
               click_texture: arcade.Texture = None,
               alpha: int = 255,
               on_click=lambda: None,
               text_colour=(255, 255, 255),
               text_size=22
               ):
        if not idle_texture:
            idle_texture = Sprites_.blank_button_dark
        if not hover_texture:
            hover_texture = Sprites_.blank_button_light
        if not click_texture:
            click_texture = Sprites_.blank_button_light_middle
        self.buttons[id_] = Button(id_, text, center, size, idle_texture, hover_texture, click_texture, alpha, on_click, text_colour, text_size)

    def render(self):
        for button in self.buttons.values():
            if button.id_ not in self.hover_buttons and button.id_ not in self.clicked_buttons:
                arcade.draw_texture_rectangle(
                    button.center.x, button.center.y, button.size.x, button.size.y,
                    button.idle_texture, alpha=button.alpha
                )
            elif button.id_ not in self.clicked_buttons:
                arcade.draw_texture_rectangle(
                    button.center.x, button.center.y, button.size.x, button.size.y,
                    button.hover_texture, alpha=button.alpha
                )
            else:
                arcade.draw_texture_rectangle(
                    button.center.x, button.center.y, button.size.x, button.size.y,
                    button.click_texture, alpha=button.alpha
                )
            arcade.draw_text(
                button.text, button.center.x, button.center.y, button.text_colour, font_size=button.text_size,
                width=button.size.x, font_name='arial', anchor_x='center', anchor_y='center', align='center'
            )

    def remove(self, id_):
        if id_ in self.buttons:
            del self.buttons[id_]

    def on_click_check(self, x, y):
        self.check_hovered(x, y)
        for id_ in self.hover_buttons:
            self.clicked_buttons.add(id_)

    def on_click_release(self):
        self.clicked_buttons.clear()
        for id_ in self.hover_buttons:
            self.buttons[id_].on_click()

    def check_hovered(self, mouse_x, mouse_y):
        for button in self.buttons.values():
            if (
                    mouse_x in range(int(button.center.x - (button.size.x / 2)), int((button.center.x + (button.size.x / 2)) + 1))
                    and
                    mouse_y in range(int(button.center.y - (button.size.y / 2)), int((button.center.y + (button.size.y / 2)) + 1))
            ):
                self.hover_buttons.add(button.id_)
            else:
                self.hover_buttons.discard(button.id_)
