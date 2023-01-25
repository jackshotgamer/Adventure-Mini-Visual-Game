import pathlib
import pickle
from W_Main_File.Essentials import State
from W_Main_File.Utilities import Vector, Seeding


class SaveManager:
    playerdata_path = pathlib.Path('./PLAYERDATA')

    @classmethod
    def floor_save(cls):
        name = State.state.player.name
        floor = State.state.player.floor
        seed = Seeding.world_seed
        tiles = State.state.grid.interactable_tiles.values()
        visited_tiles = State.state.grid.visited_tiles
        tile_list = []
        for x in tiles:
            tile_list.append(cls.get_tile_data(x))
        info = {
            'floor': floor,
            'seed': seed,
            'tiles': tile_list,
            'visited_tiles': visited_tiles
        }
        cls.ensure_save_directory()
        character_dir = cls.ensure_character_directory(name)
        floor_file = character_dir / f'{floor}_{State.state.player.realm}.pickle'
        with floor_file.open('wb') as file:
            pickle.dump(info, file)

    @classmethod
    def ensure_save_directory(cls):
        if cls.playerdata_path.exists():
            return
        cls.playerdata_path.mkdir()

    @classmethod
    def ensure_character_directory(cls, name):
        character_dir = cls.playerdata_path / f'{name}'
        if character_dir.exists():
            return character_dir
        character_dir.mkdir()
        return character_dir

    @staticmethod
    def get_tile_data(tile):
        data = tile.persistent_data()
        data['__name__'] = tile.__class__.__name__
        return data

    @classmethod
    def get_floor_file_path(cls, floor_number, character_name, realm='Overworld'):
        floor_file = cls.playerdata_path / f'{character_name}' / f'{floor_number}_{realm}.pickle'
        return floor_file

    @classmethod
    def load_floor(cls, floor_number, realm, force_load=False):
        character_name = State.state.player.name
        state = State.state
        if floor_number != 1:
            state.grid.remove(Vector.Vector(0, 0))
        elif not state.grid.get(0, 0):
            from W_Main_File.Tiles import Home_Tile
            state.grid.add(Home_Tile.HomeTile(Vector.Vector(0, 0)))
        if state.player.floor == floor_number and not force_load:
            return
        cls.ensure_save_directory()
        floor_file_path = cls.get_floor_file_path(floor_number, character_name, realm)
        State.state.grid.visited_tiles.clear()
        State.state.texture_mapping.clear()
        if not floor_file_path.exists():
            return False
        with open(floor_file_path, 'rb') as floor_file:
            import pickle
            data = pickle.load(floor_file)
        State.state.grid.visited_tiles = data['visited_tiles']
        Seeding.world_seed = data['seed']
        state.grid.interactable_tiles.clear()
        for tile in data['tiles']:
            from W_Main_File.Data import Tile
            class_name = tile['__name__']
            class_obj = Tile.Tile.named_to_tile[class_name]
            final_tile = class_obj.load_from_data(tile)
            state.grid.add(final_tile)
        return True

    @classmethod
    def save_player_data(cls, file_path):
        player = State.state.player
        data = {'character_name': player.name, 'player_x': player.pos.xf, 'player_y': player.pos.yf, 'camera_x': State.state.camera_pos.xf, 'camera_y': State.state.camera_pos.yf,
                'hp': player.hp, 'max_hp': player.max_hp, 'gold': player.gold, 'xp': player.xp, 'lvl': player.lvl, 'floor': player.floor, 'deaths': player.deaths, 'realm': player.realm}
        from W_Main_File.Essentials.State import state
        cls.ensure_save_directory()
        if not (state.player_data_path / file_path).exists():
            (state.player_data_path / file_path).mkdir()
        import pickle
        with open((state.player_data_path / file_path / 'player.pickle'), 'wb') as file:
            pickle.dump(data, file)

    @classmethod
    def load_player_data(cls, file_path):
        from W_Main_File.Essentials.State import state
        import pickle
        cls.ensure_save_directory()
        if not (state.player_data_path / file_path).exists():
            (state.player_data_path / file_path).mkdir()
        if not (state.player_data_path / file_path / 'player.pickle').exists():
            with open((state.player_data_path / file_path / 'player.pickle'), 'wb') as file:
                pickle.dump({'character_name': file_path, 'player_x': 0, 'player_y': 0, 'camera_x': 0, 'camera_y': 0, 'hp': 1000, 'max_hp': 1000,
                             'gold': 0, 'xp': 0, 'lvl': 1, 'floor': 1, 'deaths': 0, 'realm': 'Overworld'}, file)
        with open((state.player_data_path / file_path / 'player.pickle'), 'rb') as file:
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
        State.state.change_realm(data['realm'])
