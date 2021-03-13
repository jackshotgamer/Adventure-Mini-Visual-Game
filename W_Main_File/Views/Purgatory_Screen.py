from W_Main_File.Views import Exploration
from W_Main_File.Views import Fading
from W_Main_File.Utilities import Vector
from W_Main_File.Essentials import State
from arcade import gui
import arcade
from W_Main_File.Utilities.Button_Functions import LogOutButton
from W_Main_File.Views import Log_Out


class MessageLabel(arcade.gui.UILabel):
    def __init__(self, message: str):
        super().__init__(message, State.state.screen_center.x, State.state.screen_center.y + 150, 250)
        if message == 'You Died':
            self.color = arcade.color.RED


class PlayButton(arcade.gui.UIFlatButton):
    def __init__(self, uimanager: arcade.gui.UIManager):
        super().__init__('Play Game', State.state.screen_center.x, State.state.screen_center.y + 75, 250, 50)
        self.ui_manager = uimanager

    def on_click(self):
        self.ui_manager.purge_ui_elements()
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


class SavingButton(arcade.gui.UIFlatButton):
    def __init__(self, uimanager: arcade.gui.UIManager, message):
        super().__init__('Save Character_Data_Files', State.state.screen_center.x, State.state.screen_center.y - 75, 200, 50)
        self.ui_manager = uimanager
        self.message = message

    def on_click(self):
        if State.state.preoccupied:
            return
        from W_Main_File.Views import Saving
        self.ui_manager.purge_ui_elements()
        State.state.window.show_view(Saving.Saving(lambda: PurgatoryScreen(self.message)))


class CannotBeUndoneLabel(arcade.gui.UILabel):
    def __init__(self):
        super().__init__('Warning: This cannot be undone!', State.state.screen_center.x, State.state.screen_center.y + 100, 800)


class ResetCharacterView(arcade.View):
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.ui_manager = gui.UIManager()
        self.ui_manager.purge_ui_elements()
        self.ui_manager.add_ui_element(CannotBeUndoneLabel())
        self.ui_manager.add_ui_element(Log_Out.ConfirmButton(self.ui_manager, self.on_confirm_func))
        self.ui_manager.add_ui_element(Log_Out.DenyButton(self.ui_manager, self.on_deny_func))

    def on_draw(self):
        arcade.start_render()

    def on_confirm_func(self):
        state = State.state.player
        State.state.texture_mapping = {}
        state.pos = Vector.Vector(0, 0)
        state.max_hp = 220
        state.hp = 200
        state.gold = 0
        state.xp = 0
        state.lvl = 1
        state.floor = 1
        State.state.window.show_view(PurgatoryScreen(self.message))

    def on_deny_func(self):
        State.state.window.show_view(PurgatoryScreen(self.message))


class PurgatoryScreen(arcade.View):
    def __init__(self, message):
        super().__init__()
        State.state.player.hp = State.state.player.max_hp
        self.ui_manager = gui.UIManager()
        self.ui_manager.purge_ui_elements()
        self.ui_manager.add_ui_element(PlayButton(self.ui_manager))
        self.ui_manager.add_ui_element(MessageLabel(message))
        self.ui_manager.add_ui_element(ResetCharacterButton(self.ui_manager, message))
        if not State.state.player.meta_data.is_guest:
            self.ui_manager.add_ui_element(SavingButton(self.ui_manager, message))
        self.ui_manager.add_ui_element(log_out_button := LogOutButton(self.ui_manager, show_confirm_screen=False))
        log_out_button.center_y = State.state.screen_center.y - 150
        log_out_button.center_x = State.state.screen_center.x

    def on_draw(self):
        arcade.start_render()
