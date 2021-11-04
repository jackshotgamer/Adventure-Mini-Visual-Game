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

    def __init__(self, combatant: Enemy_Data.EnemyData):
        super().__init__()
        self.combatant = combatant
        self.colour = State.state.player.hp / State.state.player.max_hp
        self.colour2 = self.combatant.hp / self.combatant.max_hp
        self.truthy = False
        self.truthy2 = False
        self.key_ = False
        self.is_turn = True
        self.symbol2 = arcade.key.D
        self.current_window_size = Vector(State.state.window.width, State.state.window.height)
        from W_Main_File.Tiles import Enemy
        from W_Main_File.Views import Exploration
        self.explore = Exploration.Explore()
        self.buttons()

    def on_draw(self):
        arcade.set_background_color((18, 18, 18))
        arcade.start_render()
        arcade.draw_ellipse_filled(State.state.window.width / 1.3, State.state.window.height / 1.4, 250, 100, (90, 0, 0))
        arcade.draw_texture_rectangle(State.state.window.width / 1.3, State.state.window.height / 1.4, 170, 65, Sprites_.black_circle_sprite, alpha=100)
        arcade.draw_arc_outline(State.state.window.width / 1.3, State.state.window.height / 1.4, 250, 100, (125, 0, 0), 0, 180, 15)
        arcade.draw_arc_outline(State.state.window.width / 1.3, State.state.window.height / 1.4, 250, 100, (150, 0, 0), 180, 360, 15)
        arcade.draw_texture_rectangle(State.state.window.width / 1.3, (State.state.window.height / 1.4) + 65, 150, 150, self.sprite[self.combatant.name])

        arcade.draw_ellipse_filled(State.state.window.width / 5, State.state.window.height / 2.4, 250, 100, (90, 0, 0))
        arcade.draw_texture_rectangle(State.state.window.width / 5, State.state.window.height / 2.4, 140, 65, Sprites_.black_circle_sprite, alpha=100)
        arcade.draw_arc_outline(State.state.window.width / 5, State.state.window.height / 2.4, 250, 100, (125, 0, 0), 0, 180, 15)
        arcade.draw_arc_outline(State.state.window.width / 5, State.state.window.height / 2.4, 250, 100, (150, 0, 0), 180, 360, 15)
        if not self.key_:
            arcade.draw_texture_rectangle(State.state.window.width / 5, (State.state.window.height / 2.4) + 65, 150, 150, Sprites_.knight_start_2)
        else:
            arcade.draw_texture_rectangle(State.state.window.width / 5, (State.state.window.height / 2.4) + 65, 150, 150, Sprites_.knight_start_flipped)

        arcade.draw_rectangle_filled(State.state.window.width / 2,
                                     (State.state.window.height / 2.4) - ((State.state.window.height * 0.125) + (State.state.window.height * 0.15625)),
                                     State.state.window.width, State.state.window.height * 0.2875, (200, 200, 200))
        arcade.draw_rectangle_outline(State.state.window.width / 2, ((State.state.window.height / 2.4) - ((State.state.window.height * 0.125) + (State.state.window.height * 0.15625))) + 6,
                                      State.state.window.width - 10, State.state.window.height * 0.2875 - 10, (100, 100, 100), 10)
        # 100, 480
        arcade.draw_text(f'{State.state.player.hp} / {State.state.player.max_hp}\nHealth', State.state.window.width / 5,
                         State.state.window.height * 0.61, (255 - int(self.colour * 255), int(self.colour * 255), 0), 20, 150, 'center', anchor_x='center', anchor_y='center')
        arcade.draw_text(f'{self.combatant.hp} / {self.combatant.max_hp}\nHealth', State.state.window.width / 1.3,
                         State.state.window.height * 0.61, (255 - int(self.colour2 * 255), int(self.colour2 * 255), 0), 20, 150, 'center', anchor_x='center', anchor_y='center')
        self.button_manager.render()
        State.state.render_mouse()

    def change_background_colour(self):
        arcade.set_background_color((0, 0, 0))
        self.truthy = self.truthy

    def check_if_resized(self):
        if self.current_window_size.x == State.state.window.width and self.current_window_size.y == State.state.window.height:
            return
        else:
            self.buttons()
            self.current_window_size = Vector(State.state.window.width, State.state.window.height)

    def

    def buttons(self):
        screen_percentage_of_default = (State.state.window.height / State.state.default_window_size.y)
        self.button_manager.append('Flee', f'Flee from {self.combatant.name}', Vector((State.state.window.width * 0.13), (State.state.window.height * 0.06875)),
                                   Vector((State.state.window.width * 0.2), (State.state.window.height * 0.0625)), text_size=(16 * screen_percentage_of_default), on_click=self.flee)

    def update(self, delta_time: float):
        self.check_if_resized()
        self.colour = State.state.player.hp / State.state.player.max_hp
        self.colour2 = self.combatant.hp / self.combatant.max_hp
        if State.state.player.hp <= 0:
            from W_Main_File.Views import Purgatory_Screen, Fading
            State.state.window.show_view(Fading.Fading((lambda: Purgatory_Screen.PurgatoryScreen(f'You were killed by a {self.combatant.name}', increment_death=True)), 7, 4, should_reverse=False,
                                                       should_freeze=True, reset_pos=Vector(0, 0), halfway_func=self.change_background_colour, render=lambda _: self.fading_render(_)))
            State.state.clear_current_floor_data()
            return
        if self.combatant.hp <= 0:
            from W_Main_File.Views import Fading
            State.state.window.show_view(Fading.Fading(lambda: self.explore, 7, 4, should_reverse=True,
                                                       should_freeze=True, halfway_func=self.change_background_colour, render=lambda _: self.fading_render(_)))
            return
        if self.truthy:
            State.state.player.hp -= 2
        if self.truthy2:
            self.combatant.hp -= 1
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
