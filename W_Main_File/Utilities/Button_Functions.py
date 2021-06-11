from functools import partial

import arcade
# noinspection PyUnresolvedReferences
from arcade.gui import UIFlatButton, UIManager

from W_Main_File.Utilities import Action_Queue, Floor_Data_Saving
from W_Main_File.Essentials import State
from W_Main_File.Utilities import Vector, Seeding
from W_Main_File.Views import Player_Select, Exploration, Fading, Log_Out, Event_Base


def register_custom_exploration_buttons(button_manager, ui_manager):
    button_manager.append('Home', 'Go Home', Vector.Vector(State.state.screen_center.x + 250 + State.state.cell_size.x, (State.state.screen_center.y + 50) + (State.state.cell_size.y - 24)),
                          Vector.Vector(200, 50), on_click=go_home_button)
    button_manager.append('Log Out', 'Log Out',
                          Vector.Vector(State.state.screen_center.x + 250 + State.state.cell_size.x, (State.state.screen_center.y + 150) + (State.state.cell_size.y - 24)),
                          Vector.Vector(200, 50), on_click=lambda: log_out_button(True, ui_manager))
    if not State.state.player.meta_data.is_guest:
        button_manager.append('Save Data', 'Save Data',
                              Vector.Vector(State.state.screen_center.x + 250 + State.state.cell_size.x, (State.state.screen_center.y - 50) + (State.state.cell_size.y - 24)),
                              Vector.Vector(200, 50), on_click=save_button)


def invalidate_floor_data():
    State.state.clear_current_floor_data()


def go_home_button():
    if State.state.preoccupied:
        return
    Floor_Data_Saving.FloorSaveManager.floor_save()
    explore = Exploration.Explore()
    Action_Queue.action_queue.append(
        lambda: State.state.window.show_view(
            Fading.Fading(Exploration.Explore,
                          4,
                          5,
                          should_reverse=True,
                          should_freeze=True,
                          only_reverse=False,
                          reset_pos=Vector.Vector(0, 0),
                          halfway_func=lambda: invalidate_floor_data(),
                          reset_floor=1,
                          render=lambda _: explore.on_draw())))


def log_out_button(show_confirm_screen, ui_manager):
    if State.state.preoccupied:
        return
    Action_Queue.action_queue.append(
        lambda: State.state.window.show_view(
            Log_Out.LogOutView(
                on_deny_func=lambda: deny_funct(ui_manager),
                on_confirm_func=lambda: confirm_funct(ui_manager),
                show_confirmation_screen=show_confirm_screen)))


def save_button():
    if State.state.preoccupied:
        return
    from W_Main_File.Views import Saving
    Action_Queue.action_queue.append(
        lambda: State.state.window.show_view(
            Saving.Saving(
                Exploration.Explore)))


def confirm_funct(ui_manager: UIManager):
    # noinspection PyPackages
    from ..Views import Player_Select
    ui_manager.purge_ui_elements()
    from W_Main_File.Essentials.State import state
    state.clear_current_floor_data()
    Action_Queue.action_queue.append(lambda: State.state.window.show_view(Player_Select.PlayerSelect()))


def deny_funct(ui_manager: UIManager):
    # noinspection PyPackages
    from ..Views import Exploration
    ui_manager.purge_ui_elements()
    Action_Queue.action_queue.append(lambda: State.state.window.show_view(Exploration.Explore()))
