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
    def __init__(self, combatant: Enemy_Data.EnemyData):
        super().__init__()
        self.combatant = combatant
        self.colour = 200
        self.truthy = False
        self.key_ = False

    def on_draw(self):
        arcade.set_background_color((18, 18, 18))
        arcade.start_render()
        arcade.draw_ellipse_filled(State.state.window.width / 1.3, State.state.window.height / 1.4, 250, 100, (90, 0, 0))
        arcade.draw_texture_rectangle(State.state.window.width / 1.3, State.state.window.height / 1.4, 170, 65, Sprites_.black_circle_sprite, alpha=100)
        arcade.draw_arc_outline(State.state.window.width / 1.3, State.state.window.height / 1.4, 250, 100, (125, 0, 0), 0, 180, 15)
        arcade.draw_arc_outline(State.state.window.width / 1.3, State.state.window.height / 1.4, 250, 100, (150, 0, 0), 180, 360, 15)
        arcade.draw_texture_rectangle(State.state.window.width / 1.3, (State.state.window.height / 1.4) + 65, 150, 150, Sprites_.swamp_monster)

        arcade.draw_ellipse_filled(State.state.window.width / 5, State.state.window.height / 2.4, 250, 100, (90, 0, 0))
        arcade.draw_texture_rectangle(State.state.window.width / 5, State.state.window.height / 2.4, 140, 65, Sprites_.black_circle_sprite, alpha=100)
        arcade.draw_arc_outline(State.state.window.width / 5, State.state.window.height / 2.4, 250, 100, (125, 0, 0), 0, 180, 15)
        arcade.draw_arc_outline(State.state.window.width / 5, State.state.window.height / 2.4, 250, 100, (150, 0, 0), 180, 360, 15)
        if not self.key_:
            arcade.draw_texture_rectangle(State.state.window.width / 5, (State.state.window.height / 2.4) + 65, 150, 150, Sprites_.knight_start)
        else:
            arcade.draw_texture_rectangle(State.state.window.width / 5, (State.state.window.height / 2.4) + 65, 150, 150, Sprites_.knight_start_flipped)

        arcade.draw_rectangle_filled(State.state.window.width / 2, (State.state.window.height / 2.4) - (100 + 125), State.state.window.width, 225, (200, 200, 200))
        arcade.draw_rectangle_outline(State.state.window.width / 2, ((State.state.window.height / 2.4) - (100 + 125)) + 6, State.state.window.width - 10, 230 - 10, (100, 100, 100), 10)
        # 100, 480
        arcade.draw_text(f'{State.state.player.hp} / {State.state.player.max_hp}\nHealth', State.state.window.width / 5,
                         State.state.window.height * 0.61, (255 - int(self.colour * 255), int(self.colour * 255), 0), 20, 150, 'center', anchor_x='center', anchor_y='center')

    def update(self, delta_time: float):
        self.colour = State.state.player.hp / State.state.player.max_hp
        if self.truthy:
            State.state.player.hp -= 1
        from W_Main_File.Views import Exploration
        if Exploration.Explore.symbol_ == arcade.key.D:
            self.key_ = False
        elif Exploration.Explore.symbol_ == arcade.key.A:
            self.key_ = True

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        print(f'*{x}*, *{y}*')

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.H:
            self.truthy = True

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.H:
            self.truthy = False
