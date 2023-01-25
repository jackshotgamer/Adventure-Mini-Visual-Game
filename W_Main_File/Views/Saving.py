import arcade
from arcade import View

from W_Main_File.Utilities import Data_Saving
from W_Main_File.Essentials import State


class Saving(View):
    def __init__(self, saving_screen_func):
        super().__init__()
        self.frame_count = 1
        self.saved = False
        self.saving_screen_func = saving_screen_func

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text('Saving...', State.state.screen_center.x, State.state.screen_center.y, arcade.color.WHITE,
                         font_size=30, font_name='arial', anchor_x='center', anchor_y='center')
        State.state.render_mouse()

    def on_update(self, delta_time: float):
        self.frame_count += 1
        if self.frame_count >= 5 and not self.saved:
            Data_Saving.SaveManager.save_player_data(f'{State.state.player.name}')
            Data_Saving.SaveManager.floor_save()
            State.state.inventory.save(f'{State.state.player.name}')
            self.saved = True
        if self.frame_count >= 10 and self.saved:
            State.state.window.show_view(self.saving_screen_func())
