import arcade
import pyglet
from pyglet.window import ImageMouseCursor
from W_Main_File.Essentials import State
from W_Main_File.Data import Tile, Item, HpEntity, Sprites_
from W_Main_File.Utilities import Vector
from W_Main_File.Views import Player_Select
from W_Main_File.Tiles import Home_Tile, Loot_Functions, Trapdoor_Functions


class TestRender(Tile.Tile):
    def on_render(self, center, top_left, cell_size):
        arcade.draw_rectangle_outline(center.x, center.y, State.state.cell_size.x - 2, State.state.cell_size.y - 2, arcade.color.BRONZE)


if State.state.player.floor == 1:
    State.state.grid.add(Home_Tile.HomeTile(Vector.Vector(0, 0)))
window = arcade.Window(width=1000, height=800, resizable=True, title='Adventure Mini-Game', antialiasing=False)
window.set_min_size(1000, 800)
State.state.window = window
window.show_view(Player_Select.PlayerSelect())
State.state.player.meta_data.is_me = True
State.state.grid.add(Trapdoor_Functions.TrapdoorTile(Vector.Vector(-1, 0)))
State.state.grid.add(Loot_Functions.LootTile(Vector.Vector(2, 0)))
State.state.window.set_mouse_visible(False)
# State.state.window.draw_mouse_cursor()
# cursor_image = arcade.Sprite('Sprites/Rusty_Knife_1.png')
# cursor_image = Texture(50, 50, )
# cursor_image = pyglet.resource.image('Sprites/Rusty_Knife_1.png')
# with open('Sprites/Rusty_Knife_1.png', 'rb') as file:
#     pic = pyglet.image.load('Sprites/Rusty_Knife_1.png', file=file)
# cursor = ImageMouseCursor(pic, 24, 7)
# State.state.window.set_mouse_cursor(cursor=pic)
# DOING CUSTOM MOUSE SPRITE
if __name__ == '__main__':
    arcade.run()
