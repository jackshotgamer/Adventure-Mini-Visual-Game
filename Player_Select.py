import arcade
from arcade import gui
from urllib.parse import quote
import State
import Vector
import requests
import time


class PlayButton(gui.UIFlatButton):
    def __init__(self, ui_manager, player_select):
        super().__init__('Enter', State.state.screen_center.x, State.state.screen_center.y, 250, 50)
        self.ui_manager = ui_manager
        self.player_select = player_select

    def on_click(self):
        player_username = self.player_select.username.text
        player_password = self.player_select.password.text
        if not (player_username and player_password):
            return
        json_ = requests.get(f'http://localhost:666/save_data?name={quote(player_username)}&pw={quote(player_password)}').json()
        print(json_)
        if not json_['error']:
            state_player = State.state.player
            state_player.name = json_['player_name']
            state_player.hp = json_['hp']
            state_player.max_hp = json_['max_hp']
            state_player.pos = Vector.Vector(json_['x'], json_['y'])
            state_player.gold = json_['gold']
            state_player.xp = json_['xp']
            state_player.lvl = json_['lvl']
            state_player.floor = json_['floor']
            state_player.meta_data.isplayer = True
            print(state_player.__dict__)
            import Exploration
            self.ui_manager.purge_ui_elements()
            State.state.window.show_view(Exploration.Explore())
        else:
            self.player_select.incorrect_password_end = time.time() + 1.5


class PlayerSelect(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = gui.UIManager()
        self.ui_manager.purge_ui_elements()
        self.ui_manager.add_ui_element(PlayButton(self.ui_manager, self))
        self.username = gui.UIInputBox(State.state.screen_center.x, State.state.screen_center.y + 100, 300, 50)
        self.username.text_adapter = LimitText()
        self.password = gui.UIInputBox(State.state.screen_center.x, State.state.screen_center.y + 50, 300, 50)
        self.password.text_adapter = LimitText()
        self.ui_manager.add_ui_element(self.username)
        self.ui_manager.add_ui_element(self.password)
        self.incorrect_password_end = 0

    def on_draw(self):
        arcade.start_render()
        center_screen = Vector.Vector(self.window.width / 2, self.window.height / 2)
        arcade.draw_text('USERNAME:', center_screen.x - self.username.width + 45, self.username.center_y, arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20, anchor_x='center', anchor_y='center')
        arcade.draw_text('PASSWORD:', center_screen.x - self.password.width + 43, self.password.center_y, arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=20, anchor_x='center', anchor_y='center')
        if self.incorrect_password_end > time.time():
            arcade.draw_text('Incorrect Password', State.state.screen_center.x, State.state.screen_center.y - 50, arcade.color.RED, font_name='arial', font_size=20, anchor_x='center', anchor_y='center')


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
