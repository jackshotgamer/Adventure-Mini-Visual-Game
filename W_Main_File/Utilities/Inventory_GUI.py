import arcade
import arcade.gui
from arcade import key

from W_Main_File.Utilities import Button_Functions, Action_Queue
from W_Main_File.Views import Purgatory_Screen, Event_Base
from W_Main_File.Data import Sprites_
from W_Main_File.Essentials import State, Button_Sprite_Manager
import time
import random
from W_Main_File.Tiles import Loot_Functions, Trapdoor_Functions, Trap_Functions, Enemy
from W_Main_File.Utilities.Vector import Vector

_inventory_toggle = False


def show_inv(button_manager: 'Button_Sprite_Manager.ButtonManager'):
    global _inventory_toggle
    State.state.preoccupied = True
    _inventory_toggle = True
    button_manager.append('LeftArrow', '', Vector(State.state.screen_center.x - (State.state.screen_center.x * .1), State.state.screen_center.y * .25),
                          Vector(State.state.window.width * .05, State.state.window.height * .0625),
                          Sprites_.arrow_button_dark_left, Sprites_.arrow_button_light_left, Sprites_.arrow_button_bright_left, on_click=page_left)
    button_manager.append('RightArrow', '', Vector(State.state.screen_center.x + (State.state.screen_center.x * .1), State.state.screen_center.y * .25),
                          Vector(State.state.window.width * .05, State.state.window.height * .06250),
                          Sprites_.arrow_button_dark_right, Sprites_.arrow_button_light_right, Sprites_.arrow_button_bright_right, on_click=page_right)


def page_left():
    from W_Main_File.Views import Event_Base
    if State.state.current_page > 0 and not Event_Base.held_modifiers & arcade.key.MOD_SHIFT:
        State.state.current_page -= 1
    elif State.state.current_page > (0 + 4) and Event_Base.held_modifiers & arcade.key.MOD_SHIFT:
        State.state.current_page -= 5
    elif State.state.current_page > 0 and Event_Base.held_modifiers & arcade.key.MOD_SHIFT:
        State.state.current_page = 0


def page_right():
    from W_Main_File.Views import Event_Base
    if State.state.current_page < State.state.inventory.page_count and not Event_Base.held_modifiers & arcade.key.MOD_SHIFT:
        State.state.current_page += 1
    elif State.state.current_page < (State.state.inventory.page_count - 4) and Event_Base.held_modifiers & arcade.key.MOD_SHIFT:
        State.state.current_page += 5
    elif State.state.current_page < State.state.inventory.page_count and Event_Base.held_modifiers & arcade.key.MOD_SHIFT:
        State.state.current_page = State.state.inventory.page_count


def hide_inv(button_manager: 'Button_Sprite_Manager.ButtonManager'):
    global _inventory_toggle
    State.state.preoccupied = False
    _inventory_toggle = False
    button_manager.remove('LeftArrow')
    button_manager.remove('RightArrow')


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
        arcade.draw_rectangle_filled(State.state.screen_center.x, State.state.screen_center.y * .25, State.state.window.width * .05, State.state.window.height * .06250, arcade.color.BLACK)
        screen_percentage_of_default = (State.state.window.height / State.state.default_window_size.y)
        arcade.draw_text(f'Page:\n{State.state.current_page + 1}/{State.state.inventory.page_count + 1}', State.state.screen_center.x, State.state.screen_center.y * .25, arcade.color.LIGHT_GRAY,
                         font_size=(11 * screen_percentage_of_default), width=int(State.state.window.width * .05), align='center', font_name='arial', anchor_x='center', anchor_y='center')
        from W_Main_File.Items import All_Items
        if not State.state.inventory.items:
            knife = All_Items.rusty_knife
            State.state.inventory.add_item(knife)
        items = State.state.inventory.items
        origin_x, origin_y = (State.state.window.width * 0.25) + (State.state.cell_render_size.x / 2), (State.state.window.height * 0.8125) - (State.state.cell_render_size.y / 2)
        if items:
            item_length = len(items)
            inventory_contents = []
            for index, item in enumerate(range(0, item_length)):
                if index > State.state.inventory.page_size - 1:
                    break
                inventory_contents.append(State.state.inventory.get_item(index, State.state.current_page))
            for index, item in enumerate(inventory_contents):
                if index > 24:
                    break
                x = index % 5
                y = index // 5
                if item is not None:
                    sprite = Sprites_.get_sprite_from_id(item.id_)
                    arcade.draw_rectangle_outline(((State.state.window.width * 0.25) + (State.state.cell_render_size.x / 2)) - ((State.state.window.width * 0.095) / 2),
                                                  ((State.state.window.height * 0.8125) - (State.state.cell_render_size.y / 2)) + ((State.state.window.height * 0.11875) / 2),
                                                  State.state.window.width * 0.095, State.state.window.height * 0.11875, arcade.color.LIGHT_GRAY, 1)
                    arcade.draw_texture_rectangle((x * State.state.cell_render_size.x) + origin_x, ((y * -State.state.cell_render_size.y) + origin_y),
                                                  99, 99, sprite, alpha=200 if sprite == Sprites_.Null else 255)
        if len(items) > 25:
            pass


def show_tooltips(mouse_x, mouse_y):
    items = State.state.inventory.items
    mouse_pos = Vector(mouse_x, mouse_y)
    if items:
        origin_x = ((State.state.window.width * 0.25) + (State.state.cell_render_size.x / 2)) - ((State.state.window.width * 0.095) / 2)
        origin_y = ((State.state.window.height * 0.8125) - (State.state.cell_render_size.y / 2)) + ((State.state.window.height * 0.11875) / 2)
        item_length = len(items)
        inventory_contents = []
        for index, item in enumerate(range(0, item_length)):
            if index > State.state.inventory.page_size - 1:
                break
            inventory_contents.append(State.state.inventory.get_item(index, State.state.current_page))
        for index, item in enumerate(inventory_contents):
            if index > 24:
                break


