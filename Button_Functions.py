import arcade
from arcade.gui import UIFlatButton, UIManager
import State
import Player_Select
import Exploration
import Vector
import time


def register_ui_buttons(uimanager: UIManager):
    uimanager.add_ui_element(LogOutButton(uimanager))
    uimanager.add_ui_element(GoHomeButton(uimanager))


def reposition_button(uimanager: UIManager):
    for element in uimanager._ui_elements:
        if isinstance(element, LogOutButton):
            element.center_y, element.center_x = (State.state.screen_center.y + 150) + (State.state.cell_size.y - 24), State.state.screen_center.x + 250 + State.state.cell_size.x
        elif isinstance(element, GoHomeButton):
            element.center_y, element.center_x = (State.state.screen_center.y + 50) + (State.state.cell_size.y - 24), State.state.screen_center.x + 250 + State.state.cell_size.x


class LogOutButton(UIFlatButton):
    def __init__(self, uimanager: UIManager):
        super().__init__('Log Out', 0, 0, 200, 50)
        self.ui_manager = uimanager

    def on_click(self):
        self.ui_manager.purge_ui_elements()
        State.state.window.show_view(Player_Select.PlayerSelect())


class GoHomeButton(UIFlatButton):
    def __init__(self, uimanager: UIManager):
        super().__init__('Go Home', 0, 0, 200, 50)
        self.ui_manager = uimanager

    def on_click(self):
        import Fading
        State.state.window.show_view(Fading.Fading())
        State.state.player.pos = Vector.Vector(0, 0)
