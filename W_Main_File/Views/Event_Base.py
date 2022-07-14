import arcade
import arcade.gui

from W_Main_File.Data import Sprites_
from W_Main_File.Utilities.Vector import Vector
from collections import namedtuple
from W_Main_File.Essentials import Button_Sprite_Manager, State

symbols = set()
held_modifiers = 0


class EventBase(arcade.View):
    def __init__(self):
        super().__init__()
        self.button_manager = Button_Sprite_Manager.ButtonManager()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.button_manager.check_hovered(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.button_manager.on_click_check(x, y)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        self.button_manager.on_click_release()
        State.state.window.set_mouse_visible(False)

    def on_draw(self):
        arcade.start_render()
        self.button_manager.render()

    def on_key_press(self, symbol: int, modifiers: int):
        global symbols
        global held_modifiers
        symbols.add(symbol)
        held_modifiers |= modifiers

    def on_key_release(self, _symbol: int, _modifiers: int):
        global symbols
        global held_modifiers
        if _symbol in symbols:
            symbols.remove(_symbol)
        held_modifiers &= _modifiers


"""
100 shift
010 ctrl

press a + shift
held_modifiers = 0b100

release shift
press b



"""
