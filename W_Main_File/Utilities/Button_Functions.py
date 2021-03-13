from arcade.gui import UIFlatButton, UIManager

from W_Main_File.Essentials import State
from W_Main_File.Utilities import Vector
from W_Main_File.Views import Player_Select, Exploration, Fading, Log_Out


def register_ui_buttons(uimanager: UIManager):
    if State.state.preoccupied:
        return
    uimanager.add_ui_element(GoHomeButton(uimanager))
    uimanager.add_ui_element(LogOutButton(uimanager))
    if not State.state.player.meta_data.is_guest:
        uimanager.add_ui_element(SaveButton(uimanager))


def reposition_button(uimanager: UIManager):
    if State.state.preoccupied:
        return
    # noinspection PyProtectedMember
    for element in uimanager._ui_elements:
        if isinstance(element, LogOutButton):
            element.center_y, element.center_x = (State.state.screen_center.y + 150) + (State.state.cell_size.y - 24), State.state.screen_center.x + 250 + State.state.cell_size.x
        elif isinstance(element, GoHomeButton):
            element.center_y, element.center_x = (State.state.screen_center.y + 50) + (State.state.cell_size.y - 24), State.state.screen_center.x + 250 + State.state.cell_size.x
        elif isinstance(element, SaveButton):
            element.center_y, element.center_x = (State.state.screen_center.y - 50) + (State.state.cell_size.y - 24), State.state.screen_center.x + 250 + State.state.cell_size.x


class LogOutButton(UIFlatButton):
    def __init__(self, uimanager: UIManager, show_confirm_screen: bool = True):
        super().__init__('Log Out', (State.state.screen_center.y + 150) + (State.state.cell_size.y - 24), State.state.screen_center.x + 250 + State.state.cell_size.x, 200, 50)
        self.ui_manager = uimanager
        self.show_confirm_screen = show_confirm_screen

    def on_click(self):
        self.ui_manager.purge_ui_elements()
        # State.state.texture_mapping = {}
        # State.state.window.show_view(Player_Select.PlayerSelect())
        State.state.window.show_view(Log_Out.LogOutView(on_deny_func=self.deny_fun, on_confirm_func=self.confirm_func, show_confirmation_screen=self.show_confirm_screen))

    def deny_fun(self):
        State.state.window.show_view(Exploration.Explore())

    def confirm_func(self):
        State.state.texture_mapping = {}
        State.state.window.show_view(Player_Select.PlayerSelect())


class GoHomeButton(UIFlatButton):
    def __init__(self, uimanager: UIManager):
        super().__init__('Go Home', State.state.screen_center.y + 50 + (State.state.cell_size.y - 24), State.state.screen_center.x + 250 + State.state.cell_size.x, 200, 50)
        self.ui_manager = uimanager

    def on_click(self):
        if State.state.preoccupied:
            return
        self.ui_manager.purge_ui_elements()
        State.state.window.show_view(Fading.Fading(Exploration.Explore, 4, 5, should_reverse=True, should_freeze=True, should_reload_textures=True, only_reverse=False, reset_pos=Vector.Vector(0, 0)))


class SaveButton(UIFlatButton):
    def __init__(self, uimanager: UIManager):
        super().__init__('Save Character_Data_Files', State.state.screen_center.y + (State.state.cell_size.y - 24), State.state.screen_center.x + 250 + State.state.cell_size.x, 200, 50)
        self.ui_manager = uimanager

    def on_click(self):
        if State.state.preoccupied:
            return
        from W_Main_File.Views import Saving
        self.ui_manager.purge_ui_elements()
        State.state.window.show_view(Saving.Saving(Exploration.Explore))
