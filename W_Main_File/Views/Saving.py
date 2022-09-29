import arcade
from arcade import View

from W_Main_File.Utilities import Networking, Floor_Data_Saving, Seeding
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
            save_player_data(f'{State.state.player.name}')
            Floor_Data_Saving.FloorSaveManager.floor_save()
            State.state.inventory.save(f'{State.state.player.name}')
            self.saved = True
        if self.frame_count >= 10 and self.saved:
            State.state.window.show_view(self.saving_screen_func())


def save_player_data(file_path):
    player = State.state.player
    data = {'character_name': player.name, 'player_x': player.pos.x.rounded(), 'player_y': player.pos.y.rounded(), 'camera_x': State.state.camera_pos.x, 'camera_y': State.state.camera_pos.y,
            'hp': player.hp, 'max_hp': player.max_hp, 'gold': player.gold, 'xp': player.xp, 'lvl': player.lvl, 'floor': player.floor, 'deaths': player.deaths}
    from W_Main_File.Essentials.State import state
    if not (state.player_data_path / file_path).exists():
        (state.player_data_path / file_path).mkdir()
    import pickle
    with open((state.player_data_path / file_path / 'player'), 'wb') as file:
        pickle.dump(data, file)


def load_player_data(file_path):
    from W_Main_File.Essentials.State import state
    import pickle
    if not (state.player_data_path / file_path).exists():
        (state.player_data_path / file_path).mkdir()
    if not (state.player_data_path / file_path / 'player').exists():
        with open((state.player_data_path / file_path / 'player'), 'wb') as file:
            pickle.dump({'character_name': file_path, 'player_x': 0, 'player_y': 0, 'camera_x': 0, 'camera_y': 0, 'hp': 1000, 'max_hp': 1000,
                         'gold': 0, 'xp': 0, 'lvl': 1, 'floor': 1, 'deaths': 0}, file)
    with open((state.player_data_path / file_path / 'player'), 'rb') as file:
        data = pickle.load(file)
    from W_Main_File.Utilities import Vector
    State.state.player.name = data['character_name']
    State.state.player.pos = Vector.Vector(data['player_x'], data['player_y'])
    State.state.camera_pos = Vector.Vector(data['camera_x'], data['camera_y'])
    State.state.player.hp = data['hp']
    State.state.player.max_hp = data['max_hp']
    State.state.player.gold = data['gold']
    State.state.player.xp = data['xp']
    State.state.player.lvl = data['lvl']
    State.state.player.floor = data['floor']
    State.state.player.deaths = data['deaths']
