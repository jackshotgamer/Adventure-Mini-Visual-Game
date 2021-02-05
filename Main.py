import arcade
import Exploration
import State
import Tile
import Vector


class TestRender(Tile.Tile):
    def on_render(self, center, top_left, cell_size):
        arcade.draw_rectangle_outline(center.x, center.y, State.state.cell_size.x - 2, State.state.cell_size.y - 2, arcade.color.BRONZE)

    def key_down(self, keycode, mods):
        print(keycode)


window = arcade.Window(resizable=True)
window.show_view(Exploration.Explore())
State.state.window = window
State.state.grid.add(TestRender(Vector.Vector(1, 0)))

arcade.run()
