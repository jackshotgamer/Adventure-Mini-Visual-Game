import arcade
import arcade.gui
from arcade import key

from W_Main_File.Utilities import Button_Functions, Action_Queue
from W_Main_File.Views import Purgatory_Screen, Event_Base
from W_Main_File.Data import Sprites_
from W_Main_File.Essentials import State
import time
import random
from W_Main_File.Tiles import Loot_Functions, Trapdoor_Functions, Trap_Functions, Enemy
from W_Main_File.Utilities.Vector import Vector


class Explore(Event_Base.EventBase):
    fps = 0
    last_update = 0
    symbol_ = arcade.key.D
    previous_pos = Vector(0, 0)
    current_window_size = Vector(1000, 800)

    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        if not State.state.preoccupied:
            self.ui_manager.purge_ui_elements()
        Button_Functions.register_custom_exploration_buttons(self.button_manager, self.ui_manager)
        State.state.is_moving = False
        if ((State.state.moves_since_texture_save > 2 and State.state.is_new_tile) or State.state.player.pos == (0, 0)) and not State.state.player.meta_data.is_guest:
            for offset in State.state.generate_radius(5):
                State.state.tile_type_pos(*(offset + State.state.player.pos))
            State.state.is_new_tile = False
            State.state.moves_since_texture_save = 0
        self.should_transition_to_animation = [False, 0, 0, lambda: None]
        if not State.state.grid.get(-1, 0):
            State.state.grid.add(Trapdoor_Functions.TrapdoorTile(Vector(-1, 0)))
        if not State.state.grid.get(2, 0):
            State.state.grid.add(Loot_Functions.LootTile(Vector(2, 0)))

    def update(self, delta_time: float):
        from W_Main_File.Views import Fading
        if State.state.player.hp <= 0:
            State.state.window.show_view(Fading.Fading((lambda: Purgatory_Screen.PurgatoryScreen('You Died', True)), 7, 4, should_reverse=False,
                                                       should_freeze=True, reset_pos=Vector(0, 0), render=lambda _: self.on_draw()))
            State.state.clear_current_floor_data()
        if Action_Queue.action_queue:
            action = Action_Queue.action_queue.popleft()
            action()
        if self.should_transition_to_animation[0]:
            from W_Main_File.Views.Movement_Animator import MovementAnimator
            State.state.window.show_view(MovementAnimator(self.should_transition_to_animation[1],
                                                          self.should_transition_to_animation[2], 14 if (State.state.window.width, State.state.window.height) == (1000, 800) else 14))
            self.should_transition_to_animation[0] = False
            self.should_transition_to_animation[3]()
        else:
            Sprites_.update_backdrop()
            self.check_if_resized()
            if Explore.last_update == 0 or time.time() - Explore.last_update > 0.5:
                Explore.fps = 1 / delta_time
                Explore.last_update = time.time()

            for x_off, y_off in State.state.generate_radius(State.state.render_radius):
                real_grid_pos = State.state.player.pos + (x_off, y_off)

                if tile := State.state.grid.get(*real_grid_pos):
                    tile.on_update(delta_time)

    def check_if_resized(self):
        if self.current_window_size.x == State.state.window.width and self.current_window_size.y == State.state.window.height:
            return
        else:
            Button_Functions.register_custom_exploration_buttons(self.button_manager, self.ui_manager)
            self.current_window_size = Vector(State.state.window.width, State.state.window.height)

    key_offset = {
        key.W: (0, 1),
        key.A: (-1, 0),
        key.S: (0, -1),
        key.D: (1, 0)
    }

    def on_draw(self):
        arcade.start_render()
        center_screen = State.state.screen_center
        render_queue = []
        cell_render_size = (State.state.cell_size * ((State.state.window.width / State.state.default_window_size.x), (State.state.window.height / State.state.default_window_size.y)))
        for x_off, y_off in State.state.generate_radius(State.state.render_radius):
            real_grid_pos = State.state.player.pos + (x_off, y_off)
            render_pos = Vector(center_screen.x + x_off * cell_render_size.x, center_screen.y + y_off * cell_render_size.y)
            arcade.draw_texture_rectangle(render_pos.x, render_pos.y, cell_render_size.x, cell_render_size.y, State.state.tile_type_pos(*real_grid_pos))

        for x_off, y_off in State.state.generate_radius(State.state.render_radius):
            real_grid_pos = State.state.player.pos + (x_off, y_off)
            render_pos = Vector(center_screen.x + x_off * cell_render_size.x, center_screen.y + y_off * cell_render_size.y)

            if tile := State.state.grid.get(*real_grid_pos):
                render_queue.append((tile, render_pos, render_pos + (-(cell_render_size.x / 2), cell_render_size.y / 2), cell_render_size))
            else:
                arcade.draw_rectangle_outline(render_pos.x, render_pos.y, cell_render_size.x, cell_render_size.y, (120, 120, 120))

        for tile, *args in render_queue:
            tile.on_render(*args)

        arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y,
                                      State.state.cell_render_size.x * 0.95, State.state.cell_render_size.y * 0.95, Sprites_.black_circle_sprite, 0, 75)
        arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y,
                                      State.state.cell_render_size.x * 0.95, State.state.cell_render_size.y * 0.95, Sprites_.black_circle_square_sprite, 0, 100)
        arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y,
                                      State.state.cell_render_size.x * 0.95, State.state.cell_render_size.y * 0.95, Sprites_.black_square_circle_square_sprite, 0, 125)

        arcade.draw_rectangle_filled(center_screen.x, center_screen.y - (State.state.window.height * 0.3375), State.state.window.width * 0.625, State.state.window.height * 0.0475, (0, 0, 0))
        # arcade.draw_circle_filled(center_screen.x, center_screen.y, 25, arcade.color.AERO_BLUE)
        arcade.draw_rectangle_outline(center_screen.x, center_screen.y, State.state.window.width * 0.5, State.state.window.height * 0.625, (120, 120, 120), 4)
        screen_percentage_of_default = (State.state.window.height / State.state.default_window_size.y)
        arcade.draw_text(f'Name: {State.state.player.name}', State.state.window.width * 0.275, State.state.window.height * 0.1625, arcade.color.LIGHT_GRAY,
                         font_size=(11 * screen_percentage_of_default), font_name='arial')
        arcade.draw_text(f'Hp: {int(State.state.player.hp)} / {int(State.state.player.max_hp)}', State.state.window.width * 0.475, State.state.window.height * 0.1625, arcade.color.LIGHT_GRAY,
                         font_size=(11 * screen_percentage_of_default), font_name='arial')
        arcade.draw_text(f'Level: {int(State.state.player.lvl)}', State.state.window.width * 0.67, State.state.window.height * 0.1625, arcade.color.LIGHT_GRAY,
                         font_size=(11 * screen_percentage_of_default), font_name='arial')
        arcade.draw_text(f'Gold: {int(State.state.player.gold)}', State.state.window.width * 0.355, State.state.window.height * 0.8125, arcade.color.LIGHT_GRAY,
                         font_size=(14 * screen_percentage_of_default), font_name='arial')
        arcade.draw_text(f'xp: {int(State.state.player.xp)}', State.state.window.width * 0.565, State.state.window.height * 0.8125, arcade.color.LIGHT_GRAY,
                         font_size=(14 * screen_percentage_of_default), font_name='arial')
        arcade.draw_text(f'Floor: {int(State.state.player.floor)}', State.state.window.width * 0.5, (State.state.window.height * 0.5) - (cell_render_size.y * .37), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=(12 * screen_percentage_of_default), anchor_x='center', anchor_y='center')
        arcade.draw_text(str(State.state.player.pos.tuple()), State.state.window.width * 0.5, (State.state.window.height * 0.5) + (cell_render_size.y * .37), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=(12 * screen_percentage_of_default), anchor_x='center', anchor_y='center')
        Sprites_.draw_backdrop()

        if Explore.symbol_ == arcade.key.D:
            arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y,
                                          State.state.cell_render_size.y * 0.75, State.state.cell_render_size.y * 0.75, Sprites_.knight_start_2)
        elif Explore.symbol_ == arcade.key.A:
            arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y,
                                          State.state.cell_render_size.y * 0.75, State.state.cell_render_size.y * 0.75, Sprites_.knight_start_flipped)
        from W_Main_File.Utilities import Inventory_GUI
        Inventory_GUI.render_inventory()
        arcade.draw_text(f'FPS = {self.fps:.1f}', 2, self.window.height - 22, arcade.color.GREEN,
                         font_name='arial', font_size=14)
        for tile, *args in render_queue:
            tile.on_render_foreground(*args)
        self.button_manager.render()

    def on_key_release(self, symbol, mods):
        if tile := State.state.grid.get(*State.state.player.pos):
            tile.key_up(symbol, mods)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        thing_to_do = (State.state.grid.get(*State.state.player.pos, default="EmptyTile"))
        thing_to_do_2 = (State.state.grid.get(*self.previous_pos, default="EmptyTile"))
        print(f'Current tile: {thing_to_do.__class__.__name__ if not thing_to_do.__class__.__name__ == "str" else "EmptyTile"}'
              f'\nPrevious tile: {thing_to_do_2.__class__.__name__ if not thing_to_do_2.__class__.__name__ == "str" else "EmptyTile"}\n')

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.B:
            State.state.player.hp -= State.state.player.max_hp
        if symbol in self.key_offset:
            if symbol in (arcade.key.A, arcade.key.D):
                self.__class__.symbol_ = symbol
            if State.state.preoccupied:
                return
            self.__class__.previous_pos = State.state.player.pos
            State.state.moves_since_texture_save += 1
            offset = Vector(*self.key_offset[symbol])
            prior_player_pos = State.state.player.pos
            new_player_pos = prior_player_pos + offset

            if tile := State.state.grid.get(*prior_player_pos):
                if not tile.can_player_move():
                    return
                tile.on_exit()
            if tile := State.state.grid.get(*new_player_pos):
                tile.on_enter()

            def after_update():
                State.state.player.pos = new_player_pos

                if (
                        not State.state.grid.get(new_player_pos.x, new_player_pos.y)
                        and random.random() < 0.02
                        and State.state.texture_mapping.get(f'{new_player_pos.x} {new_player_pos.y}') in {'1', '2'}
                        and new_player_pos.tuple() not in State.state.grid.visited_tiles
                ):
                    loot = Loot_Functions.LootTile(new_player_pos)
                    State.state.grid.add(loot)
                elif (
                        not State.state.grid.get(new_player_pos.x, new_player_pos.y)
                        and random.random() < 0.05
                        and State.state.texture_mapping.get(f'{new_player_pos.x} {new_player_pos.y}') in {'1'}
                        and new_player_pos.tuple() not in State.state.grid.visited_tiles
                ):
                    enemy = Enemy.EnemyTile(new_player_pos)
                    State.state.grid.add(enemy)
                # elif (
                #         not State.state.grid.get(new_player_pos.x, new_player_pos.y)
                #         and random.random() < 0.02
                #         and State.state.texture_mapping.get(f'{new_player_pos.x} {new_player_pos.y}') in {'1', '2'}
                #         and new_player_pos.tuple() not in State.state.grid.visited_tiles
                # ):
                #     pass
                elif (
                        State.state.get_tile_id(Vector(new_player_pos.x, new_player_pos.y)) in ('0.5', '1.5')
                        and not State.state.grid.get(new_player_pos.x, new_player_pos.y)
                ):
                    trap = Trap_Functions.TrapTile(new_player_pos)
                    trap.on_enter()
                    State.state.grid.add(trap)

                State.state.grid.add_visited_tile(new_player_pos)

            self.should_transition_to_animation = [True, prior_player_pos, new_player_pos, after_update]

        else:
            if tile := State.state.grid.get(*State.state.player.pos):
                tile.key_down(symbol, modifiers)
