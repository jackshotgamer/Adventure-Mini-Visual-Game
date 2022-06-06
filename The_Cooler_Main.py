# from W_Main_File.Data import Item
# from typing import Union
# from W_Main_File.Essentials import State
#
#
# class InventoryContainer:
#     def __init__(self, page_size=25):
#         self.items = []
#         self.page_size = page_size
#
#     def add_item(self, item: Item):
#         for index, item1 in enumerate(self.items):
#             if item1 is None:
#                 self.items[index] = item
#                 return
#         self.items.append(item)
#         print(f'added, item: {item}')
#
#     def remove_item(self, index: int, page_num: int = None):
#         if self.items:
#             if page_num is not None:
#                 index1 = index + (page_num * self.page_size)
#             else:
#                 index1 = index
#             if 0 <= index1 < len(self.items):
#                 self.items[index1] = None
#
#     def count_items(self, id_):
#         if isinstance(id_, str):
#             if self.items:
#                 matching_items = 0
#                 for item in self.items:
#                     if item is not None:
#                         if id_ == item.id_:
#                             matching_items += 1
#                 return matching_items
#
#     def get_item(self, index, page_num=None):
#         if isinstance(index, int):
#             if self.items:
#                 if page_num is None:
#                     if 0 <= index < len(self.items):
#                         return self.items[index]
#                 else:
#                     if 0 <= index < len(self.items):
#                         if index < self.page_size:
#                             index1 = index + (page_num * self.page_size)
#                         else:
#                             index1 = index
#                         return self.items[index1]
#
#
# i = InventoryContainer()
# from W_Main_File.Items.All_Items import rusty_knife, null_weapon_2, null_weapon_1
# for _ in range(0, 24):
#     i.add_item(rusty_knife)
#     i.add_item(null_weapon_1)
#     i.add_item(null_weapon_2)
#     i.add_item(rusty_knife)
# i.add_item(Item.Item('Torch', 'Torch', Item.ItemType.Consumable))
# amount_of_knives = i.count_items(rusty_knife.id_)
# import random
# for x in range(0, 10):
#     i.remove_item(x, 0)
# amount_of_knives2 = i.count_items(rusty_knife.id_)
# obj = i.get_item(21, 3)
# print(amount_of_knives)
# print(amount_of_knives2)
#
# """
# page: ...
# page 2: ...
# page3: None
# page: 4 ...
# """
#
