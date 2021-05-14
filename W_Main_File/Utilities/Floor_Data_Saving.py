import pathlib
import pickle
from W_Main_File.Essentials import State


class FloorSaveManager:
    interactable_tiles = pathlib.Path('./Interactable_Tiles')

    @classmethod
    def floor_save(cls, name, floor, seed, tiles):
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
