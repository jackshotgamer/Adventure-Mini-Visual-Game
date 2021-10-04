from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from W_Main_File.Data import Item
from typing import Union
from W_Main_File.Essentials import State


class InventoryContainer:
    def __init__(self, page_size=25):
        self.items = []
        self.page_size = page_size

    def remove_empty_pages(self):
        pass

    @property
    def page_count(self):
        return (len(self.items) // State.state.inventory.page_size) + (1 if (len(self.items) / State.state.inventory.page_size) % 1 else 0)

    def add_item(self, item: 'Item'):
        for index, item1 in enumerate(self.items):
            if item1 is None:
                self.items[index] = item
                return
        self.items.append(item)
        print(f'added, item: {item}')

    def remove_item(self, index: int, page_num: int = None):
        if self.items:
            if page_num is not None:
                index1 = index + (page_num * self.page_size)
            else:
                index1 = index
            if 0 <= index1 < len(self.items):
                self.items[index1] = None

    def count_items(self, id_):
        if isinstance(id_, str):
            if self.items:
                matching_items = 0
                for item in self.items:
                    if item is not None:
                        if id_ == item.id_:
                            matching_items += 1
                return matching_items

    def get_item(self, index, page_num=None):
        if isinstance(index, int):
            if self.items:
                if page_num is None:
                    if 0 <= index < len(self.items):
                        return self.items[index]
                else:
                    if 0 <= index < len(self.items):
                        if index < self.page_size:
                            index1 = index + (page_num * self.page_size)
                        else:
                            index1 = index
                        if 0 <= index1 < len(self.items):
                            return self.items[index1]

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
        print('hi')
