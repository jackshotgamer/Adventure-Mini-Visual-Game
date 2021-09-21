import arcade
import arcade.gui
from arcade import key

from W_Main_File.Utilities import Button_Functions, Action_Queue
from W_Main_File.Views import Purgatory_Screen, Event_Base
from W_Main_File.Data import Sprites_
from W_Main_File.Essentials import State
import time
import random
from W_Main_File.Tiles import Loot_Functions, Trapdoor_Functions, Trap_Functions, Enemy
from W_Main_File.Utilities.Vector import Vector

_inventory_toggle = False


def show_inv():
    global _inventory_toggle
    State.state.preoccupied = True
    _inventory_toggle = True


def hide_inv():
    global _inventory_toggle
    State.state.preoccupied = False
    _inventory_toggle = False


def is_inv():
    if _inventory_toggle:
        return True
    else:
        return False


def render_inventory():
    if _inventory_toggle:
        import numpy as np
        arcade.draw_rectangle_filled(State.state.screen_center.x, State.state.screen_center.y, State.state.window.width * 0.5, State.state.window.height * 0.625, (20, 20, 20))
        arcade.draw_rectangle_outline(State.state.screen_center.x, State.state.screen_center.y, State.state.window.width * 0.5, State.state.window.height * 0.625, (90, 90, 90), 6)
        for y in np.arange((State.state.window.height * 0.1875), (State.state.window.height * 0.8125), State.state.cell_render_size.y):
            arcade.draw_line(State.state.window.width * 0.25, y, State.state.window.width * 0.75, y, (90, 90, 90), 2)
        for x in np.arange((State.state.window.width * 0.25), (State.state.window.width * 0.75), State.state.cell_render_size.x):
            arcade.draw_line(x, State.state.window.height * 0.1875, x, State.state.window.height * 0.8125, (90, 90, 90), 2)
        from W_Main_File.Data import Item
        from W_Main_File.Items import All_Items
        if not State.state.inventory.items:
            knife = All_Items.rusty_knife
            State.state.inventory.add_item(knife)
        items = State.state.inventory.items
        origin_x, origin_y = (State.state.window.width * 0.25) + (State.state.cell_render_size.x / 2), (State.state.window.height * 0.8125) - (State.state.cell_render_size.y / 2)
        for index, item in enumerate(items):
            if index > 25:
                break
            x = index % 5
            y = index // 5
            arcade.draw_texture_rectangle((x * State.state.cell_render_size.x) + origin_x, ((y * -State.state.cell_render_size.y) + origin_y),
                                          99, 99, item.sprite, alpha=200 if item.sprite == Sprites_.Null else 255)
        if len(items) > 25:
            pass
