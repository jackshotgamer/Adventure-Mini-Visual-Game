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


class CursorPriorityManager(gui.UIManager):
    def on_draw(self):
        super().on_draw()


class PlayerSelect(Event_Base.EventBase):
    def __init__(self):
        super().__init__()
        arcade.set_background_color((0, 0, 0))
        self.ui_manager = CursorPriorityManager()
        self.ui_manager.purge_ui_elements()
        self.username = None
        self.password = None
        self.current_window_size = Vector.Vector(1000, 800)
        self.incorrect_password_end = 0
        self.buttons()
        State.state.clear_current_floor_data()

    def enter_button(self):
        player_username = self.username.text.strip()
        player_password = self.password.text.strip()
        if not (player_username and player_password):
            return

        json_ = get(f'http://localhost:666/save_data?name={quote(player_username)}&pw={quote(player_password)}').json()
        if not json_['error']:
            state_player = State.state.player
            state_player.name = json_['player_name']
            State.state.pw = quote(player_password)
            state_player.hp = json_['hp']
            state_player.max_hp = json_['max_hp']
            state_player.pos = Vector.Vector(json_['x'], json_['y'])
            state_player.gold = json_['gold']
            state_player.xp = json_['xp']
            state_player.lvl = json_['lvl']
            state_player.floor = json_['floor']
            state_player.deaths = json_['deaths']
            State.state.inventory.load(state_player.name)
            state_player.meta_data.is_player = True
            state_player.meta_data.is_guest = False
            state_player.meta_data.is_enemy = False
            from W_Main_File.Utilities import Inventory_GUI
            Inventory_GUI._inventory_toggle = False
            State.state.preoccupied = False
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
            State.state.window.show_view(Exploration.Explore())
        else:
            self.incorrect_password_end = time.time() + 1.5

    def on_update(self, delta_time: float):
        self.check_if_resized()

    @staticmethod
    def exit_button():
        sys.exit()

    def buttons(self):
        self.ui_manager.purge_ui_elements()
        self.username = gui.UIInputBox(State.state.screen_center.x, State.state.screen_center.y + 100, 300, 50)
        self.username.text_adapter = LimitText()
        self.password = gui.UIInputBox(State.state.screen_center.x, State.state.screen_center.y + 50, 300, 50)
        self.password.text_adapter = LimitText()
        self.ui_manager.add_ui_element(self.username)
        self.ui_manager.add_ui_element(self.password)
        self.button_manager.append('Guest', 'Login as Guest', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y + 150), Vector.Vector(250, 50), on_click=self.guest_button)
        self.button_manager.append('Enter', 'Enter', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y), Vector.Vector(250, 50), on_click=self.enter_button)
        self.button_manager.append('Quit', 'Quit', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y - 50), Vector.Vector(100, 50), on_click=self.exit_button)

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
        import os
        if os.path.exists(f'Interactable_Tiles/Guest/'):
            shutil.rmtree(f'Interactable_Tiles/Guest/')
        from W_Main_File.Views import Exploration
        self.ui_manager.purge_ui_elements()
        Seeding.set_world_seed_from_player_name()
        State.state.window.show_view(Exploration.Explore())

    # noinspection PyProtectedMember
    def on_draw(self):
        super().on_draw()
        center_screen = Vector.Vector(self.window.width / 2, self.window.height / 2)
        arcade.draw_text('USERNAME:', center_screen.x - self.username.width + 45, self.username.center_y, arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20, anchor_x='center', anchor_y='center')
        arcade.draw_text('PASSWORD:', center_screen.x - self.password.width + 43, self.password.center_y, arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20, anchor_x='center', anchor_y='center')
        if self.incorrect_password_end > time.time():
            arcade.draw_text('Incorrect Password', State.state.screen_center.x, State.state.screen_center.y - 100, arcade.color.RED, font_name='arial', font_size=20, anchor_x='center',
                             anchor_y='center')
        State.state.render_mouse()


# noinspection PyUnresolvedReferences,PyProtectedMember,PyAttributeOutsideInit
class LimitText(gui.elements.inputbox._KeyAdapter):
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        if text != self._text:
            self.state_changed = True

        self._text = text[:15]
