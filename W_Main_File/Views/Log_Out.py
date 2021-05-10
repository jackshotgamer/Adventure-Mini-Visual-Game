import arcade
from arcade.gui import UIFlatButton, UIManager, UILabel

from W_Main_File.Utilities import Action_Queue
from W_Main_File.Essentials import State
from W_Main_File.Utilities import Vector
from functools import partial
# noinspection PyPackages
from ..Views import Event_Base


class LogOutView(Event_Base.EventBase):
    def __init__(self, on_deny_func, on_confirm_func, show_confirmation_screen: bool = True, show_warning_with_guest_and_player: bool = True):
        super().__init__()
        self.ui_manager = UIManager()
        self.ui_manager.purge_ui_elements()
        self.on_confirm_func = on_confirm_func
        self.on_deny_func = on_deny_func
        self.show_confirmation_screen = show_confirmation_screen
        self.show_warning_with_guest_and_player = show_warning_with_guest_and_player
        if self.show_confirmation_screen:
            self.button_manager.append('Confirm1', 'Confirm?', Vector.Vector(State.state.screen_center.x - 100, State.state.screen_center.y), Vector.Vector(200, 50),
                                       on_click=on_confirm_func)
            self.button_manager.append('Deny1', 'Deny?', Vector.Vector(State.state.screen_center.x + 100, State.state.screen_center.y), Vector.Vector(200, 50),
                                       on_click=self.on_deny_func)

    def update(self, delta_time: float):
        if not self.show_confirmation_screen:
            State.state.texture_mapping = {}
            self.ui_manager.purge_ui_elements()
            self.on_confirm_func()
        if Action_Queue.action_queue:
            action = Action_Queue.action_queue.popleft()
            action()

    def on_draw(self):
        super().on_draw()
        if self.show_warning_with_guest_and_player:
            arcade.draw_text(('Warning:\n' 'This will NOT save your data. This cannot be undone!' if not State.state.player.meta_data.is_guest
                              else 'You will lose your progress. This cannot be undone!'), State.state.screen_center.x, State.state.screen_center.y + 100, arcade.color.WHITE,
                             23, 800, anchor_x='center', anchor_y='center', align='center')


# def confirm_function(ui_manager: UIManager):
#     # noinspection PyPackages
#     from . import
#     ui_manager.purge_ui_elements()
#     State.state.window.show_view()
#
#
# def deny_function(ui_manager: UIManager):
#     # noinspection PyPackages
#     from . import
#     ui_manager.purge_ui_elements()
#     State.state.load_textures()
#     State.state.window.show_view()
