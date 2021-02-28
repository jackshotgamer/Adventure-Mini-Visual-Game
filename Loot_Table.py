from typing import Tuple
import Exploration
import Vector
import State
import Tile
import arcade
import Sprites_
import random


class LootTable:
    def __init__(self, *items: Tuple[str, int]):
        self.items = dict(items)

    def get_item(self):
        return random.choices(tuple(self.items), k=1, weights=tuple(self.items.values()))
