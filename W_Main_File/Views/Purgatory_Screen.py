from functools import partial

from arcade.gui import UIManager

from W_Main_File.Views import Exploration, Event_Base, Log_Out
from W_Main_File.Views import Fading
from W_Main_File.Utilities import Vector, Seeding, Action_Queue
from W_Main_File.Essentials import State
from arcade import gui
import arcade


def play_button(ui_manager: UIManager):
    State.state.clear_current_floor_data()
    ui_manager.purge_ui_elements()
    State.state.player.hp = State.state.player.max_hp
    explore = Exploration.Explore()
    State.state.window.show_view(Fading.Fading(lambda: explore, 10, 4, should_reverse=True, only_reverse=True, reset_pos=Vector.Vector(0, 0), reset_floor=1, render=lambda _: explore.on_draw()))


def reset_character_button(ui_manager: UIManager, message):
    ui_manager.purge_ui_elements()
    Action_Queue.action_queue.append(
        lambda: State.state.window.show_view(
            ResetCharacterView(
                message)))


def saving_button(ui_manager: UIManager, message):
    if State.state.preoccupied:
        return
    from W_Main_File.Views import Saving
    ui_manager.purge_ui_elements()
    Action_Queue.action_queue.append(
        lambda: State.state.window.show_view(
            Saving.Saving(
                lambda: PurgatoryScreen(
                    message))))


def confirm_func(message):
    state = State.state.player
    State.state.clear_current_floor_data()
    import shutil
    shutil.rmtree(f'PLAYERDATA/{State.state.player.name}')
    state.pos = Vector.Vector(0, 0)
    state.max_hp = 1000
    state.hp = 1000
    state.gold = 0
    state.xp = 0
    state.lvl = 1
    state.floor = 1
    Action_Queue.action_queue.append(
        lambda: State.state.window.show_view(
            PurgatoryScreen(
                message)))


def deny_func(message):
    Action_Queue.action_queue.append(
        lambda: State.state.window.show_view(
            PurgatoryScreen(
                message)))


class ResetCharacterView(Event_Base.EventBase):
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.ui_manager = gui.UIManager()
        self.ui_manager.purge_ui_elements()
        self.button_manager.append('Confirm2', 'Confirm?', Vector.Vector(State.state.screen_center.x - 100, State.state.screen_center.y), Vector.Vector(199, 50),
                                   on_click=partial(confirm_func, message))
        self.button_manager.append('Deny2', 'Deny?', Vector.Vector(State.state.screen_center.x + 100, State.state.screen_center.y), Vector.Vector(199, 50),
                                   on_click=partial(deny_func, message))

    def on_draw(self):
        super().on_draw()
        arcade.draw_text('Warning: This cannot be undone!', State.state.screen_center.x, State.state.screen_center.y + 100, arcade.color.WHITE,
                         23, 800, anchor_x='center', anchor_y='center', align='center')

    def update(self, delta_time: float):
        if Action_Queue.action_queue:
            action = Action_Queue.action_queue.popleft()
            action()


class PurgatoryScreen(Event_Base.EventBase):
    def __init__(self, message, increment_death=False):
        super().__init__()
        arcade.set_background_color((0, 0, 0))
        State.state.player.hp = State.state.player.max_hp
        self.message = message
        self.ui_manager = gui.UIManager()
        self.current_window_size = Vector.Vector(State.state.window.width, State.state.window.height)
        self.buttons()
        if increment_death:
            print('hi')
            State.state.player.deaths += 1
            from W_Main_File.Utilities import Seeding
            Seeding.set_world_seed_from_player_name()
            State.state.clear_current_floor_data(should_clear_grid=False)

    def on_draw(self):
        super().on_draw()
        arcade.draw_text(self.message, State.state.screen_center.x, State.state.screen_center.y + 150,
                         (arcade.color.RED if self.message == 'You Died' else arcade.color.RED), 23, 1000, align='center', anchor_y='center', anchor_x='center')
        State.state.render_mouse()

    def update(self, delta_time: float):
        if Action_Queue.action_queue:
            action = Action_Queue.action_queue.popleft()
            action()
        self.check_if_resized()

    def buttons(self):
        self.ui_manager.purge_ui_elements()
        self.button_manager.append('Play', 'Play game', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y + 75), Vector.Vector(250, 50),
                                   on_click=partial(play_button, self.ui_manager))
        self.button_manager.append('Log Out', 'Log Out', (Vector.Vector(State.state.screen_center.x, State.state.screen_center.y - 150) if State.state.player.meta_data.is_player
                                                          else Vector.Vector(State.state.screen_center.x, State.state.screen_center.y)),
                                   Vector.Vector(200, 50), on_click=lambda: log_out_buttons(True, self.message, self.ui_manager))
        if not State.state.player.meta_data.is_guest:
            self.button_manager.append('Save', 'Save Character', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y - 75), Vector.Vector(200, 50),
                                       on_click=partial(saving_button, self.ui_manager, self.message))
            self.button_manager.append('Reset Character', 'Reset all Stats', Vector.Vector(State.state.screen_center.x, State.state.screen_center.y), Vector.Vector(250, 50),
                                       on_click=partial(reset_character_button, self.ui_manager, self.message))

    def check_if_resized(self):
        if self.current_window_size.x == State.state.window.width and self.current_window_size.y == State.state.window.height:
            return
        else:
            self.buttons()
            self.current_window_size = Vector.Vector(State.state.window.width, State.state.window.height)


def log_out_buttons(show_confirm_screen, message, ui_manager):
    State.state.window.show_view(Log_Out.LogOutView(on_deny_func=lambda: deny_fun(ui_manager, message), on_confirm_func=lambda: confirm_fun(ui_manager), show_confirmation_screen=show_confirm_screen))


def confirm_fun(ui_manager: UIManager):
    # noinspection PyPackages
    from ..Views import Player_Select
    ui_manager.purge_ui_elements()
    from W_Main_File.Essentials.State import state
    state.texture_mapping.clear()
    Action_Queue.action_queue.append(
        lambda: State.state.window.show_view(Player_Select.PlayerSelect()))


def deny_fun(ui_manager: UIManager, message):
    # noinspection PyPackages
    ui_manager.purge_ui_elements()
    Action_Queue.action_queue.append(
        lambda: State.state.window.show_view(
            PurgatoryScreen(
                message)))
