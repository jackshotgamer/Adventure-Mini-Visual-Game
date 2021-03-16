from functools import partial

from arcade.gui import UIManager

from W_Main_File.Views import Exploration, Event_Base, Log_Out
from W_Main_File.Views import Fading
from W_Main_File.Utilities import Vector
from W_Main_File.Essentials import State
from arcade import gui
import arcade


class PlayButton(arcade.gui.UIFlatButton):
    def __init__(self, uimanager: arcade.gui.UIManager):
        super().__init__('Play Game', State.state.screen_center.x, State.state.screen_center.y + 75, 250, 50)
        self.ui_manager = uimanager

    def on_click(self):
        self.ui_manager.purge_ui_elements()
        State.state.player.hp = State.state.player.max_hp
        State.state.window.show_view(Fading.Fading(Exploration.Explore, 7, 4, should_reverse=True, only_reverse=True, should_reload_textures=True, reset_pos=Vector.Vector(0, 0)))


def play_button(ui_manager: UIManager):
    ui_manager.purge_ui_elements()
    State.state.player.hp = State.state.player.max_hp
    State.state.window.show_view(Fading.Fading(Exploration.Explore, 7, 4, should_reverse=True, only_reverse=True, should_reload_textures=True, reset_pos=Vector.Vector(0, 0)))


class ResetCharacterButton(arcade.gui.UIFlatButton):
    def __init__(self, uimanager: arcade.gui.UIManager, message):
        super().__init__('Reset all Stats', State.state.screen_center.x, State.state.screen_center.y, 250, 50)
        self.ui_manager = uimanager
        self.message = message

    def on_click(self):
        self.ui_manager.purge_ui_elements()
        State.state.window.show_view(ResetCharacterView(self.message))


def reset_character_button(ui_manager: UIManager, message):
    ui_manager.purge_ui_elements()
    State.state.window.show_view(ResetCharacterView(message))


class SavingButton(arcade.gui.UIFlatButton):
    def __init__(self, uimanager: arcade.gui.UIManager, message):
        super().__init__('Save Character', State.state.screen_center.x, State.state.screen_center.y - 75, 200, 50)
        self.ui_manager = uimanager
        self.message = message

    def on_click(self):
        if State.state.preoccupied:
            return
        from W_Main_File.Views import Saving
        self.ui_manager.purge_ui_elements()
        State.state.window.show_view(Saving.Saving(lambda: PurgatoryScreen(self.message)))


def saving_button(ui_manager: UIManager, message):
    if State.state.preoccupied:
        return
    from W_Main_File.Views import Saving
    ui_manager.purge_ui_elements()
    State.state.window.show_view(Saving.Saving(lambda: PurgatoryScreen(message)))


def confirm_func(message):
    state = State.state.player
    State.state.texture_mapping = {}
    state.pos = Vector.Vector(0, 0)
    state.max_hp = 220
    state.hp = 200
    state.gold = 0
    state.xp = 0
    state.lvl = 1
    state.floor = 1
    State.state.window.show_view(PurgatoryScreen(message))


def deny_func(message):
    State.state.window.show_view(PurgatoryScreen(message))


class ResetCharacterView(Event_Base.EventBase):
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.ui_manager = gui.UIManager()
        self.ui_manager.purge_ui_elements()
        self.button_manager.append('Confirm2', 'Confirm?', Vector.Vector(State.state.screen_center.x - 100, State.state.screen_center.y), Vector.Vector(200, 50),
                                   on_click=partial(confirm_func, message))
        self.button_manager.append('Deny2', 'Deny?', Vector.Vector(State.state.screen_center.x + 100, State.state.screen_center.y), Vector.Vector(200, 50),
                                   on_click=partial(deny_func, message))

    def on_draw(self):
        super().on_draw()
        arcade.draw_text('Warning: This cannot be undone!', State.state.screen_center.x, State.state.screen_center.y + 100, arcade.color.WHITE,
                         23, 800, anchor_x='center', anchor_y='center', align='center')


class PurgatoryScreen(Event_Base.EventBase):
    def __init__(self, message):
        super().__init__()
        State.state.player.hp = State.state.player.max_hp
        self.message = message
        self.ui_manager = gui.UIManager()
        self.ui_manager.purge_ui_elements()
        self.button_manager.append('Play', 'Play game', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y + 75), Vector.Vector(250, 50),
                                   on_click=partial(play_button, self.ui_manager))
        self.button_manager.append('Log Out', 'Log Out', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y - 150),
                                   Vector.Vector(200, 50), on_click=lambda: log_out_buttons(True, message, self.ui_manager))
        if not State.state.player.meta_data.is_guest:
            self.button_manager.append('Save', 'Save Character', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y - 75), Vector.Vector(200, 50),
                                       on_click=partial(saving_button, self.ui_manager, message))
            self.button_manager.append('Reset Character', 'Reset all Stats', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y), Vector.Vector(250, 50),
                                       on_click=partial(reset_character_button, self.ui_manager, message))

    def on_draw(self):
        super().on_draw()
        arcade.draw_text(self.message, State.state.screen_center.x, State.state.screen_center.y + 150,
                         (arcade.color.RED if self.message == 'You Died' else arcade.color.WHITE), 23, 250, align='center', anchor_y='center', anchor_x='center')


def log_out_buttons(show_confirm_screen, message, ui_manager):
    State.state.window.show_view(Log_Out.LogOutView(on_deny_func=lambda: deny_fun(ui_manager, message), on_confirm_func=lambda: confirm_fun(ui_manager), show_confirmation_screen=show_confirm_screen))


def confirm_fun(ui_manager: UIManager):
    # noinspection PyPackages
    from ..Views import Player_Select
    ui_manager.purge_ui_elements()
    State.state.window.show_view(Player_Select.PlayerSelect())


def deny_fun(ui_manager: UIManager, message):
    # noinspection PyPackages
    ui_manager.purge_ui_elements()
    State.state.load_textures()
    State.state.window.show_view(PurgatoryScreen(message))
