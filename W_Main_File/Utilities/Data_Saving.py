import contextlib
import pathlib
import pickle
import arcade
from W_Main_File.Essentials import State
from W_Main_File.Utilities import Vector, Seeding
from W_Main_File.Data import HpEntity
from enum import Enum, auto


class IST(Enum):
    assign_path_to_sprites = auto()
    assign_image_to_sprites = auto()
    both = auto()


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

    @staticmethod
    @contextlib.contextmanager
    def inventory_save_manager(file_path, data=None, tasks: IST = IST.both, player_or_inv='player'):
        if tasks is IST.both or tasks is IST.assign_path_to_sprites:
            for item in State.state.player.inventory.items:
                if isinstance(item.sprite, arcade.Texture):
                    item.sprite = item.sprite.name.split('-', 1)[0]
                elif isinstance(item.sprite, str):
                    item.sprite = item.sprite
                else:
                    print(item.sprite)
                    raise AttributeError

        yield

        if tasks is IST.both or tasks is IST.assign_image_to_sprites:
            if data is None:
                with open((State.state.player_data_path / file_path / f'{player_or_inv}.pickle'), 'rb') as file:
                    data = pickle.load(file)
            from arcade import load_texture
            if player_or_inv == 'player':
                for item in data['player'].inventory.items:
                    # noinspection PyTypeChecker
                    if isinstance(item.sprite, str):
                        item.sprite = load_texture(item.sprite)
                    else:
                        raise ValueError
            elif player_or_inv == 'inv':
                for item in data:
                    if isinstance(item.sprite, str):
                        item.sprite = load_texture(item.sprite)
                    else:
                        raise ValueError
            else:
                raise ValueError

    @classmethod
    def save_player_data(cls, file_path):
        player = State.state.player
        # data = {'character_name': player.name, 'player_x': player.pos.xf, 'player_y': player.pos.yf, 'camera_x': State.state.player.camera_pos.xf, 'camera_y': State.state.player.camera_pos.yf,
        #         'hp': player.hp, 'max_hp': player.max_hp, 'gold': player.gold, 'xp': player.xp, 'lvl': player.lvl, 'floor': player.floor, 'deaths': player.deaths, 'realm': player.realm}
        with cls.inventory_save_manager(file_path, player_or_inv='player'):
            data = {'player': player}
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
                # pickle.dump({'character_name': file_path, 'player_x': 0, 'player_y': 0, 'camera_x': 0, 'camera_y': 0, 'hp': 1000, 'max_hp': 1000,
                #              'gold': 0, 'xp': 0, 'lvl': 1, 'floor': 1, 'deaths': 0, 'realm': 'Overworld'}, file)
                pickle.dump({'player': HpEntity.PlayerEntity(file_path, Vector.Vector(0, 0), 1000, 1000, 0, 0, 1, 1)}, file)
        with open((state.player_data_path / file_path / 'player.pickle'), 'rb') as file:
            data = pickle.load(file)
        print(f'loading 1 (data): {[x.sprite for x in data["player"].inventory.items]}')
        with cls.inventory_save_manager(file_path, data, tasks=IST.assign_image_to_sprites, player_or_inv='player'):
            pass
        print(f'loading 2 (data): {[x.sprite for x in data["player"].inventory.items]}')
        State.state.player = data['player']
        State.state.change_realm(State.state.player.realm)
