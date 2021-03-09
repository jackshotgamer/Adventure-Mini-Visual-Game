from typing import Tuple
import collections
import Exploration
import Fading
import Vector
import State
import Tile
from arcade import gui
import arcade
import Sprites_
import random
import Grid


class MessageLabel(arcade.gui.UILabel):
    def __init__(self, message: str):
        super().__init__(message, State.state.screen_center.x, State.state.screen_center.y + 150, 250, 50)


class PlayButton(arcade.gui.UIFlatButton):
    def __init__(self, uimanager: arcade.gui.UIManager):
        super().__init__('Play Game', State.state.screen_center.x, State.state.screen_center.y + 150, 250, 50)
        self.ui_manager = uimanager

    def on_click(self):
        self.ui_manager.purge_ui_elements()
        State.state.window.show_view(Fading.Fading(Exploration.Explore, 7, 4, should_reverse=True, only_reverse=True, should_reload_textures=True, reset_pos=Vector.Vector(0, 0)))


class PurgatoryScreen(arcade.View):
    def __init__(self, message):
        super().__init__()
        self.ui_manager = gui.UIManager()
        self.ui_manager.purge_ui_elements()
        self.ui_manager.add_ui_element(PlayButton(self.ui_manager))
        self.ui_manager.add_ui_element(MessageLabel(message))
