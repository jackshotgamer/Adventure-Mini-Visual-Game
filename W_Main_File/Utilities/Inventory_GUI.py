import arcade
import arcade.gui
from arcade import key
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from W_Main_File.Data.Item import Item
from W_Main_File.Utilities import Button_Functions, Action_Queue
from W_Main_File.Views import Purgatory_Screen, Event_Base
from W_Main_File.Data import Sprites_
from W_Main_File.Essentials import State, Button_Sprite_Manager
import time
import random
from W_Main_File.Tiles import Loot_Functions, Trapdoor_Functions, Trap_Functions, Enemy
from W_Main_File.Utilities.Vector import Vector

_inventory_toggle = False
_menu_toggle = False


def show_inv(button_manager: 'Button_Sprite_Manager.ButtonManager'):
    global _inventory_toggle
    State.state.preoccupied = True
    _inventory_toggle = True
    button_manager.append('LeftArrow', '', Vector(State.state.screen_center.x - (State.state.screen_center.x * .1), State.state.screen_center.y * .25),
                          Vector(State.state.window.width * .05, State.state.window.height * .0625),
                          Sprites_.arrow_button_dark_left, Sprites_.arrow_button_light_left, Sprites_.arrow_button_bright_left, on_click=lambda: Action_Queue.action_queue.append(page_left))
    button_manager.append('RightArrow', '', Vector(State.state.screen_center.x + (State.state.screen_center.x * .1), State.state.screen_center.y * .25),
                          Vector(State.state.window.width * .05, State.state.window.height * .06250),
                          Sprites_.arrow_button_dark_right, Sprites_.arrow_button_light_right, Sprites_.arrow_button_bright_right, on_click=lambda: Action_Queue.action_queue.append(page_right))


def page_left():
    for item in State.state.player.inventory.get_items_on_page(State.state.current_page):
        if item is not None:
            item.selected = False
    from W_Main_File.Views import Event_Base
    if State.state.current_page > 0 and not Event_Base.held_modifiers & arcade.key.MOD_SHIFT:
        State.state.current_page -= 1
    elif State.state.current_page > (0 + 4) and Event_Base.held_modifiers & arcade.key.MOD_SHIFT:
        State.state.current_page -= 5
    elif State.state.current_page > 0 and Event_Base.held_modifiers & arcade.key.MOD_SHIFT:
        State.state.current_page = 0


def page_right():
    for item in State.state.player.inventory.get_items_on_page(State.state.current_page):
        if item is not None:
            item.selected = False
    from W_Main_File.Views import Event_Base
    if State.state.current_page < State.state.player.inventory.page_count and not Event_Base.held_modifiers & arcade.key.MOD_SHIFT:
        State.state.current_page += 1
    elif State.state.current_page < (State.state.player.inventory.page_count - 4) and Event_Base.held_modifiers & arcade.key.MOD_SHIFT:
        State.state.current_page += 5
    elif State.state.current_page < State.state.player.inventory.page_count and Event_Base.held_modifiers & arcade.key.MOD_SHIFT:
        State.state.current_page = State.state.player.inventory.page_count


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


def inventory_nw():
    return Vector(((State.state.window.width * 0.25) + (State.state.cell_render_size.x / 2)) - ((State.state.window.width * 0.095) / 2),
                  ((State.state.window.height * 0.8125) - (State.state.cell_render_size.y / 2)) + ((State.state.window.height * 0.11875) / 2))


def inventory_se():
    return Vector(((State.state.window.width * 0.75) - (State.state.cell_render_size.x / 2)) + ((State.state.window.width * 0.095) / 2),
                  ((State.state.window.height * 0.1875) + (State.state.cell_render_size.y / 2)) - ((State.state.window.height * 0.11875) / 2))


def render_inventory(mouse_pos: Vector):
    if _inventory_toggle:
        import numpy as np
        arcade.draw_rectangle_filled(State.state.screen_center.x, State.state.screen_center.y, State.state.window.width * 0.5, State.state.window.height * 0.625, (20, 20, 20))
        arcade.draw_rectangle_outline(State.state.screen_center.x, State.state.screen_center.y, State.state.window.width * 0.5, State.state.window.height * 0.625, (90, 90, 90), 4)
        for y in np.arange((State.state.window.height * 0.1875), (State.state.window.height * 0.8125), State.state.cell_render_size.y):
            arcade.draw_line(State.state.window.width * 0.25, y, State.state.window.width * 0.75, y, (90, 90, 90), 2)
        for x in np.arange((State.state.window.width * 0.25), (State.state.window.width * 0.75), State.state.cell_render_size.x):
            arcade.draw_line(x, State.state.window.height * 0.1875, x, State.state.window.height * 0.8125, (90, 90, 90), 2)
        arcade.draw_rectangle_filled(State.state.screen_center.x, State.state.screen_center.y * .25, State.state.window.width * .05, State.state.window.height * .06250, arcade.color.BLACK)
        screen_percentage_of_default = (State.state.window.height / State.state.default_window_size.y)
        arcade.draw_text(f'Page:\n{State.state.current_page + 1}/{State.state.player.inventory.page_count + 1}', State.state.screen_center.x, State.state.screen_center.y * .25, arcade.color.LIGHT_GRAY,
                         font_size=(11 * screen_percentage_of_default), width=int(State.state.window.width * .05), align='center', font_name='arial', anchor_x='center', anchor_y='center')
        items = State.state.player.inventory.items
        origin_x, origin_y = (State.state.window.width * 0.25) + (State.state.cell_render_size.x / 2), (State.state.window.height * 0.8125) - (State.state.cell_render_size.y / 2)
        if items:
            item_length = len(items)
            inventory_contents = []
            for index, item in enumerate(range(0, item_length)):
                if index > State.state.player.inventory.page_size - 1:
                    break
                inventory_contents.append(State.state.player.inventory.get_item(index, State.state.current_page))
            for index, item in enumerate(inventory_contents):
                if index > 24:
                    break
                x = index % 5
                y = index // 5
                if item is not None:
                    sprite = item.sprite
                    # arcade.draw_rectangle_outline(inventory_nw().x, inventory_nw().y, State.state.window.width * 0.095, State.state.window.height * 0.11875, arcade.color.LIGHT_GRAY, 1)
                    arcade.draw_texture_rectangle((x * State.state.cell_render_size.x) + origin_x, ((y * -State.state.cell_render_size.y) + origin_y),
                                                  100, 100, sprite, alpha=100 if sprite == Sprites_.Null else 255)
                    if State.state.debug_mode:
                        arcade.draw_point((x * State.state.cell_render_size.x) + origin_x, ((y * -State.state.cell_render_size.y) + origin_y), arcade.color.GREEN, 4)
                    if item.selected:
                        arcade.draw_rectangle_outline((x * State.state.cell_render_size.x) + origin_x, ((y * -State.state.cell_render_size.y) + origin_y),
                                                      State.state.cell_render_size.x * 0.85, State.state.cell_render_size.y * 0.85, (200, 25, 25), 5)
        State.state.render_mouse()
        if not _menu_toggle:
            show_tooltips(mouse_pos)
        if len(items) > 25:
            pass
    else:
        State.state.render_mouse()


