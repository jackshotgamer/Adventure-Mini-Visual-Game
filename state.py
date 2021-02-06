import hpentity
import vector
import metadata
import grid


class State:
    def __init__(self):
        self.player = hpentity.HpEntity('Temp', 50, vector.Vector(0, 0), metadata.MetaData(is_player=True))
        self.window = None
        self.grid = grid.Grid()
        self.cell_size = vector.Vector(100, 100)
        self.render_radius = 2

    @property
    def screen_center(self):
        return vector.Vector(self.window.width / 2, self.window.height / 2)

    @staticmethod
    def generate_radius(radius):
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                yield x, y

    @staticmethod
    def generate_edges(inner_radius):
        for x in range(~inner_radius, inner_radius + 2):
            for y in range(~inner_radius, inner_radius + 2):
                if abs(x) > inner_radius or abs(y) > inner_radius:
                    yield x, y


state = State()
