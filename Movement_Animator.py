import arcade
import Vector
import State


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
        self.current_steps += 1
        if self.current_steps > self.animation_steps:
            import Exploration
            State.state.window.show_view(Exploration.Explore())

    def on_draw(self):
        arcade.start_render()
        center = State.state.screen_center
        arcade.draw_rectangle_outline(center.x, center.y, 500, 500, arcade.color.DARK_GRAY)
        for start, end in self.empty_tiles:
            tile_center = Vector.Vector(*arcade.lerp_vec(start, end, self.current_steps / self.animation_steps))
            arcade.draw_rectangle_outline(tile_center.x, tile_center.y, State.state.cell_size.x - 2, State.state.cell_size.y - 2, arcade.color.DARK_GRAY)

        for tile, start, end in self.affected_tiles:
            tile_center = Vector.Vector(*arcade.lerp_vec(start, end, self.current_steps / self.animation_steps))
            tile.on_render(tile_center, tile_center + (-(State.state.cell_size.x / 2), State.state.cell_size.y / 2), State.state.cell_size)
        arcade.draw_circle_filled(center.x, center.y, 25, arcade.color.AERO_BLUE)
        self.draw_edges(self.render_radius)
        arcade.draw_text(str(State.state.player.pos.tuple()), center.x, center.y + (State.state.cell_size.y * .37), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=12, anchor_x='center', anchor_y='center')

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
