import arcade

from W_Main_File.Data import Tile, Sprites_
from W_Main_File.Essentials import State


class TrapTile(Tile.Tile):
    def __init__(self, pos):
        super().__init__(pos)
        self.playing_alert = False
        self.finished_alert = False
        self.at_full_opacity = False
        self.alpha = 0
        self.frame_count = 0
        self.width = 100
        self.height = 100

    def on_render_foreground(self, center, top_left, cell_size):
        if State.state.player.pos == self.pos and self.playing_alert:
            if State.state.is_moving:
                return
            arcade.draw_texture_rectangle(center.x, (center.y + 100), self.width, self.height, Sprites_.trap_alert, alpha=self.alpha)

    def on_enter(self):
        State.state.preoccupied = True
        self.playing_alert = True
        subtract_amount = (int(State.state.player.max_hp * 0.2) if (State.state.player.hp / State.state.player.max_hp) >= 0.4 else int(State.state.player.max_hp * 0.1))
        # noinspection PyAttributeOutsideInit
        self.goal_hp = State.state.player.hp - subtract_amount

    def on_update(self, delta_time):
        if self.finished_alert:
            self.finished_alert = False
            self.at_full_opacity = False
            State.state.preoccupied = False
            return
        if not self.at_full_opacity:
            self.alpha = min(255, self.alpha + 6)
            if self.alpha == 255:
                self.at_full_opacity = True
        if self.at_full_opacity:
            self.frame_count += 1
            if not self.frame_count % 1:
                if State.state.player.hp > 0:
                    State.state.player.hp = max(self.goal_hp, State.state.player.hp - 1)
                if not self.frame_count % 10:
                    if self.width == 100:
                        self.width = 95
                    elif self.width == 95:
                        self.width = 100
                    if self.height == 100:
                        self.height = 95
                    elif self.height == 95:
                        self.height = 100
                    if not State.state.player.hp > self.goal_hp or not State.state.player.hp > 0:
                        self.finished_alert = True
                        self.playing_alert = False
                        self.frame_count = 0

    def persistent_data(self):
        return {
            'pos': self.pos
        }

    @classmethod
    def load_from_data(cls, persistent_data):
        tile = TrapTile(persistent_data['pos'])
        return tile
