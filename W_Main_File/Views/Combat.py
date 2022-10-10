import arcade
import arcade.gui
from arcade import key

from W_Main_File.Utilities import Button_Functions, Action_Queue
from W_Main_File.Views import Purgatory_Screen, Event_Base
from W_Main_File.Data import Sprites_, HpEntity, Enemy_Data
from W_Main_File.Essentials import State
import time
import random
from W_Main_File.Tiles import Loot_Functions, Trapdoor_Functions, Trap_Functions
from W_Main_File.Utilities.Vector import Vector


class Combat(Event_Base.EventBase):
    sprite = {
        'Witch': Sprites_.swamp_monster,
        'Dragon': Sprites_.swamp_monster,
        'Ogre': Sprites_.swamp_monster,
    }

    def __init__(self):
        super().__init__()

        self.colour = State.state.player.hp / State.state.player.max_hp
        self.colour2 = State.state.player.hp / State.state.player.max_hp
        self.truthy = False
        self.truthy2 = False
        self.key_ = False
        self.symbol2 = arcade.key.D
        self.current_window_size = Vector(State.state.window.width, State.state.window.height)
        from W_Main_File.Views import Exploration
        self.explore = Exploration.Explore()
        self.buttons()

    def on_draw(self):
        arcade.set_background_color((18, 18, 18))
        arcade.start_render()
        cell_render_size = (State.state.cell_size * ((State.state.window.width / State.state.default_window_size.xf), (State.state.window.height / State.state.default_window_size.y)))

        self.button_manager.render()
        State.state.render_mouse()

    @staticmethod
    def change_background_colour():
        arcade.set_background_color((0, 0, 0))

    def check_if_resized(self):
        if self.current_window_size.x == State.state.window.width and self.current_window_size.y == State.state.window.height:
            return
        else:
            self.buttons()
            self.current_window_size = Vector(State.state.window.width, State.state.window.height)

    def buttons(self):
        self.button_manager.append('flee', 'Flee', State.state.screen_center, Vector(150, 60), on_click=self.flee, text_colour=(200, 100, 100))

    def update(self, delta_time: float):
        self.check_if_resized()
        self.colour = State.state.player.hp / State.state.player.max_hp
        # self.colour2 = self.combatant.hp / self.combatant.max_hp
        if State.state.player.hp <= 0:
            from W_Main_File.Views import Purgatory_Screen, Fading
            State.state.window.show_view(Fading.Fading((lambda: Purgatory_Screen.PurgatoryScreen(f'You were killed by an enemy!', increment_death=True)), 7, 4, should_reverse=False,
                                                       should_freeze=True, reset_pos=Vector(0, 0), halfway_func=self.change_background_colour, render=lambda _: self.fading_render(_)))
            State.state.clear_current_floor_data()
            return
        # if self.combatant.hp <= 0:
        #     from W_Main_File.Views import Fading
        #     State.state.window.show_view(Fading.Fading(lambda: self.explore, 7, 4, should_reverse=True,
        #                                                should_freeze=True, halfway_func=self.change_background_colour, render=lambda _: self.fading_render(_)))
        #     return
        if self.truthy:
            State.state.player.hp -= 2
        if self.symbol2 == arcade.key.D:
            self.key_ = False
        elif self.symbol2 == arcade.key.A:
            self.key_ = True

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        print(f'*{x}*, *{y}*')

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.H:
            self.truthy = True
        if symbol == arcade.key.J:
            self.truthy2 = True
        self.symbol2 = symbol

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.H:
            self.truthy = False
        if _symbol == arcade.key.J:
            self.truthy2 = False

    def fading_render(self, state_):
        if state_ == 'fading' or not state_:
            self.on_draw()
        elif state_ == 'reversing':
            self.explore.on_draw()
        arcade.set_background_color((0, 0, 0))

    def flee(self):
        from W_Main_File.Views import Fading
        if State.state.player.hp <= State.state.player.max_hp * 0.25:
            State.state.player.hp = 1
        else:
            State.state.player.hp -= int(State.state.player.max_hp * 0.25)
        self.change_background_colour()
        State.state.window.show_view(Fading.Fading(lambda: self.explore, 1, 1, should_reverse=True,
                                                   should_freeze=True, halfway_func=self.change_background_colour, render=lambda _: self.fading_render(_)))
        return
