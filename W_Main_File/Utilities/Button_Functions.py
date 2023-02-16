import typing
# noinspection PyUnresolvedReferences
from arcade.gui import UIFlatButton, UIManager

from W_Main_File.Utilities import Action_Queue, Data_Saving, Inventory_GUI
from W_Main_File.Essentials import State
from W_Main_File.Utilities import Vector
from W_Main_File.Views import Exploration, Fading, Log_Out

if typing.TYPE_CHECKING:
    from W_Main_File.Essentials import Button_Sprite_Manager


def register_custom_exploration_buttons(button_manager: 'Button_Sprite_Manager.ButtonManager', ui_manager, inv_button_works=True):
    button_manager.clear_all(True)
    button_manager.append('Log Out', 'Log Out',
                          Vector.Vector((State.state.window.width * 0.875),
                                        (State.state.screen_center.y + (State.state.window.height * 0.1875)) + (State.state.cell_render_size.y - (State.state.window.height * 0.03))),
                          Vector.Vector((State.state.window.width * 0.2), (State.state.window.height * 0.0625)), on_click=lambda: log_out_button(True, ui_manager))
    button_manager.append('Home', 'Go Home',
                          Vector.Vector((State.state.window.width * 0.875),
                                        (State.state.screen_center.y + (State.state.window.height * 0.0625))
                                        + (State.state.cell_render_size.y - (State.state.window.height * 0.03))),
                          Vector.Vector((State.state.window.width * 0.2), (State.state.window.height * 0.0625)), on_click=go_home_button)
    button_manager.append('Inventory', 'Open Inventory',
                          Vector.Vector((State.state.window.width * 0.875),
                                        (State.state.screen_center.y - (State.state.window.height * 0.0625)) + (State.state.cell_render_size.y - (State.state.window.height * 0.03))),
                          Vector.Vector((State.state.window.width * 0.2), (State.state.window.height * 0.0625)), on_click=(lambda: toggle_inv(button_manager)) if inv_button_works else None)
    if not State.state.player.meta_data.is_guest:
        button_manager.append('Save Data', 'Save Data',
                              Vector.Vector((State.state.window.width * 0.875),
                                            (State.state.screen_center.y - (State.state.window.height * 0.1875)) + (State.state.cell_render_size.y - (State.state.window.height * 0.03))),
                              Vector.Vector((State.state.window.width * 0.2), (State.state.window.height * 0.0625)), on_click=save_button)


def invalidate_floor_data():
    State.state.clear_current_floor_data()


def go_home_button():
    if State.state.preoccupied:
        return
    Data_Saving.SaveManager.floor_save()
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
    from W_Main_File.Utilities import Inventory_GUI
    if State.state.preoccupied and not Inventory_GUI.is_inv():
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


def toggle_inv(button_manager: 'Button_Sprite_Manager.ButtonManager'):
    if Inventory_GUI.is_inv():
        Inventory_GUI.hide_inv(button_manager)
    else:
        if State.state.preoccupied:
            return
        Inventory_GUI.show_inv(button_manager)


def confirm_funct(ui_manager: UIManager):
    # noinspection PyPackages
    from ..Views import Player_Select
    ui_manager.purge_ui_elements()
    from W_Main_File.Essentials.State import state
    state.clear_current_floor_data()
    State.state.player.inventory.items.clear()
    Action_Queue.action_queue.append(lambda: State.state.window.show_view(Player_Select.PlayerSelect()))


def deny_funct(ui_manager: UIManager):
    # noinspection PyPackages
    from ..Views import Exploration
    ui_manager.purge_ui_elements()
    Action_Queue.action_queue.append(lambda: State.state.window.show_view(Exploration.Explore()))
