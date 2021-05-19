import pathlib
import pickle
from W_Main_File.Essentials import State
from W_Main_File.Utilities import Vector, Seeding


class FloorSaveManager:
    interactable_tiles = pathlib.Path('./Interactable_Tiles')

    @classmethod
    def floor_save(cls):
        name = State.state.player.name
        floor = State.state.player.floor
        seed = Seeding.world_seed
        tiles = State.state.grid.tiles.values()
        tile_list = []
        for x in tiles:
            tile_list.append(cls.get_tile_data(x))
        info = {
            'floor': floor,
            'seed': seed,
            'tiles': tile_list
        }
        cls.ensure_save_directory()
        character_dir = cls.ensure_character_directory(name)
        floor_file = character_dir / f'{floor}.pickle'
        with floor_file.open('wb') as file:
            pickle.dump(info, file)

    @classmethod
    def ensure_save_directory(cls):
        if cls.interactable_tiles.exists():
            return
        cls.interactable_tiles.mkdir()

    @classmethod
    def ensure_character_directory(cls, name):
        character_dir = cls.interactable_tiles / f'{name}'
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
    def get_floor_file_path(cls, floor_number, character_name):
        floor_file = cls.interactable_tiles / f'{character_name}' / f'{floor_number}.pickle'
        return floor_file

    @classmethod
    def load_floor(cls, floor_number, force_load=False):
        character_name = State.state.player.name
        state = State.state
        if floor_number != 1:
            state.grid.remove(Vector.Vector(0, 0))
        elif not state.grid.get(0, 0):
            from W_Main_File.Tiles import Home_Tile
            state.grid.add(Home_Tile.HomeTile(Vector.Vector(0, 0)))
        if state.player.floor == floor_number and not force_load:
            return
        floor_file_path = cls.get_floor_file_path(floor_number, character_name)
        if not floor_file_path.exists():
            return False
        with open(floor_file_path, 'rb') as floor_file:
            import pickle
            data = pickle.load(floor_file)
        Seeding.world_seed = data['seed']
        state.grid.tiles.clear()
        for tile in data['tiles']:
            from W_Main_File.Data import Tile
            class_name = tile['__name__']
            class_obj = Tile.Tile.named_to_tile[class_name]
            final_tile = class_obj.load_from_data(tile)
            state.grid.add(final_tile)
        return True
