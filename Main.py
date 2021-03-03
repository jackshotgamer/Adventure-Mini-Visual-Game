import arcade
import State
import Tile
import Vector
import Player_Select
import Home_Tile
import Loot_Functions


class TestRender(Tile.Tile):
    def on_render(self, center, top_left, cell_size):
        arcade.draw_rectangle_outline(center.x, center.y, State.state.cell_size.x - 2, State.state.cell_size.y - 2, arcade.color.BRONZE)
        # arcade.draw_texture_rectangle()

    def key_down(self, keycode, mods):
        print(keycode)


State.state.grid.add(Home_Tile.HomeTile(Vector.Vector(0, 0)))
window = arcade.Window(width=1000, height=800)
State.state.window = window
window.show_view(Player_Select.PlayerSelect())
State.state.player.meta_data.is_me = True
State.state.grid.add(TestRender(Vector.Vector(1, 0)))
State.state.grid.add(Loot_Functions.LootTile(Vector.Vector(-1, 0)))

arcade.run()
