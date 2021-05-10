import arcade
from W_Main_File.Essentials import State
from W_Main_File.Data import Tile
from W_Main_File.Utilities import Vector
from W_Main_File.Views import Player_Select
from W_Main_File.Tiles import Home_Tile, Loot_Functions, Trapdoor_Functions


class TestRender(Tile.Tile):
    def on_render(self, center, top_left, cell_size):
        arcade.draw_rectangle_outline(center.x, center.y, State.state.cell_size.x - 2, State.state.cell_size.y - 2, arcade.color.BRONZE)
        # arcade.draw_texture_rectangle()

    def key_down(self, keycode, mods):
        print(keycode)


if State.state.player.floor == 1:
    State.state.grid.add(Home_Tile.HomeTile(Vector.Vector(0, 0)))
window = arcade.Window(width=1000, height=800)
State.state.window = window
window.show_view(Player_Select.PlayerSelect())
State.state.player.meta_data.is_me = True
# State.state.grid.add(TestRender(Vector.Vector(1, 0)))
State.state.grid.add(Trapdoor_Functions.TrapdoorTile(Vector.Vector(-1, 0)))
State.state.grid.add(Loot_Functions.LootTile(Vector.Vector(2, 0)))

if __name__ == '__main__':
    arcade.run()
