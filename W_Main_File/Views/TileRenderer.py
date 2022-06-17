import time

import arcade
import arcade.gui
from W_Main_File.Data import Sprites_
from W_Main_File.Essentials import State
from W_Main_File.Utilities import Vector, Button_Functions
from W_Main_File.Views import Event_Base


class TileRenderer:
    def __init__(self, render_radius):
        self.render_radius = render_radius

    def get_tiles_in_render_range(self, grid):
        tile_pos = set()
        center = State.state.screen_center
        for offset in State.state.generate_radius(self.render_radius):
            tile_pos.add(State.state.grid_camera_pos + offset)
        return [
            (tile, ((pos - (State.state.grid_camera_pos_raw - pos)) * State.state.cell_render_size) + center)
            for pos in tile_pos if (tile := grid.get(*pos))
        ]

    def on_draw(self, render_rad=None):
        render_radius = render_rad or self.render_radius
        center = State.state.screen_center
        # todo: fix not generating new sprites

        var = ((State.state.grid_camera_pos * State.state.cell_render_size) - State.state.camera_pos)
        for offset in State.state.generate_radius(render_radius):
            real_grid_pos = State.state.grid_camera_pos + offset
            render_pos = (center + (State.state.cell_render_size * offset)) + var
            arcade.draw_texture_rectangle(render_pos.xf, render_pos.yf,
                                          State.state.cell_render_size.x, State.state.cell_render_size.y, State.state.tile_type_pos(*real_grid_pos))

    def on_draw_tile(self, grid=None):
        grid = grid or State.state.grid
        for tile, pos in self.get_tiles_in_render_range(grid):
            tile.on_render(pos, pos + (-(State.state.cell_render_size.xf / 2), State.state.cell_render_size.yf / 2), State.state.cell_render_size)

    def on_draw_foreground(self, grid=None):
        grid = grid or State.state.grid
        for tile, pos in self.get_tiles_in_render_range(grid):
            tile.on_render_foreground(pos, pos + (-(State.state.cell_render_size.xf / 2), State.state.cell_render_size.yf / 2), State.state.cell_render_size)
