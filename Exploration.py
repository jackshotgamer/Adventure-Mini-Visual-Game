import arcade
from Vector import Vector
import State
from arcade import key
import Button_Functions
import arcade.gui


class Explore(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.purge_ui_elements()
        Button_Functions.register_ui_buttons(self.ui_manager)

    def on_update(self, delta_time: float):
        Button_Functions.reposition_button(self.ui_manager)

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
        arcade.draw_text(f'Name: {State.state.player.name}', center_screen.x - 250, center_screen.y - 270, arcade.color.LIGHT_GRAY,
                         font_size=12, font_name='arial')
        arcade.draw_text(f'Hp: {State.state.player.hp}', center_screen.x - 25, center_screen.y - 270, arcade.color.LIGHT_GRAY,
                         font_size=12, font_name='arial')
        arcade.draw_text(f'Level: {State.state.player.lvl}', center_screen.x + 170, center_screen.y - 270, arcade.color.LIGHT_GRAY,
                         font_size=12, font_name='arial')
        arcade.draw_text(f'Gold: {State.state.player.gold}', center_screen.x - 145, center_screen.y + 250, arcade.color.LIGHT_GRAY,
                         font_size=14, font_name='arial')
        arcade.draw_text(f'xp: {State.state.player.xp}', center_screen.x + 55, center_screen.y + 250, arcade.color.LIGHT_GRAY,
                         font_size=14, font_name='arial')
        arcade.draw_text(f'Floor: {State.state.player.floor}', center_screen.x, center_screen.y - (State.state.cell_size.y * .37), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=12, anchor_x='center', anchor_y='center')
        arcade.draw_text(str(State.state.player.pos.tuple()), center_screen.x, center_screen.y + (State.state.cell_size.y * .37), arcade.color.LIGHT_GRAY,
                         font_name='arial', font_size=12, anchor_x='center', anchor_y='center')

        render_queue = []
        for x_off, y_off in State.state.generate_radius(State.state.render_radius):
            real_grid_pos = State.state.player.pos + (x_off, y_off)
            render_pos = Vector(center_screen.x + x_off * State.state.cell_size.x, center_screen.y + y_off * State.state.cell_size.y)

            if tile := State.state.grid.get(*real_grid_pos):
                render_queue.append((tile, render_pos, render_pos + (-(State.state.cell_size.x / 2), State.state.cell_size.y / 2), State.state.cell_size))
            else:
                arcade.draw_rectangle_outline(render_pos.x, render_pos.y, State.state.cell_size.x - 2, State.state.cell_size.y - 2, arcade.color.DARK_GRAY)

        for tile, *args in render_queue:
            tile.on_render(*args)

    def on_key_release(self, symbol, mods):
        if tile := State.state.grid.get(*State.state.player.pos):
            tile.key_up(symbol, mods)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in self.key_offset:
            offset = Vector(*self.key_offset[symbol])
            prior_player_pos = State.state.player.pos
            new_player_pos = prior_player_pos + offset

            from Movement_Animator import MovementAnimator
            State.state.window.show_view(MovementAnimator(prior_player_pos, new_player_pos, 13))

            State.state.player.pos = new_player_pos
            if tile := State.state.grid.get(*prior_player_pos):
                tile.on_exit()
            if tile := State.state.grid.get(*new_player_pos):
                tile.on_enter()
        else:
            if tile := State.state.grid.get(*State.state.player.pos):
                tile.key_down(symbol, modifiers)
