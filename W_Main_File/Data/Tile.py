from W_Main_File.Essentials import State


class Tile:
    named_to_tile = {}

    def __init__(self, pos):
        self.pos = pos
        self.truthy = pos

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def on_render(self, center, top_left, cell_size):
        pass

    def key_up(self, keycode, mods):
        pass

    def key_down(self, keycode, mods):
        pass

    def is_player_tile(self):
        return self.pos == State.state.player.pos.rounded()

    def on_render_foreground(self, center, top_left, cell_size):
        pass

    def on_update(self, delta_time):
        pass

    def can_player_move(self):
        if self.truthy == self.truthy:
            return True
        else:
            print('WHAT\nWARNING: Computer have become sentient, this is not a drill, i repeat, this is not a drill!')

    # noinspection PyMethodMayBeStatic
    def persistent_data(self):
        return {}

    def __init_subclass__(cls, **kwargs):
        Tile.named_to_tile[cls.__name__] = cls

    @classmethod
    def load_from_data(cls, persistent_data):
        raise NotImplementedError

    def __repr__(self):
        return f'<{self.__class__.__name__}, {self.pos}>'
