from W_Main_File.Data import Item
from typing import Union
from W_Main_File.Essentials import State


class InventoryContainer:
    def __init__(self):
        self.items = []

    def add_item(self, item: Item):
        self.items.append(item)
        print(f'added, item: {item}')
        if State.state.player.meta_data.is_player and not State.state.player.meta_data.is_guest:
            self.save(f'{State.state.player.name}')

    def remove_item(self, item: Union[Item.Item, int, str]):
        if isinstance(item, Item.Item):
            if item in self.items:
                self.items.remove(item)
        elif isinstance(item, str):
            if self.items:
                for item1 in self.items:
                    if item == item1.id_:
                        break
                else:
                    return
                self.items.remove(item1)
        elif isinstance(item, int):
            if self.items:
                if 0 <= item < len(self.items):
                    del self.items[item]
        if State.state.player.meta_data.is_player and not State.state.player.meta_data.is_guest:
            self.save(f'{State.state.player.name}')

    def get_item(self, index_or_id):
        if isinstance(index_or_id, str):
            if self.items:
                for item in self.items:
                    if index_or_id == item.id_:
                        return item
        elif isinstance(index_or_id, int):
            if self.items:
                if 0 <= index_or_id < len(self.items):
                    return self.items[index_or_id]

    def load(self, file_path):
        import pathlib
        import pickle
        if not pathlib.Path(f'Inventory_Contents/{file_path}').exists():
            with open(f'Inventory_Contents/{file_path}', 'wb') as file:
                pickle.dump([], file)
        with open(f'Inventory_Contents/{file_path}', 'rb') as file:
            self.items = pickle.load(file)

    def save(self, file_path):
        import pathlib
        import pickle
        if not pathlib.Path('Inventory_Contents').exists():
            pathlib.Path('Inventory_Contents').mkdir()
        with open(f'Inventory_Contents/{file_path}', 'wb') as file:
            pickle.dump(self.items, file)
