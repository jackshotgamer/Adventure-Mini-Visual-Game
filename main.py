import arcade
from views import exploration
from state import state
import tile
from vector import Vector


class TestRender(tile.Tile):
    def on_render(self, center, top_left, cell_size):
        arcade.draw_rectangle_outline(center.x, center.y, state.cell_size.x - 2, state.cell_size.y - 2, arcade.color.BRONZE)


window = arcade.Window(resizable=True)
window.show_view(exploration.Explore())
state.window = window
state.grid.add(TestRender(Vector(1, 0)))

arcade.run()
