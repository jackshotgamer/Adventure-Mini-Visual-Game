import time

import arcade
import Vector
import State
import Sprites_


class MovementAnimator(arcade.View):
    def __init__(self, grid_start, grid_end, animation_steps):
        super().__init__()
        self.render_radius = State.state.render_radius
        self.grid_start = grid_start
        self.grid_end = grid_end
        self.animation_steps = animation_steps
        self.current_steps = 0
        self.tile_render_offset = Vector.Vector(0, 0)
        self.affected_tiles = self.get_affected_tiles()
        self.empty_tiles = self.get_empty_tiles()
        State.state.is_moving = True

    def get_affected_tiles(self):
        tile_pos = set()
        center = State.state.screen_center
        for offset in State.state.generate_radius(self.render_radius):
            tile_pos.update((self.grid_end + offset, self.grid_start + offset))
        return [
            (tile, ((pos - self.grid_start) * State.state.cell_size) + center, ((pos - self.grid_end) * State.state.cell_size) + center)
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
                ((pos - self.grid_start) * State.state.cell_size) + center,
                ((pos - self.grid_end) * State.state.cell_size) + center
            )
            for pos in tile_pos
            if State.state.grid.get(*pos) is None
        ]

    def update(self, delta_time: float):
        import Exploration
        self.current_steps += 1
        if self.current_steps > self.animation_steps:
            State.state.window.show_view(Exploration.Explore())
        Sprites_.update_backdrop()
        if Exploration.Explore.last_update == 0 or time.time() - Exploration.Explore.last_update > 0.5:
            Exploration.Explore.fps = 1 / delta_time
            Exploration.Explore.last_update = time.time()

    def on_draw(self):
        import Sprites_
        arcade.start_render()
        center = State.state.screen_center
        if self.affected_tiles:
            first_tile = self.affected_tiles[0][1:]
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

        for offset in State.state.generate_radius(3):
            # noinspection PyUnboundLocalVariable
            real_grid_pos = State.state.player.pos + offset
            render_pos = (center + (State.state.cell_size * offset)) + sprite_offset
            arcade.draw_texture_rectangle(render_pos.x, render_pos.y, 100, 100, State.state.tile_type_pos(*real_grid_pos))

        for tile, start, end in self.affected_tiles:
            tile_center = Vector.Vector(*arcade.lerp_vec(start, end, self.current_steps / self.animation_steps))
            tile.on_render(tile_center, tile_center + (-(State.state.cell_size.x / 2), State.state.cell_size.y / 2), State.state.cell_size)
            # sprite_offset = tile_center - end

        arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y, 99, 99, Sprites_.black_circle_sprite, 0, 75)
        arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y, 99, 99, Sprites_.black_circle_square_sprite, 0, 100)
        arcade.draw_texture_rectangle(State.state.screen_center.x, State.state.screen_center.y, 99, 99, Sprites_.black_square_circle_square_sprite, 0, 125)

        for start, end in self.empty_tiles:
            tile_center = Vector.Vector(*arcade.lerp_vec(start, end, self.current_steps / self.animation_steps))
            arcade.draw_rectangle_outline(tile_center.x, tile_center.y, State.state.cell_size.x - 2, State.state.cell_size.y - 2, (120, 120, 120))
            # sprite_offset = tile_center - end

        arcade.draw_circle_filled(center.x, center.y, 25, arcade.color.AERO_BLUE)
        arcade.draw_rectangle_outline(center.x, center.y, 500, 500, arcade.color.DARK_GRAY)
        arcade.draw_rectangle_filled(center.x, center.y - 270, 500, 38, (0, 0, 0))
        arcade.draw_rectangle_filled(center.x, center.y + 270, 500, 38, (0, 0, 0))
        arcade.draw_text(f'Name: {State.state.player.name}', center.x - 225, center.y - 270, arcade.color.LIGHT_GRAY,
                         font_size=11, font_name='arial')
        arcade.draw_text(f'Hp: {int(State.state.player.hp)}', center.x - 25, center.y - 270, arcade.color.LIGHT_GRAY,
                         font_size=11, font_name='arial')
        arcade.draw_text(f'Level: {int(State.state.player.lvl)}', center.x + 170, center.y - 270, arcade.color.LIGHT_GRAY,
                         font_size=11, font_name='arial')
        arcade.draw_text(f'Gold: {int(State.state.player.gold)}', center.x - 145, center.y + 250, arcade.color.LIGHT_GRAY,
                         font_size=14, font_name='arial')
        arcade.draw_text(f'xp: {int(State.state.player.xp)}', center.x + 65, center.y + 250, arcade.color.LIGHT_GRAY,
                         font_size=14, font_name='arial')
        arcade.draw_text(f'Floor: {int(State.state.player.floor)}', center.x, center.y - (State.state.cell_size.y * .37), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=12, anchor_x='center', anchor_y='center')
        arcade.draw_text(str(State.state.player.pos.tuple()), center.x, center.y + (State.state.cell_size.y * .37), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=12, anchor_x='center', anchor_y='center')
        Sprites_.draw_backdrop()
        import Exploration
        arcade.draw_text(f'FPS = {Exploration.Explore.fps:.1f}', 2, self.window.height - 22, arcade.color.GREEN,
                         font_name='arial', font_size=14)
        for tile, start, end in self.affected_tiles:
            tile_center = Vector.Vector(*arcade.lerp_vec(start, end, self.current_steps / self.animation_steps))
            tile.on_render_foreground(tile_center, tile_center + (-(State.state.cell_size.x / 2), State.state.cell_size.y / 2), State.state.cell_size)

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
