import time

import arcade
import arcade.gui
from W_Main_File.Data import Sprites_
from W_Main_File.Essentials import State
from W_Main_File.Utilities import Vector, Button_Functions
from W_Main_File.Views import Event_Base


class MovementAnimator(Event_Base.EventBase):
    def __init__(self, grid_start, grid_end, animation_steps):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        self.render_radius = State.state.render_radius
        self.grid_start = grid_start
        self.grid_end = grid_end
        self.animation_steps = animation_steps
        self.current_steps = 0
        Button_Functions.register_custom_exploration_buttons(self.button_manager, self.ui_manager, False)
        self.tile_render_offset = Vector.Vector(0, 0)
        self.affected_tiles = self.get_affected_tiles()
        self.empty_tiles = self.get_empty_tiles()
        State.state.is_moving = True
        self.enemy_tiles = []

    def get_affected_tiles(self):
        tile_pos = set()
        center = State.state.screen_center
        for offset in State.state.generate_radius(self.render_radius):
            tile_pos.update((self.grid_end + offset, self.grid_start + offset))
        return [
            (tile, ((pos - self.grid_start) * self.cell_render_size) + center, ((pos - self.grid_end) * self.cell_render_size) + center)
            for pos in tile_pos
            if (tile := State.state.grid.get(*pos))
        ]

    def get_empty_tiles(self):
        tile_pos = set()
        center = State.state.screen_center
        for offset in State.state.generate_radius(self.render_radius):
            tile_pos.update((self.grid_end + offset, self.grid_start + offset))
        return [
            (
                ((pos - self.grid_start) * self.cell_render_size) + center,
                ((pos - self.grid_end) * self.cell_render_size) + center
            )
            for pos in tile_pos
            if State.state.grid.get(*pos) is None
        ]

    def update(self, delta_time: float):
        from W_Main_File.Views import Exploration
        self.current_steps += 1
        if self.current_steps > self.animation_steps:
            State.state.is_moving = False
            State.state.window.show_view(Exploration.Explore())
        Sprites_.update_backdrop()
        Sprites_.update_character()
        if Exploration.Explore.last_update == 0 or time.time() - Exploration.Explore.last_update > 0.5:
            Exploration.Explore.fps = 1 / delta_time
            Exploration.Explore.last_update = time.time()

    @property
    def cell_render_size(self):
        return State.state.cell_size * ((State.state.window.width / State.state.default_window_size.x), (State.state.window.height / State.state.default_window_size.y))

    def on_draw(self):
        arcade.start_render()
        center = State.state.screen_center
        if self.affected_tiles:
            first_tile = self.affected_tiles[0][1:]  # [start:stop:step]
        else:
            first_tile = self.empty_tiles[0]
        sprite_offset = \
            Vector.Vector(
                *arcade.lerp_vec(
                    first_tile[0],
                    first_tile[1],
                    self.current_steps /
                    self.animation_steps)
            ) - first_tile[1]

        for offset in State.state.generate_radius(State.state.render_radius):
            # noinspection PyUnboundLocalVariable
            real_grid_pos = State.state.player.pos + offset
            render_pos = (center + (self.cell_render_size * offset)) + sprite_offset
            arcade.draw_texture_rectangle(render_pos.x, render_pos.y, self.cell_render_size.x, self.cell_render_size.y, State.state.tile_type_pos(*real_grid_pos))

        for tile, start, end in self.affected_tiles:
            tile_center = Vector.Vector(*arcade.lerp_vec(start, end, self.current_steps / self.animation_steps))
            tile.on_render(tile_center, tile_center + (-(self.cell_render_size.x / 2), self.cell_render_size.y / 2), self.cell_render_size)

        for start, end in self.empty_tiles:
            tile_center = Vector.Vector(*arcade.lerp_vec(start, end, self.current_steps / self.animation_steps))
            arcade.draw_rectangle_outline(tile_center.x, tile_center.y, self.cell_render_size.x, self.cell_render_size.y, (120, 120, 120))

        # arcade.draw_circle_filled(center.x, center.y, 25, arcade.color.AERO_BLUE)
        arcade.draw_rectangle_filled(center.x, center.y - (State.state.window.height * 0.3375), State.state.window.width * 0.625, State.state.window.height * 0.0475, (0, 0, 0))
        arcade.draw_rectangle_filled(center.x, center.y + (State.state.window.height * 0.3375), State.state.window.width * 0.625, State.state.window.height * 0.0475, (0, 0, 0))
        arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y,
                                      State.state.cell_render_size.x * 0.95, State.state.cell_render_size.y * 0.95, Sprites_.black_circle_sprite, 0, 75)
        arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y,
                                      State.state.cell_render_size.x * 0.95, State.state.cell_render_size.y * 0.95, Sprites_.black_circle_square_sprite, 0, 100)
        arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y,
                                      State.state.cell_render_size.x * 0.95, State.state.cell_render_size.y * 0.95, Sprites_.black_square_circle_square_sprite, 0, 125)
        screen_percentage_of_default = (State.state.window.height / State.state.default_window_size.y)
        arcade.draw_text(f'Floor: {int(State.state.player.floor)}', State.state.window.width * 0.5, (State.state.window.height * 0.5) - (self.cell_render_size.y * .37), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=(12 * screen_percentage_of_default), anchor_x='center', anchor_y='center')
        arcade.draw_text(str(State.state.player.pos.tuple()), State.state.window.width * 0.5, (State.state.window.height * 0.5) + (self.cell_render_size.y * .37), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=(12 * screen_percentage_of_default), anchor_x='center', anchor_y='center')
        Sprites_.draw_backdrop()
        Sprites_.draw_character()
        arcade.draw_rectangle_outline(center.x, center.y, State.state.window.width * 0.5, State.state.window.height * 0.625, (120, 120, 120), 4)
        from W_Main_File.Views import Exploration
        arcade.draw_text(f'FPS = {Exploration.Explore.fps:.1f}', 2, self.window.height - 22, arcade.color.GREEN,
                         font_name='arial', font_size=14)
        for tile, start, end in self.affected_tiles:
            tile_center = Vector.Vector(*arcade.lerp_vec(start, end, self.current_steps / self.animation_steps))
            tile.on_render_foreground(tile_center, tile_center + (-(self.cell_render_size.x / 2), self.cell_render_size.y / 2), self.cell_render_size)
        self.text_render()
        self.button_manager.render()

    # noinspection PyMethodMayBeStatic,PyProtectedMember
    def text_render(self):
        screen_percentage_of_default = (State.state.window.height / State.state.default_window_size.y)
        # arcade.draw_rectangle_filled(State.state.window.width / 2, State.state.window.height * 0.8275, State.state.window.width * 0.333333334, State.state.window.height * 0.03125,
        #                              arcade.color.BLACK)
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
        State.state.render_mouse()

    @staticmethod
    def draw_edges(inner_radius):
        cell_size = State.state.cell_size
        for x_off in range(~ inner_radius, inner_radius + 2):
            render = (Vector.Vector(x_off, inner_radius + 1) * cell_size) + State.state.screen_center
            arcade.draw_rectangle_filled(render.x, render.y, cell_size.x - 1, cell_size.y - 1, arcade.color.BLACK)

            render = (Vector.Vector(x_off, -(inner_radius + 1)) * cell_size) + State.state.screen_center
            arcade.draw_rectangle_filled(render.x, render.y, cell_size.x - 1, cell_size.y - 1, arcade.color.BLACK)

        for y_off in range(~ inner_radius, inner_radius + 2):
            render = (Vector.Vector(inner_radius + 1, y_off) * cell_size) + State.state.screen_center
            arcade.draw_rectangle_filled(render.x, render.y, cell_size.x - 1, cell_size.y - 1, arcade.color.BLACK)

            render = (Vector.Vector(-(inner_radius + 1), y_off) * cell_size) + State.state.screen_center
            arcade.draw_rectangle_filled(render.x, render.y, cell_size.x - 1, cell_size.y - 1, arcade.color.BLACK)
