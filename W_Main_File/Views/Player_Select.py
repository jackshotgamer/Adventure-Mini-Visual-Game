import arcade
from arcade import gui
from urllib.parse import quote

from W_Main_File.Essentials import State, Button_Sprite_Manager
from W_Main_File.Utilities import Vector, Seeding, Floor_Data_Saving, Button_Functions
from requests import get
import time
import sys
# noinspection PyPackages
from . import Event_Base
from collections import namedtuple


class CursorPriorityManager(gui.UIManager):
    def on_draw(self):
        super().on_draw()
        if not State.state.preoccupied:
            State.state.render_mouse()


PlayerDataTemplate = namedtuple('PlayerDataTemplate', 'name pos max_hp hp gold xp level floor deaths')


class PlayerSelect(Event_Base.EventBase):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((0, 0, 0))
        self.ui_manager = CursorPriorityManager()
        self.ui_manager.purge_ui_elements()
        self.username = None
        self.current_window_size = Vector.Vector(1000, 800)
        self.incorrect_password_end = 0
        self.buttons()
        self.player_data = PlayerDataTemplate('Guest', Vector.Vector(0, 0), 1000, 1000, 0, 0, 1, 1, 0)
        State.state.clear_current_floor_data()

    def on_username_update(self, player):
        player_username = player.strip()
        if (not player_username) or (player_username.lower() == 'guest'):
            return
        from W_Main_File.Essentials.State import state
        import pickle
        if not (state.player_data_path / player / 'player').exists():
            self.player_data = PlayerDataTemplate('Guest', Vector.Vector(0, 0), 1000, 1000, 0, 0, 1, 1, 0)
            return
        with open((state.player_data_path / player / 'player'), 'rb') as file:
            data = pickle.load(file)
            self.player_data = PlayerDataTemplate(data['character_name'], Vector.Vector(data['player_x'], data['player_y']), data['max_hp'], data['hp'], data['gold'], data['xp'], data['lvl'],
                                                  data['floor'], data['deaths'])

    def enter_button(self):
        player_username = self.username.text.strip()
        if not player_username:
            return
        if player_username.lower() == 'guest':
            return
        from W_Main_File.Views.Saving import load_player_data
        print(f'Username: {player_username}')
        load_player_data(player_username)
        if State.state.player.lvl == 2:
            from W_Main_File.Data.Sprites_ import weights
            weights[4] = 100
        state_player = State.state.player
        print(f'State Name: {state_player.name}')
        State.state.inventory.load(state_player.name)
        state_player.meta_data.is_player = True
        state_player.meta_data.is_guest = False
        state_player.meta_data.is_enemy = False
        from W_Main_File.Utilities import Inventory_GUI
        Inventory_GUI._inventory_toggle = False
        State.state.preoccupied = False
        State.cache_state.clear()
        State.state.current_page = 0
        from W_Main_File.Views import Exploration
        self.ui_manager.purge_ui_elements()
        Seeding.set_world_seed_from_player_name()
        State.state.grid.interactable_tiles.clear()
        if State.state.player.floor != 1:
            State.state.grid.remove(Vector.Vector(0, 0))
        elif not State.state.grid.get(0, 0):
            from W_Main_File.Tiles import Home_Tile
            State.state.grid.add(Home_Tile.HomeTile(Vector.Vector(0, 0)))
        Floor_Data_Saving.FloorSaveManager.load_floor(state_player.floor, force_load=True)
        self.render_mouse = False
        State.state.window.show_view(Exploration.Explore())

    def on_update(self, delta_time: float):
        self.check_if_resized()

    @staticmethod
    def exit_button():
        arcade.close_window()

    def buttons(self):
        self.ui_manager.purge_ui_elements()
        self.username = gui.UIInputBox(State.state.screen_center.x, State.state.screen_center.y + 100, 300, 50)
        self.username.text_adapter = LimitText(self.on_username_update)
        self.ui_manager.add_ui_element(self.username)
        self.button_manager.append('Guest', 'Login as Guest', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y + 150), Vector.Vector(250, 50), on_click=self.guest_button)
        self.button_manager.append('Enter', 'Enter', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y + 50), Vector.Vector(250, 50), on_click=self.enter_button)
        self.button_manager.append('Quit', 'Quit', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y), Vector.Vector(100, 50), on_click=self.exit_button)

    def check_if_resized(self):
        if self.current_window_size.x == State.state.window.width and self.current_window_size.y == State.state.window.height:
            return
        else:
            self.buttons()
            self.current_window_size = Vector.Vector(State.state.window.width, State.state.window.height)

    def guest_button(self):
        state = State.state.player
        State.state.grid.interactable_tiles.clear()
        if not State.state.grid.get(0, 0):
            from W_Main_File.Tiles import Home_Tile
            State.state.grid.add(Home_Tile.HomeTile(Vector.Vector(0, 0)))
        import shutil
        state.name = 'Guest'
        state.meta_data.is_player = False
        state.meta_data.is_guest = True
        state.meta_data.is_enemy = False
        state.pos = Vector.Vector(0, 0)
        state.max_hp = 1000
        state.hp = 1000
        state.gold = 0
        state.xp = 0
        state.lvl = 1
        state.floor = 1
        state.deaths = 0
        from W_Main_File.Utilities import Inventory_GUI
        Inventory_GUI._inventory_toggle = False
        State.state.preoccupied = False
        State.cache_state.clear()
        State.state.camera_pos = Vector.Vector(0, 0)
        State.state.current_page = 0
        import os
        if os.path.exists(f'Interactable_Tiles/Guest/'):
            shutil.rmtree(f'Interactable_Tiles/Guest/')
        from W_Main_File.Views import Exploration
        self.ui_manager.purge_ui_elements()
        Seeding.set_world_seed_from_player_name()
        self.render_mouse = False
        State.state.window.show_view(Exploration.Explore())

    # noinspection PyProtectedMember
    def on_draw(self):
        self.render_mouse = True
        super().on_draw()
        center_screen = Vector.Vector(self.window.width / 2, self.window.height / 2)
        arcade.draw_text('USERNAME:', center_screen.x - self.username.width + 45, self.username.center_y, arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20, anchor_x='center', anchor_y='center')
        arcade.draw_text(f'Name: {self.username.text if self.username.text != "" else "Guest"}', center_screen.x - (73 - 1), (self.username.center_y - (75 + 125)), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20)
        arcade.draw_text(f'Position: X: {self.player_data.pos.x}, Y: {self.player_data.pos.y}', center_screen.x - (95 - 1), (self.username.center_y - (100 + 125)), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20)
        arcade.draw_text(f'Maximum HP: {self.player_data.max_hp}', center_screen.x - (156 - 1), (self.username.center_y - (125 + 125)), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20)
        arcade.draw_text(f'HP: {self.player_data.hp}', center_screen.x - (40 - 1), (self.username.center_y - (150 + 125)), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20)
        arcade.draw_text(f'Gold: {self.player_data.gold}', center_screen.x - (59 - 1), (self.username.center_y - (175 + 125)), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20)
        arcade.draw_text(f'XP: {self.player_data.xp}', center_screen.x - (39 - 1), (self.username.center_y - (200 + 125)), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20)
        arcade.draw_text(f'Level: {self.player_data.level}', center_screen.x - (66 - 1), (self.username.center_y - (225 + 125)), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20)
        arcade.draw_text(f'Floor: {self.player_data.floor}', center_screen.x - (63 - 1), (self.username.center_y - (250 + 125)), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20)
        arcade.draw_text(f'Deaths: {self.player_data.deaths}', center_screen.x - (85 - 1), (self.username.center_y - (275 + 125)), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20)
        State.state.render_mouse()


# noinspection PyUnresolvedReferences,PyProtectedMember,PyAttributeOutsideInit
class LimitText(gui.elements.inputbox._KeyAdapter):
    def __init__(self, callback_on_change):
        super().__init__()
        self.callback_on_change = callback_on_change

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if text != self._text:
            self.state_changed = True
        self._text = text[:15]
        self.callback_on_change(self._text)
