import arcade
from arcade.gui import UIFlatButton, UIManager, UILabel

from W_Main_File.Essentials import State


class LogOutView(arcade.View):
    def __init__(self, on_deny_func, on_confirm_func, show_confirmation_screen: bool = True, show_warning_with_guest_and_player: bool = True):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.purge_ui_elements()
        self.on_confirm_func = on_confirm_func
        self.show_confirmation_screen = show_confirmation_screen
        if self.show_confirmation_screen:
            self.ui_manager.add_ui_element(ConfirmButton(self.ui_manager, on_confirm_func))
            self.ui_manager.add_ui_element(DenyButton(self.ui_manager, on_deny_func))
            if show_warning_with_guest_and_player:
                self.ui_manager.add_ui_element(WarningText())

    def update(self, delta_time: float):
        if not self.show_confirmation_screen:
            State.state.texture_mapping = {}
            self.ui_manager.purge_ui_elements()
            self.on_confirm_func()

    def on_draw(self):
        arcade.start_render()


class ConfirmButton(UIFlatButton):
    def __init__(self, uimanager: UIManager, on_confirm_func):
        super().__init__('Confirm?', State.state.screen_center.x - 100, State.state.screen_center.y, 200, 50)
        self.ui_manager = uimanager
        self.on_confirm_func = on_confirm_func

    def on_click(self):
        self.ui_manager.purge_ui_elements()
        self.on_confirm_func()


class DenyButton(UIFlatButton):
    def __init__(self, uimanager: UIManager, on_deny_func):
        super().__init__('Deny?', State.state.screen_center.x + 100, State.state.screen_center.y, 200, 50)
        self.ui_manager = uimanager
        self.on_deny_func = on_deny_func

    def on_click(self):
        self.ui_manager.purge_ui_elements()
        State.state.load_textures()
        self.on_deny_func()


class WarningText(UILabel):
    def __init__(self):
        super().__init__(('Warning:\n' 'This will NOT save your data. This cannot be undone!' if not State.state.player.meta_data.is_guest
                          else 'You will lose your progress. This cannot be undone!'), State.state.screen_center.x, State.state.screen_center.y + 100, 800)
