import arcade
import arcade.gui
from arcade import key
from pathlib import Path

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
        'Death Knight': Sprites_.death_knight,
        'Devouring Horror': Sprites_.devouring_horror,
        'Golden Serpent': Sprites_.golden_serpent,
        'Offspring of Shrub Niggurath': Sprites_.offspring_of_shub_niggurath,
        'Purgatory Dragon Skeleton': Sprites_.purgatory_dragon_skeleton,
        'Troglodyte': Sprites_.troglodyte,
        'Troglodyte Hellebardier': Sprites_.troglodyte_hellebardier,
    }

    def __init__(self):
        super().__init__()
        self.prev_cell_size = State.state.cell_size
        self.colour = State.state.player.hp / State.state.player.max_hp
        self.colour2 = State.state.player.hp / State.state.player.max_hp
        self.truthy = False
        self.truthy2 = False
        self.key_ = False
        self.delta_timer = 0
        self.symbol2 = arcade.key.D
        self.current_window_size = Vector(State.state.window.width, State.state.window.height)
        from W_Main_File.Views import Exploration
        self.explore = Exploration.Explore()
        self.rendered_once = 0
        self.buttons()

    def on_draw(self):
        arcade.set_background_color((18, 18, 18))
        arcade.start_render()
        Sprites_.draw_backdrop()
        arcade.draw_texture_rectangle(State.state.screen_center.xf, State.state.screen_center.yf, 700, 700, Sprites_.combat_terrain)
        if self.rendered_once == 1:
            State.state.cell_size = Vector((State.state.window.width * 0.5) / 9, (State.state.window.height * 0.625) / 9)
            self.rendered_once = 2
        elif self.rendered_once == 0:
            self.rendered_once = 1
        arcade.draw_rectangle_outline(State.state.screen_center.xf, State.state.screen_center.yf, 700, 700, arcade.color.GRAY, 6)
        # noinspection PyGlobalUndefined

        Sprites_.draw_cropped_backdrop()
        self.button_manager.render()
        State.state.render_mouse()

    def change_background_colour(self):
        State.state.cell_size = self.prev_cell_size
        self.explore.tile_renderer.first_render = True
        arcade.set_background_color((0, 0, 0))

    def check_if_resized(self):
        if self.current_window_size.x == State.state.window.width and self.current_window_size.y == State.state.window.height:
            return
        else:
            Sprites_.renew_cropped_backdrop()
            self.buttons()
            self.current_window_size = Vector(State.state.window.width, State.state.window.height)

    def buttons(self):
        self.button_manager.append('flee', 'Flee', Vector(State.state.window.width - (State.state.screen_center.x * 0.15), State.state.screen_center.y), Vector(100, 60),
                                   on_click=self.flee, text_colour=(200, 100, 100))

    def update(self, delta_time: float):
        self.delta_timer += delta_time
        if self.delta_timer > 0.35:
            self.check_if_resized()
            print(f'Resized {self.delta_timer}')
            self.delta_timer = 0
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
        Sprites_.update_backdrop()

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
