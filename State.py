import HpEntity
import Vector
import Meta_Data
import Grid


class State:
    def __init__(self):
        self.player = HpEntity.HpEntity('Temp', 50, Vector.Vector(0, 0), Meta_Data.MetaData(is_player=True))
        self.window = None
        self.grid = Grid.Grid()
        self.cell_size = Vector.Vector(100, 100)
        self.render_radius = 2

    @property
    def screen_center(self):
        return Vector.Vector(self.window.width / 2, self.window.height / 2)

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
