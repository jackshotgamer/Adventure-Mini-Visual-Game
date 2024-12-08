from W_Main_File.Essentials import State
from W_Main_File.Data import Tile, Sprites_
import arcade


class VillageTile(Tile.Tile):
    def __init__(self, pos):
        super().__init__(pos)
        self.current_opacity = 0

    @property
    def heal_potion_cost(self):
        return 25

    def on_render_foreground(self, center, top_left, cell_size):
        if State.state.player.pos.rounded() == self.pos:
            from W_Main_File.Utilities import Inventory_GUI
            if Inventory_GUI.is_inv():
                return
            if State.state.is_moving:
                return
            arcade.draw_rectangle_filled(center.x, center.y, cell_size.x * 2.1, cell_size.y * 0.45, (0, 0, 0, self.current_opacity))
            if State.state.player.gold >= self.heal_potion_cost:
                arcade.draw_text(f'Press E to purchase a health potion\nThis will cost {self.heal_potion_cost} Gold', center.x, center.y, (255, 215, 0, 220),
                                 12, anchor_x='center', anchor_y='center', align='center')
            else:
                arcade.draw_text(f'You cannot afford a health potion!\nYou need {self.heal_potion_cost - State.state.player.gold} more gold.\nCome back later!', center.x, center.y, (255, 69, 0, 220),
                                 12, anchor_x='center', anchor_y='center', align='center')

    def on_update(self, delta_time):
        from W_Main_File.Utilities import Inventory_GUI
        if Inventory_GUI.is_inv():
            return
        self.current_opacity = min(200, self.current_opacity + 4)

    def on_enter(self):
        self.current_opacity = 0

    def key_down(self, keycode, mods):
        from W_Main_File.Utilities import Inventory_GUI
        if Inventory_GUI.is_inv():
            return
        if keycode == arcade.key.E:
            if State.state.player.gold >= self.heal_potion_cost:
                State.state.player.gold -= self.heal_potion_cost
                State.state.player.inventory.add_item(Sprites_.item_dict['health_potion']())

    def persistent_data(self):
        return {
            'pos': self.pos
        }

    @classmethod
    def load_from_data(cls, persistent_data):
        return VillageTile(persistent_data['pos'])
