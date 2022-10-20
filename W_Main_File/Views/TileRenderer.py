import time
import pyglet
import arcade
import arcade.gui
from W_Main_File.Data import Sprites_
from W_Main_File.Data.Sprites_ import texture_to_sprite
from W_Main_File.Essentials import State
from W_Main_File.Utilities import Vector, Button_Functions
from W_Main_File.Views import Event_Base


class TileRenderer:
    def __init__(self, render_radius):
        self.render_radius = render_radius
        State.cache_state.last_values = [State.state.camera_pos, State.state.render_radius, State.state.cell_size]
        self.first_render = True

    def get_tiles_in_render_range(self, grid):
        tile_pos = set()
        center = State.state.screen_center
        from W_Main_File.Tiles import Trap_Functions
        for offset in State.state.generate_radius(self.render_radius):
            if isinstance(grid.get(*(State.state.player.pos.rounded() + offset)), Trap_Functions.TrapTile):
                pass
                # print(f'Trap pos: {State.state.player.pos.rounded() + offset}')
            tile_pos.add((State.state.player.pos.rounded() + offset))
        return [
            (tile, ((pos * State.state.cell_render_size) + center) - State.state.camera_pos)
            for pos in tile_pos if (tile := grid.get(*pos))
        ]

    def on_draw(self, render_rad=None):
        render_radius = render_rad or self.render_radius
        center = State.state.screen_center
        # todo: fix not generating new sprites
        var = ((State.state.grid_camera_pos * State.state.cell_render_size) - State.state.camera_pos)
        if State.cache_state.last_values != [State.state.camera_pos, State.state.render_radius, State.state.cell_size] or self.first_render:
            State.cache_state.tile_cache = arcade.SpriteList()
            for offset in State.state.generate_radius(render_radius):
                real_grid_pos = State.state.grid_camera_pos + offset
                render_pos = (center + (State.state.cell_render_size * offset)) + var
                temp_sprite = texture_to_sprite(State.state.tile_type_pos(*real_grid_pos), State.state.cell_render_size.xf, State.state.cell_render_size.yf)
                temp_sprite.position = render_pos
                State.cache_state.tile_cache.append(temp_sprite)
                offset1 = Vector.Vector(*render_pos/100)
            State.cache_state.last_values = [State.state.camera_pos, State.state.render_radius, State.state.cell_size]
            self.first_render = False
        State.cache_state.tile_cache.draw(filter=pyglet.gl.GL_NEAREST)

    def on_draw_tile(self, grid=None):
        grid = grid or State.state.grid
        for tile, pos in self.get_tiles_in_render_range(grid):
            tile.on_render(pos, pos + (-(State.state.cell_render_size.xf / 2), State.state.cell_render_size.yf / 2), State.state.cell_render_size)

    def on_draw_foreground(self, grid=None):
        grid = grid or State.state.grid
        for tile, pos in self.get_tiles_in_render_range(grid):
            if State.state.debug_mode:
                arcade.draw_point(pos.x, pos.y, arcade.color.BLUE if tile.__class__.__name__ == 'TrapTile' else arcade.color.GOLD, 9)
            tile.on_render_foreground(pos, pos + (-(State.state.cell_render_size.xf / 2), State.state.cell_render_size.yf / 2), State.state.cell_render_size)
