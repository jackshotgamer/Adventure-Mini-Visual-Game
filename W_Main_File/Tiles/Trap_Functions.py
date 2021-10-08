import arcade, random

from W_Main_File.Data import Tile, Sprites_
from W_Main_File.Essentials import State


class TrapTile(Tile.Tile):
    def __init__(self, pos):
        super().__init__(pos)
        self.playing_alert = False
        self.finished_alert = False
        self.at_full_opacity = False
        self.alpha = 0
        self.goal_hp = None
        self.frame_count = 0
        self.width = 100
        self.height = 100

    def on_render_foreground(self, center, top_left, cell_size):
        if State.state.player.pos == self.pos and self.playing_alert:
            if State.state.is_moving:
                return
            from W_Main_File.Utilities import Inventory_GUI
            if Inventory_GUI.is_inv():
                return
            arcade.draw_texture_rectangle(center.x, (center.y + 100), self.width, self.height, Sprites_.trap_alert, alpha=self.alpha)

    def on_enter(self):
        State.state.preoccupied = True
        self.playing_alert = True
        subtract_amount = (int(State.state.player.max_hp * random.uniform(0.15, 0.25)) if
                           (State.state.player.hp / State.state.player.max_hp) >= 0.4 else
                           int(State.state.player.max_hp * random.uniform(0.05, 0.15)))
        # noinspection PyAttributeOutsideInit
        self.goal_hp = State.state.player.hp - subtract_amount
        print(self.goal_hp)

    def on_update(self, delta_time):
        from W_Main_File.Utilities import Inventory_GUI
        if Inventory_GUI.is_inv():
            return
        if self.goal_hp is None:
            return
        if self.finished_alert:
            self.finished_alert = False
            self.at_full_opacity = False
            self.alpha = 0
            State.state.preoccupied = False
            return
        if not self.at_full_opacity:
            self.alpha = min(255, self.alpha + 10)
            if self.alpha == 255:
                self.at_full_opacity = True
        if self.at_full_opacity:
            self.frame_count += 1
            if not self.frame_count % 2:
                if State.state.player.hp > 0:
                    State.state.player.hp = max(0, max(self.goal_hp, State.state.player.hp - 3))
            if not self.frame_count % 8:
                if self.width == 100:
                    self.width = random.randint(90, 92)
                elif self.width in (90, 91, 92):
                    self.width = 100
                if self.height == 100:
                    self.height = random.randint(90, 92)
                elif self.height in (90, 91, 92):
                    self.height = 100
                if not State.state.player.hp > self.goal_hp or not State.state.player.hp > 0:
                    self.finished_alert = True
                    self.playing_alert = False
                    self.frame_count = 0

    def on_exit(self):
        self.goal_hp = None

    def persistent_data(self):
        return {
            'pos': self.pos
        }

    @classmethod
    def load_from_data(cls, persistent_data):
        tile = TrapTile(persistent_data['pos'])
        return tile
