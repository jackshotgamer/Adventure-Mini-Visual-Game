from W_Main_File.Essentials import State
from W_Main_File.Utilities import Vector


class Grid:
    def __init__(self):
        self.interactable_tiles = {}
        self.visited_tiles = set()

    def add(self, *tiles):
        for tile_info in tiles:
            if tile_info.pos in self.interactable_tiles:
                raise ValueError('Error: Duplicate tile')
            self.interactable_tiles[tile_info.pos.tuple()] = tile_info

    def remove(self, xy: Vector.Vector):
        if xy.tuple() in self.interactable_tiles:
            del self.interactable_tiles[xy.tuple()]

    def get(self, x, y, default=None):
        return self.interactable_tiles.get((x, y), default)

    def add_visited_tile(self, vector):
        from W_Main_File.Essentials import State
        if (vector.x, vector.y) in self.interactable_tiles or State.state.tile_type_pos(vector.x, vector.y) == '0':
            return
        self.visited_tiles.add(vector.tuple())
