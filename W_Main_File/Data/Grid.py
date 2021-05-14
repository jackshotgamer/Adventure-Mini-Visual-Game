from W_Main_File.Utilities import Vector


class Grid:
    def __init__(self):
        self.tiles = {}

    def add(self, *tiles):
        for tile_info in tiles:
            if tile_info.pos in self.tiles:
                raise ValueError('Error: Duplicate tile')
            self.tiles[tile_info.pos.tuple()] = tile_info

    def remove(self, xy: Vector.Vector):
        if xy.tuple() in self.tiles:
            del self.tiles[xy.tuple()]

    def get(self, x, y, default=None):
        return self.tiles.get((x, y), default)
