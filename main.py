import arcade
from views import exploration
import state
import tile
import vector


class TestRender(tile.Tile):
    def on_render(self, center, top_left, cell_size):
        arcade.draw_rectangle_outline(center.x, center.y, state.state.cell_size.x - 2, state.state.cell_size.y - 2, arcade.color.BRONZE)


window = arcade.Window(resizable=True)
window.show_view(exploration.Explore())
state.state.window = window
state.state.grid.add(TestRender(vector.Vector(1, 0)))

arcade.run()
