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
        arcade.draw_rectangle_filled(State.state.screen_center.x, State.state.screen_center.y, State.state.window.width * 0.5, State.state.window.height * 0.625, (20, 20, 20))
        arcade.draw_rectangle_outline(State.state.screen_center.x, State.state.screen_center.y, State.state.window.width * 0.5, State.state.window.height * 0.625, (120, 120, 120), 2)
