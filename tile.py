from state import state


class Tile:
    def __init__(self, pos):
        self.pos = pos

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
        return self.pos == state.player.pos