def sprite_from_text_image(image, key_: str = "Key"):
    text_sprite = arcade.Sprite()
    text_sprite._texture = arcade.Texture(key_)
    text_sprite.texture.image = image
    text_sprite.width = image.width
    text_sprite.height = image.height
    return text_sprite


def get_hovered_item_index(mouse_pos):
    origin_pos_nw = inventory_nw()
    mouse_pos_local = Vector(mouse_pos.x - origin_pos_nw.x, mouse_pos.y - origin_pos_nw.y)
    box_pos_int = Vector(int(mouse_pos_local.x / State.state.cell_render_size.x), int(mouse_pos_local.y / State.state.cell_render_size.y))
    return abs(box_pos_int.y * 5) + box_pos_int.x


def get_hovered_item(mouse_pos) -> "Item":
    return State.state.player.inventory.get_item(get_hovered_item_index(mouse_pos), State.state.current_page)


def show_tooltips(mouse_pos: Vector):
    items = State.state.player.inventory.items
    if not items:
        return
    origin_pos_nw = inventory_nw()
    origin_pos_se = inventory_se()
    origin_pos_sw = Vector(origin_pos_nw.x, origin_pos_se.y)
    origin_pos_ne = Vector(origin_pos_se.x, origin_pos_nw.y)
    if not ((origin_pos_sw.x < mouse_pos.x < origin_pos_ne.x) and (origin_pos_sw.y < mouse_pos.y < origin_pos_ne.y)):
        return
    # arcade.draw_text
    mouse_pos_local = Vector(mouse_pos.x - origin_pos_nw.x, mouse_pos.y - origin_pos_nw.y)
    box_pos_int = Vector(int(mouse_pos_local.x / State.state.cell_render_size.x), int(mouse_pos_local.y / State.state.cell_render_size.y))
    grid_pos = Vector((origin_pos_nw.x + (box_pos_int.x * State.state.cell_render_size.x)) + (State.state.cell_render_size.x / 2),
                      (origin_pos_nw.y + (box_pos_int.y * State.state.cell_render_size.y)) - (State.state.cell_render_size.y / 2))
    from W_Main_File.Items.Inventory import InventoryContainer
    from W_Main_File.Data import Item
    item: Item.Item = get_hovered_item(mouse_pos)
    if item is not None:
        if item.type_ is Item.ItemType.Weapon:
            item: Item.Weapon
            if item.has_elemental_damage:
                element_type = item.element_type().name.replace('_', ' ')
                text_image = arcade.get_text_image(f'Name: {item.name}\nType: {item.type_.name}\nDamage: {item.min_attack}'
                                                   f'-{item.max_attack}\nSpeed: {item.speed}\nRange: {item.range}\nElement: {element_type.title()}', arcade.color.GREEN, 14)
            else:
                text_image = arcade.get_text_image(f'Name: {item.name}\nType: {item.type_.name}\nDamage: {item.min_attack}-{item.max_attack}\nSpeed: {item.speed}\nRange: {item.range}',
                                                   arcade.color.GREEN, 14)
        else:
            text_image = arcade.get_text_image(f'Name: {item.name}\nType: {item.type_.name}', arcade.color.GREEN, 14)
    else:
        text_image = arcade.get_text_image('', (20, 20, 20), 1)
    image = sprite_from_text_image(text_image)
    offset = 10
    if item is not None:
        tooltip_center = Vector(mouse_pos.x + ((image.width / 2) + offset), mouse_pos.y - ((image.height / 2) + offset))
        arcade.draw_line(grid_pos.x, grid_pos.y, (tooltip_center.x - ((image.width + 20) / 2)), (tooltip_center.y + ((image.height + 20) / 2)), arcade.color.PINK, 3)
        arcade.draw_rectangle_filled(tooltip_center.x, tooltip_center.y, image.width + 20, image.height + 20, (40, 40, 40))
        arcade.draw_rectangle_outline(tooltip_center.x, tooltip_center.y, image.width + 20, image.height + 20, (40, 150, 40), 2)
    arcade.draw_texture_rectangle(mouse_pos.x + ((image.width / 2) + offset), mouse_pos.y - ((image.height / 2) + offset), image.width, image.height, image.texture)
