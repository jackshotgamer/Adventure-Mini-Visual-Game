import arcade
from arcade.gui import UIFlatButton, UIManager, UILabel

import Exploration
import Player_Select
import State


class LogOutView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.purge_ui_elements()
        self.ui_manager.add_ui_element(ConfirmButton(self.ui_manager))
        self.ui_manager.add_ui_element(DenyButton(self.ui_manager))
        self.ui_manager.add_ui_element(WarningText())

    def on_draw(self):
        arcade.start_render()


class ConfirmButton(UIFlatButton):
    def __init__(self, uimanager: UIManager):
        super().__init__('Confirm?', State.state.screen_center.x - 100, State.state.screen_center.y, 200, 50)
        self.ui_manager = uimanager

    def on_click(self):
        self.ui_manager.purge_ui_elements()
        State.state.texture_mapping = {}
        State.state.window.show_view(Player_Select.PlayerSelect())


class DenyButton(UIFlatButton):
    def __init__(self, uimanager: UIManager):
        super().__init__('Deny?', State.state.screen_center.x + 100, State.state.screen_center.y, 200, 50)
        self.ui_manager = uimanager

    def on_click(self):
        self.ui_manager.purge_ui_elements()
        State.state.load_textures()
        State.state.window.show_view(Exploration.Explore())


class WarningText(UILabel):
    def __init__(self):
        super().__init__(('Warning:\n' 'This will NOT save your data. This cannot be undone!' if not State.state.player.meta_data.is_guest
                          else 'You will lose your progress. This cannot be undone!'), State.state.screen_center.x, State.state.screen_center.y + 100, 800)