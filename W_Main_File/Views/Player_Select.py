import arcade
from arcade import gui
from urllib.parse import quote

from W_Main_File.Essentials import State, Button_Sprite_Manager
from W_Main_File.Utilities import Vector, Seeding, Floor_Data_Saving
import requests
import time
import sys
# noinspection PyPackages
from . import Event_Base


class PlayerSelect(Event_Base.EventBase):
    def __init__(self):
        super().__init__()
        self.ui_manager = gui.UIManager()
        self.ui_manager.purge_ui_elements()
        self.username = gui.UIInputBox(State.state.screen_center.x, State.state.screen_center.y + 100, 300, 50)
        self.username.text_adapter = LimitText()
        self.password = gui.UIInputBox(State.state.screen_center.x, State.state.screen_center.y + 50, 300, 50)
        self.password.text_adapter = LimitText()
        self.ui_manager.add_ui_element(self.username)
        self.ui_manager.add_ui_element(self.password)
        self.incorrect_password_end = 0
        self.button_manager.append('Guest', 'Login as Guest', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y + 150), Vector.Vector(250, 50), on_click=self.guest_button)
        self.button_manager.append('Enter', 'Enter', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y), Vector.Vector(250, 50), on_click=self.enter_button)
        self.button_manager.append('Quit', 'Quit', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y - 50), Vector.Vector(100, 50), on_click=self.exit_button)
        State.state.clear_current_floor_data()

    def enter_button(self):
        player_username = self.username.text.strip()
        player_password = self.password.text.strip()
        if not (player_username and player_password):
            return

        json_ = requests.get(f'http://localhost:666/save_data?name={quote(player_username)}&pw={quote(player_password)}').json()
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
            state_player.meta_data.is_player = True
            state_player.meta_data.is_guest = False
            state_player.meta_data.is_enemy = False
            from W_Main_File.Views import Exploration
            self.ui_manager.purge_ui_elements()
            Seeding.set_world_seed_from_player_name()
            State.state.grid.tiles.clear()
            if State.state.player.floor != 1:
                State.state.grid.remove(Vector.Vector(0, 0))
            elif not State.state.grid.get(0, 0):
                from W_Main_File.Tiles import Home_Tile
                State.state.grid.add(Home_Tile.HomeTile(Vector.Vector(0, 0)))
            Floor_Data_Saving.FloorSaveManager.load_floor(state_player.floor, force_load=True)
            State.state.window.show_view(Exploration.Explore())
        else:
            self.incorrect_password_end = time.time() + 1.5

    def exit_button(self):
        sys.exit()

    def guest_button(self):
        state = State.state.player
        State.state.grid.tiles.clear()
        if not State.state.grid.get(0, 0):
            from W_Main_File.Tiles import Home_Tile
            State.state.grid.add(Home_Tile.HomeTile(Vector.Vector(0, 0)))
        state.name = 'Guest'
        state.meta_data.is_player = False
        state.meta_data.is_guest = True
        state.meta_data.is_enemy = False
        state.pos = Vector.Vector(0, 0)
        state.max_hp = 220
        state.hp = 200
        state.gold = 0
        state.xp = 0
        state.lvl = 1
        state.floor = 1
        from W_Main_File.Views import Exploration
        self.ui_manager.purge_ui_elements()
        Seeding.set_world_seed_from_player_name()
        State.state.window.show_view(Exploration.Explore())

    def on_draw(self):
        super().on_draw()
        center_screen = Vector.Vector(self.window.width / 2, self.window.height / 2)
        arcade.draw_text('USERNAME:', center_screen.x - self.username.width + 45, self.username.center_y, arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20, anchor_x='center', anchor_y='center')
        arcade.draw_text('PASSWORD:', center_screen.x - self.password.width + 43, self.password.center_y, arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20, anchor_x='center', anchor_y='center')
        if self.incorrect_password_end > time.time():
            arcade.draw_text('Incorrect Password', State.state.screen_center.x, State.state.screen_center.y - 100, arcade.color.RED, font_name='arial', font_size=20, anchor_x='center', anchor_y='center')


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
