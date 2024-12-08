import contextlib
import pathlib
import arcade
import pickle
import json
import shutil
from enum import Enum, auto
from W_Main_File.Essentials import State
from W_Main_File.Utilities import Seeding

"""

JSON:
universal
cannot store python as instances
- requires construction on loading to restore to instance
- requires formatting data to JSON compliant data structures (dicts, lists, tuples, ints, strings)

PICKLE:
versioning
- cannot load pickle file from a previous pickle version, or a future version


"""


class IST(Enum):
    assign_path_to_sprites = auto()
    assign_image_to_sprites = auto()
    both = auto()


# noinspection PyMethodMayBeStatic
class SavingFunctions:
    def update_most_recent_auto(self):
        maximum = 1
        for directory in self.get_auto_path().iterdir():
            try:
                maximum = max(maximum, int(directory.stem))
            except ValueError:
                continue
        State.state.current_auto_save = maximum

    def update_most_recent_official(self):
        maximum = 1
        for directory in self.get_official_path().iterdir():
            try:
                maximum = max(maximum, int(directory.stem))
            except ValueError:
                continue
        State.state.current_official_save = maximum

    def get_auto_path(self, current=False, clean=False, plus_one=False):
        m_path = pathlib.Path(f'PLAYERDATA/{State.state.player.name}/AUTOSAVES')
        if clean:
            self.format_directories()
            if len(files := [file for file in m_path.iterdir()]) > 5:
                # files = sorted(files, key=lambda x: int(str(x.stem)))
                for _ in range(2):
                    files2 = sorted(map(int, map(str, files)))
                    for index, file in enumerate(tuple(files)):
                        if int(str(file)) == files2[0]:
                            shutil.rmtree(files[index].absolute())
        if not current:
            return m_path
        else:
            self.update_most_recent_auto()
            return m_path / str(State.state.current_auto_save + (1 if plus_one else 0))

    def get_official_path(self, current=False, plus_one=False):
        m_path = pathlib.Path(f'PLAYERDATA/{State.state.player.name}/OFFICIAL')
        if not current:
            return m_path
        else:
            self.update_most_recent_official()
            return m_path / str(State.state.current_official_save + (1 if plus_one else 0))

    def format_directories(self):
        player_path = pathlib.Path(f'PLAYERDATA/{State.state.player.name}/AUTOSAVES/{State.state.current_auto_save}')
        player_path.mkdir(parents=True, exist_ok=True)
        player_path = pathlib.Path(f'PLAYERDATA/{State.state.player.name}/OFFICIALS/{State.state.current_official_save}')
        player_path.mkdir(parents=True, exist_ok=True)

    def assign_path_to_sprites(self):
        for item in State.state.player.inventory.items:
            if isinstance(item.sprite, arcade.Texture):
                item.sprite = item.sprite.name.split('-', 1)[0]
            else:
                print(item)
                raise ValueError

    def assign_image_to_sprites(self, file_path):
        with open(file_path / 'player.pickle', 'rb') as file:
            player_data = pickle.load(file)
        with open(file_path / 'inv.pickle', 'rb') as file:
            inv_data = pickle.load(file)
        for item in inv_data:
            if isinstance(item.sprite, str):
                item.sprite = arcade.load_texture(item.sprite)
            else:
                raise ValueError
        player_data['player'].inventory.items = inv_data

    def get_tile_list(self):
        tile_list = []
        for tile in State.state.grid.interactable_tiles.values():
            data = tile.persistent_data()
            data['__name__'] = tile.__class__.__name__
            tile_list.append(data)
        return tile_list

    def make_auto_save(self):
        self.format_directories()
        auto_path = self.get_auto_path(current=True)
        State.state.current_auto_save += 1
        # data = {'character_name': player.name, 'player_x': player.pos.xf, 'player_y': player.pos.yf, 'camera_x': State.state.player.camera_pos.xf, 'camera_y': State.state.player.camera_pos.yf,
        #         'hp': player.hp, 'max_hp': player.max_hp, 'gold': player.gold, 'xp': player.xp, 'lvl': player.lvl, 'floor': player.floor, 'deaths': player.deaths, 'realm': player.realm}
        floor_data = {
            'floor': State.state.player.floor,
            'seed': Seeding.world_seed,
            'tiles': self.get_tile_list(),
            'visited_tiles': State.state.grid.visited_tiles
        }
        self.assign_path_to_sprites()
        with open('PLAYERDATA/meta_data.json', 'w') as file:
            meta_data = {
                'current_auto_save': State.state.current_auto_save,
                'current_official_save': State.state.current_official_save,
            }
            json.dump(meta_data, file)
        with open((auto_path / 'player.pickle'), 'wb') as file:
            pickle.dump(State.state.player, file)
        with open((auto_path / 'inv.pickle'), 'wb') as file:
            pickle.dump(State.state.player.inventory.items, file)
        with open(auto_path / f'{State.state.player.floor}_{State.state.player.realm}.pickle', 'wb') as file:
            pickle.dump(floor_data, file)
        self.assign_image_to_sprites(auto_path)

    def make_official_save(self):
        self.make_auto_save()
        auto_path = self.get_auto_path(current=True)
        o_path = self.get_official_path(current=True, plus_one=True)
        State.state.current_official_save += 1
        shutil.copy(auto_path, o_path)

    def get_auto_save_data(self):
        self.format_directories()
        # data = {'character_name': player.name, 'player_x': player.pos.xf, 'player_y': player.pos.yf, 'camera_x': State.state.player.camera_pos.xf, 'camera_y': State.state.player.camera_pos.yf,
        #         'hp': player.hp, 'max_hp': player.max_hp, 'gold': player.gold, 'xp': player.xp, 'lvl': player.lvl, 'floor': player.floor, 'deaths': player.deaths, 'realm': player.realm}
        floor_data = {
            'floor': State.state.player.floor,
            'seed': Seeding.world_seed,
            'tiles': self.get_tile_list(),
            'visited_tiles': State.state.grid.visited_tiles
        }
        return_data = {
            'meta': '',
            'player': '',
            'inventory': '',
            'floor': '',
        }

        auto_path = self.get_auto_path(current=True)
        with open('PLAYERDATA/meta_data.json', 'w') as file:
            return_data['meta'] = json.load(file)
        with open((auto_path / 'player.pickle'), 'rb') as file:
            return_data['player'] = pickle.load(file)
        with open((auto_path / 'inv.pickle'), 'rb') as file:
            return_data['inventory'] = pickle.load(file)
        with open(auto_path / f'{State.state.player.floor}_{State.state.player.realm}.pickle', 'rb') as file:
            return_data['floor'] = pickle.load(file)
        self.assign_image_to_sprites(auto_path)
