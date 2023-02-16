from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from W_Main_File.Data import Item
from typing import Union
from W_Main_File.Essentials import State
from W_Main_File.Utilities import Data_Saving
from pathlib import Path
import pickle



class InventoryContainer:
    def __init__(self, page_size=25):
        self.items = []
        self.page_size = page_size

    @property
    def page_count(self):
        return (len(self.items) // self.page_size) + (1 if (len(self.items) / self.page_size) % 1 else 0)

    @staticmethod
    def get_absolute_index(index, page_num=None):
        if page_num is None:
            page_num = State.state.current_page
        return index+(page_num*25)

    def add_item(self, item: 'Item'):
        for index, item1 in enumerate(self.items):
            if item1 is None:
                self.items[index] = item
                return
        self.items.append(item)
        if State.state.debug_mode:
            print(f'added, item: {item}')

    def remove_item(self, index: int, page_num: int = None, checks=True):
        if self.items:
            if page_num is not None:
                index1 = index + (page_num * self.page_size)
            else:
                index1 = index
            if 0 <= index1 < len(self.items):
                self.items[index1] = None
                if checks:
                    self.clear_empty_pages()
                    self.trim_inventory()

    def remove_item_not_index(self, item, checks=True):
        if self.items:
            if item in self.items:
                index = self.items.index(item)
                self.items[index] = None
                if checks:
                    self.clear_empty_pages()
                    self.trim_inventory()

    def remove_mass_items(self, indexes, checks=True):
        for index in indexes:
            self.remove_item(index, State.state.current_page, checks=checks)
        if checks:
            self.clear_empty_pages()
            self.trim_inventory(False)
        for item in self.items:
            if item is not None:
                item.selected = False
        if State.cache_state.selected_list:
            del State.cache_state.selected_list

    def sort_inventory(self):
        self.items.sort(key=lambda x: (x.type_.value, x.name.casefold()))

    def trim_inventory(self, remove_all=False):
        items_removed = 0
        items_length = len(self.items)
        for index, item in reversed(list(enumerate(self.items))):
            if item is None:
                del self.items[index]
                items_removed += 1
            elif remove_all:
                continue
            else:
                break
        if State.state.current_page >= self.page_count:
            if State.state.current_page != 0:
                State.state.current_page = self.page_count - 1

    def clear_empty_pages(self):
        for page_num in reversed(range(self.page_count)):
            if not any(self.get_items_on_page(page_num)):
                if page_num == self.page_count-1:
                    for index in reversed(range(page_num*25, (page_num*25)+(len(self.get_items_on_page(page_num))))):
                        del self.items[index]
                else:
                    for index in reversed(range(page_num*25, (page_num*25)+25)):
                        del self.items[index]

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
                    else:
                        return None

    def get_items_on_page(self, page_num=None):
        if page_num is None:
            page_num = State.state.current_page
        if not isinstance(page_num, int) or not self.items or page_num > self.page_count:
            return []
        lower_upper_bound = [(page_num * 25), (page_num * 25) + 25]
        if lower_upper_bound[1] > len(self.items) - 1:
            lower_upper_bound[1] = len(self.items) - 1
        items_to_return = []
        for index in range(lower_upper_bound[0], lower_upper_bound[1]):
            items_to_return.append(self.items[index])
        return items_to_return

    def get_items_and_indexes_on_page(self, page_num=None):
        if page_num is None:
            page_num = State.state.current_page
        if not isinstance(page_num, int) or not self.items or page_num > self.page_count:
            return []
        lower_upper_bound = [(page_num * 25), (page_num * 25) + 25]
        if lower_upper_bound[1] > len(self.items) - 1:
            lower_upper_bound[1] = len(self.items) - 1
        items_to_return = []
        for index in range(lower_upper_bound[0], lower_upper_bound[1]+1):
            items_to_return.append((self.items[index], index))
        return items_to_return

    def load(self, file_path):
        from W_Main_File.Essentials.State import state
        if not (state.player_data_path / file_path).exists():
            (state.player_data_path / file_path).mkdir()
        if not (state.player_data_path / file_path / 'inv.pickle').exists():
            with open((state.player_data_path / file_path / 'inv.pickle'), 'wb') as file:
                pickle.dump([], file)
        with open((state.player_data_path / file_path / 'inv.pickle'), 'rb') as file:
            self.items = pickle.load(file)
        print(f'loading 1 (inv): {[x.sprite for x in self.items]}')
        with Data_Saving.SaveManager.inventory_save_manager(file_path, self.items, player_or_inv='inv'):
            pass
        print(f'loading 2 (inv): {[x.sprite for x in self.items]}')

    def save(self, file_path):
        from W_Main_File.Essentials.State import state
        if not (state.player_data_path / file_path).exists():
            (state.player_data_path / file_path).mkdir()
        with Data_Saving.SaveManager.inventory_save_manager(file_path, player_or_inv='inv'):
            with open((state.player_data_path / file_path / 'inv.pickle'), 'wb') as file:
                pickle.dump(self.items, file)
