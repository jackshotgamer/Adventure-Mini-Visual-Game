import pathlib
import pickle
from W_Main_File.Essentials import State


class FloorSaveManager:
    interactable_tiles = pathlib.Path('./Interactable_Tiles')

    def floor_save(self, name, floor, seed, tiles):
        info = {
            'floor': floor,
            'seed': seed,
            'tiles': tiles
        }
        self.ensure_save_directory()
        character_dir = self.ensure_character_directory(name)
        floor_file = character_dir / f'{floor}.pickle'
        with floor_file.open('wb') as file:
            pickle.dump(info, file)

    def ensure_save_directory(self):
        if self.interactable_tiles.exists():
            return
        self.interactable_tiles.mkdir()

    def ensure_character_directory(self, name):
        character_dir = self.interactable_tiles / f'{name}'
        if character_dir.exists():
            return character_dir
        character_dir.mkdir()
        return character_dir
