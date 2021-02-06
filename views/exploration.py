import arcade
from vector import Vector
from state import state
from arcade import key


class Explore(arcade.View):
    key_offset = {
        key.W: (0, 1),
        key.A: (-1, 0),
        key.S: (0, -1),
        key.D: (1, 0)
    }

    def on_draw(self):
        arcade.start_render()
        center_screen = Vector(self.window.width / 2, self.window.height / 2)
        arcade.draw_circle_filled(center_screen.x, center_screen.y, 25, arcade.color.AERO_BLUE)
        arcade.draw_rectangle_outline(center_screen.x, center_screen.y, 500, 500, arcade.color.DARK_GRAY, 2)
        arcade.draw_text(str(state.player.pos.tuple()), center_screen.x, center_screen.y + (state.cell_size.y * .37),
                         arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=12, anchor_x='center', anchor_y='center')
        render_queue = []
        for x_off, y_off in state.generate_radius(state.render_radius):
            real_grid_pos = state.player.pos + (x_off, y_off)
            render_pos = Vector(center_screen.x + x_off * state.cell_size.x, center_screen.y + y_off * state.cell_size.y)

            if tile := state.grid.get(*real_grid_pos):
                render_queue.append(
                    (tile, render_pos, render_pos + (-(state.cell_size.x / 2), state.cell_size.y / 2), state.cell_size))
            else:
                arcade.draw_rectangle_outline(render_pos.x, render_pos.y, state.cell_size.x - 2, state.cell_size.y - 2,
                                              arcade.color.DARK_GRAY)
        for tile, *args in render_queue:
            tile.on_render(*args)

    def on_key_release(self, symbol, mods):
        if tile := state.grid.get(*state.player.pos):
            tile.key_up(symbol, mods)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in self.key_offset:
            offset = Vector(*self.key_offset[symbol])
            prior_player_pos = state.player.pos
            new_player_pos = prior_player_pos + offset

            from views import MovementAnimator
            state.window.show_view(MovementAnimator(prior_player_pos, new_player_pos, 5))

            state.player.pos = new_player_pos
            if tile := state.grid.get(*prior_player_pos):
                tile.on_exit()
            if tile := state.grid.get(*new_player_pos):
                tile.on_enter()
        else:
            if tile := state.grid.get(*state.player.pos):
                tile.key_down(symbol, modifiers)
