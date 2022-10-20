import arcade
from W_Main_File.Essentials import State
from W_Main_File.Data import Sprites_
from W_Main_File.Utilities import Vector
from W_Main_File.Views import Player_Select
from W_Main_File.Tiles import Home_Tile, Loot_Functions, Trapdoor_Functions

State.state.window = arcade.Window(width=1000, height=800, resizable=True, title='Adventure Mini-Game', antialiasing=False)
State.state.window.set_min_size(1000, 800)
if State.state.player.floor == 1:
    State.state.grid.add(Home_Tile.HomeTile(Vector.Vector(0, 0)))
State.state.window.ctx.BLEND_DEFAULT = State.state.window.ctx.BLEND_DEFAULT
State.state.window.center_window()
State.state.window.show_view(Player_Select.PlayerSelect())
State.state.player.meta_data.is_me = True
State.state.grid.add(Trapdoor_Functions.TrapdoorTile(Vector.Vector(-1, 0)))
State.state.grid.add(Loot_Functions.LootTile(Vector.Vector(2, 0)))
State.state.window.set_mouse_visible(False)
Sprites_.renew_cropped_backdrop()
if __name__ == '__main__':
    arcade.run()
