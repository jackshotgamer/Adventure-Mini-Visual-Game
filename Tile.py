import State


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
        return self.pos == State.state.player.pos

    def on_render_foreground(self, center, top_left, cell_size):
        pass

    def on_update(self, delta_time):
        pass
