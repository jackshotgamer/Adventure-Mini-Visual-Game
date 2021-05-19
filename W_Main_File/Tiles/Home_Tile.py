from W_Main_File.Essentials import State
from W_Main_File.Data import Tile, Sprites_
import arcade


class HomeTile(Tile.Tile):
    def __init__(self, pos):
        super().__init__(pos)
        self.current_opacity = 0

    @property
    def heal_cost(self):
        return max(1, int((State.state.player.max_hp - State.state.player.hp) * 0.1))

    def on_render(self, center, top_left, cell_size):
        arcade.draw_rectangle_outline(center.x, center.y, State.state.cell_size.x - 2, State.state.cell_size.y - 2, arcade.color.BRONZE)
        arcade.draw_texture_rectangle(center.x, center.y, 97, 97, Sprites_.home_sprite)

    def on_render_foreground(self, center, top_left, cell_size):
        if State.state.player.hp < State.state.player.max_hp and State.state.player.pos == self.pos:
            if State.state.is_moving:
                return
            arcade.draw_rectangle_filled(center.x, center.y, cell_size.x * 2, cell_size.y * 0.45, (0, 0, 0, self.current_opacity))
            if State.state.player.gold >= self.heal_cost:
                arcade.draw_text(f'Press E to heal to {State.state.player.max_hp} Hit Points\n        This will cost {self.heal_cost} Gold', center.x, center.y, (255, 215, 0, 220),
                                 12, anchor_x='center', anchor_y='center')
            else:
                arcade.draw_text(f'You cannot afford a full heal!\n      You need {self.heal_cost - State.state.player.gold} more gold.\n          Come back later!', center.x, center.y, (255, 69, 0, 220),
                                 12, anchor_x='center', anchor_y='center')

    def on_update(self, delta_time):
        self.current_opacity = min(200, self.current_opacity + 4)

    def on_enter(self):
        self.current_opacity = 0

    def key_down(self, keycode, mods):
        if State.state.player.hp < State.state.player.max_hp:
            if keycode == arcade.key.E:
                if State.state.player.gold >= self.heal_cost:
                    State.state.player.gold -= self.heal_cost
                    State.state.player.hp = State.state.player.max_hp
            elif keycode == arcade.key.G and State.state.player.meta_data.is_me:
                State.state.player.gold += self.heal_cost
        elif keycode == arcade.key.H and State.state.player.meta_data.is_me:
            State.state.player.hp //= 2

    def persistent_data(self):
        return {
            'pos': self.pos
        }

    @classmethod
    def load_from_data(cls, persistent_data):
        return HomeTile(persistent_data['pos'])