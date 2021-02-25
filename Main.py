import arcade
import Exploration
import State
import Tile
import Vector
import Player_Select
import Sprites


class TestRender(Tile.Tile):
    def on_render(self, center, top_left, cell_size):
        arcade.draw_rectangle_outline(center.x, center.y, State.state.cell_size.x - 2, State.state.cell_size.y - 2, arcade.color.BRONZE)
        # arcade.draw_texture_rectangle()

    def key_down(self, keycode, mods):
        print(keycode)


window = arcade.Window(width=1000, height=800)
State.state.window = window
window.show_view(Player_Select.PlayerSelect())
State.state.grid.add(TestRender(Vector.Vector(1, 0)))

arcade.run()
